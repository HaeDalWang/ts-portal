"""
JWT 인증 미들웨어
===============

JWT 토큰 검증 및 사용자 정보 헤더 주입을 담당하는 미들웨어
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
import httpx
import logging
from datetime import datetime
from typing import Optional, Dict, Any

from app.core.config import settings, get_service_url

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    """JWT 인증 미들웨어"""
    
    # 인증이 필요 없는 경로들
    SKIP_AUTH_PATHS = {
        "/",
        "/docs",
        "/redoc", 
        "/openapi.json",
        "/health",
        "/metrics",
        "/api/auth/login",
        "/api/auth/refresh",
        "/api/auth/health",
        "/api/members/health",
        "/api/customers/health", 
        "/api/calendar/health",
        "/api/notices/health",
        "/api/feeds/health"
    }
    
    def __init__(self, app):
        super().__init__(app)
        self.auth_service_url = get_service_url("auth")
    
    async def dispatch(self, request: Request, call_next):
        """요청 처리 전 JWT 토큰 검증"""
        
        # 인증 스킵 경로 체크
        if self._should_skip_auth(request.url.path):
            return await call_next(request)
        
        try:
            # JWT 토큰 추출
            token = self._extract_token(request)
            if not token:
                return self._unauthorized_response("토큰이 없습니다.")
            
            # 토큰 검증 및 사용자 정보 추출
            user_info = await self._verify_token(token)
            if not user_info:
                return self._unauthorized_response("유효하지 않은 토큰입니다.")
            
            # 사용자 정보를 헤더에 주입
            self._inject_user_headers(request, user_info)
            
            # 요청 로깅
            logger.info(f"인증된 요청: {user_info.get('username')} -> {request.url.path}")
            
            response = await call_next(request)
            return response
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"인증 미들웨어 오류: {e}")
            return self._error_response("인증 처리 중 오류가 발생했습니다.")
    
    def _should_skip_auth(self, path: str) -> bool:
        """인증을 스킵할지 결정"""
        # 정확한 경로 매칭
        if path in self.SKIP_AUTH_PATHS:
            return True
        
        # 패턴 매칭 (예: /api/auth/*)
        for skip_path in self.SKIP_AUTH_PATHS:
            if skip_path.endswith("*") and path.startswith(skip_path[:-1]):
                return True
        
        return False
    
    def _extract_token(self, request: Request) -> Optional[str]:
        """요청에서 JWT 토큰 추출"""
        # Authorization 헤더에서 Bearer 토큰 추출
        authorization = request.headers.get("Authorization")
        if authorization and authorization.startswith("Bearer "):
            return authorization[7:]
        
        # 쿠키에서 토큰 추출 (옵션)
        token = request.cookies.get("access_token")
        if token:
            return token
        
        return None
    
    async def _verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """JWT 토큰 검증"""
        try:
            # 로컬 JWT 검증 (빠른 검증)
            payload = jwt.decode(
                token, 
                settings.JWT_SECRET_KEY, 
                algorithms=[settings.JWT_ALGORITHM]
            )
            
            # 토큰 만료 체크
            exp = payload.get("exp")
            if exp and datetime.utcnow().timestamp() > exp:
                logger.warning("만료된 토큰")
                return None
            
            # Auth Service에서 추가 검증 (선택적)
            if self.auth_service_url:
                user_info = await self._verify_with_auth_service(token)
                if user_info:
                    return user_info
            
            # 로컬 검증 결과 반환
            return {
                "user_id": payload.get("sub"),
                "username": payload.get("username"),
                "role": payload.get("role", "user"),
                "permissions": payload.get("permissions", [])
            }
            
        except JWTError as e:
            logger.warning(f"JWT 검증 실패: {e}")
            return None
        except Exception as e:
            logger.error(f"토큰 검증 오류: {e}")
            return None
    
    async def _verify_with_auth_service(self, token: str) -> Optional[Dict[str, Any]]:
        """Auth Service를 통한 토큰 검증"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(
                    f"{self.auth_service_url}/verify",
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.warning(f"Auth Service 검증 실패: {response.status_code}")
                    return None
                    
        except httpx.TimeoutException:
            logger.warning("Auth Service 타임아웃")
            return None
        except Exception as e:
            logger.error(f"Auth Service 검증 오류: {e}")
            return None
    
    def _inject_user_headers(self, request: Request, user_info: Dict[str, Any]):
        """사용자 정보를 헤더에 주입"""
        # 기존 헤더를 변경 가능한 딕셔너리로 변환
        headers = dict(request.headers)
        
        # 사용자 정보 헤더 추가
        headers["X-User-ID"] = str(user_info.get("user_id", ""))
        headers["X-Username"] = str(user_info.get("username", ""))
        headers["X-User-Role"] = str(user_info.get("role", "user"))
        headers["X-User-Permissions"] = ",".join(user_info.get("permissions", []))
        
        # 요청 객체의 헤더 업데이트
        request._headers = headers
        request.scope["headers"] = [
            (key.lower().encode(), value.encode()) 
            for key, value in headers.items()
        ]
    
    def _unauthorized_response(self, message: str) -> JSONResponse:
        """인증 실패 응답"""
        return JSONResponse(
            status_code=401,
            content={
                "error": "Unauthorized",
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
        )
    
    def _error_response(self, message: str) -> JSONResponse:
        """오류 응답"""
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
        ) 