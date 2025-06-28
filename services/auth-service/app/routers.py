"""
Auth Service - API 라우터

인증/인가 REST API 엔드포인트 정의
"""

import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from .database import get_db
from .service import AuthService
from .schemas import (
    LoginRequest, TokenResponse, TokenVerifyRequest, TokenVerifyResponse,
    CurrentUserResponse, LogoutRequest, SuccessResponse
)

logger = logging.getLogger(__name__)

# 라우터 생성
auth_router = APIRouter()

# Bearer 토큰 스키마
security = HTTPBearer()


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """AuthService 의존성 주입"""
    return AuthService(db)


@auth_router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    사용자 로그인
    
    - 이메일과 비밀번호로 인증
    - 성공 시 JWT 토큰 반환
    - 마지막 로그인 시간 업데이트
    """
    try:
        return auth_service.login(login_data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"로그인 처리 중 오류: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="로그인 처리 중 오류가 발생했습니다."
        )


@auth_router.post("/logout", response_model=SuccessResponse)
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    사용자 로그아웃
    
    - Bearer 토큰 필요
    - 토큰 유효성 검증 후 로그아웃 처리
    """
    try:
        token = credentials.credentials
        success = auth_service.logout(token)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 토큰입니다."
            )
        
        return SuccessResponse(message="성공적으로 로그아웃되었습니다.")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"로그아웃 처리 중 오류: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="로그아웃 처리 중 오류가 발생했습니다."
        )


@auth_router.post("/verify", response_model=TokenVerifyResponse)
async def verify_token(
    token_request: TokenVerifyRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    JWT 토큰 검증
    
    - 다른 마이크로서비스에서 토큰 검증 시 사용
    - 토큰 유효성과 사용자 정보 반환
    """
    try:
        token_data = auth_service.verify_token(token_request.token)
        
        if not token_data:
            return TokenVerifyResponse(
                valid=False,
                message="토큰 검증에 실패했습니다."
            )
        
        if not token_data.get("valid", False):
            return TokenVerifyResponse(
                valid=False,
                message=token_data.get("message", "유효하지 않은 토큰입니다.")
            )
        
        return TokenVerifyResponse(
            valid=True,
            user_id=token_data.get("user_id"),
            user_role=token_data.get("role"),
            expires_at=token_data.get("expires_at"),
            message="토큰이 유효합니다."
        )
        
    except Exception as e:
        logger.error(f"토큰 검증 중 오류: {e}")
        return TokenVerifyResponse(
            valid=False,
            message="토큰 검증 중 오류가 발생했습니다."
        )


@auth_router.get("/me", response_model=CurrentUserResponse)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    현재 사용자 정보 조회
    
    - Bearer 토큰 필요
    - 토큰에서 사용자 정보 추출하여 반환
    """
    try:
        token = credentials.credentials
        user = auth_service.get_current_user_from_token(token)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 토큰입니다.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return CurrentUserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            position=user.position,
            team=user.team,
            is_active=user.is_active,
            last_login=user.last_login
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"현재 사용자 조회 중 오류: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="사용자 정보 조회 중 오류가 발생했습니다."
        )


@auth_router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    토큰 갱신
    
    - 기존 토큰이 유효한 경우 새로운 토큰 발급
    - 토큰 만료 시간 연장
    """
    try:
        token = credentials.credentials
        user = auth_service.get_current_user_from_token(token)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 토큰입니다.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 새로운 토큰 생성
        token_data = auth_service.create_access_token(user)
        return TokenResponse(**token_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"토큰 갱신 중 오류: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="토큰 갱신 중 오류가 발생했습니다."
        )


# API Gateway용 헤더 기반 토큰 검증 엔드포인트
@auth_router.get("/validate")
async def validate_token_for_gateway(
    authorization: Optional[str] = Header(None),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    API Gateway용 토큰 검증 엔드포인트
    
    - Authorization 헤더에서 토큰 추출
    - 검증 결과를 헤더로 반환 (X-User-ID, X-User-Role)
    """
    try:
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization 헤더가 필요합니다."
            )
        
        # Bearer 토큰 추출
        token = auth_service.extract_token_from_header(authorization)
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 Authorization 헤더 형식입니다."
            )
        
        # 토큰 검증
        token_data = auth_service.verify_token(token)
        if not token_data or not token_data.get("valid"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 토큰입니다."
            )
        
        # API Gateway에서 사용할 헤더 정보 반환
        return {
            "user_id": token_data.get("user_id"),
            "user_role": token_data.get("role"),
            "email": token_data.get("email"),
            "valid": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Gateway 토큰 검증 중 오류: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="토큰 검증 중 오류가 발생했습니다."
        ) 