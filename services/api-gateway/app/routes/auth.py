"""
Auth Service 라우터
=================

인증 관련 요청을 Auth Service로 프록시하는 라우터
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
import logging
from typing import Any, Dict

from app.core.config import get_service_url

logger = logging.getLogger(__name__)
router = APIRouter()

# Auth Service URL
AUTH_SERVICE_URL = get_service_url("auth")


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_to_auth_service(request: Request, path: str):
    """Auth Service로 모든 요청 프록시"""
    
    if not AUTH_SERVICE_URL:
        raise HTTPException(status_code=503, detail="Auth Service를 사용할 수 없습니다.")
    
    try:
        # 요청 데이터 준비
        url = f"{AUTH_SERVICE_URL}/{path}"
        headers = dict(request.headers)
        
        # Host 헤더 제거 (프록시 시 문제 방지)
        headers.pop("host", None)
        
        # 요청 본문 읽기
        body = await request.body()
        
        # 쿼리 파라미터 포함
        query_params = dict(request.query_params)
        
        logger.info(f"Auth Service 프록시: {request.method} {url}")
        
        # HTTP 클라이언트로 요청 전달
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=body,
                params=query_params
            )
            
            # 응답 헤더 준비
            response_headers = dict(response.headers)
            # 일부 헤더 제거 (프록시 시 문제 방지)
            response_headers.pop("content-encoding", None)
            response_headers.pop("content-length", None)
            response_headers.pop("transfer-encoding", None)
            
            # 응답 반환
            return JSONResponse(
                status_code=response.status_code,
                content=response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
                headers=response_headers
            )
            
    except httpx.TimeoutException:
        logger.error(f"Auth Service 타임아웃: {url}")
        raise HTTPException(status_code=504, detail="Auth Service 응답 시간 초과")
        
    except httpx.ConnectError:
        logger.error(f"Auth Service 연결 실패: {url}")
        raise HTTPException(status_code=503, detail="Auth Service에 연결할 수 없습니다.")
        
    except Exception as e:
        logger.error(f"Auth Service 프록시 오류: {e}")
        raise HTTPException(status_code=500, detail="인증 서비스 처리 중 오류가 발생했습니다.")


@router.get("/health")
async def auth_health():
    """Auth Service 헬스체크"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{AUTH_SERVICE_URL}/health")
            return response.json()
    except Exception as e:
        logger.error(f"Auth Service 헬스체크 실패: {e}")
        return {"status": "unhealthy", "error": str(e)} 