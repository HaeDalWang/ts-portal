"""Calendar Service 라우터"""
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
import logging
from app.core.config import get_service_url

logger = logging.getLogger(__name__)
router = APIRouter()

CALENDAR_SERVICE_URL = get_service_url("calendar")

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_to_calendar_service(request: Request, path: str):
    """Calendar Service로 모든 요청 프록시"""
    if not CALENDAR_SERVICE_URL:
        raise HTTPException(status_code=503, detail="Calendar Service를 사용할 수 없습니다.")
    
    try:
        url = f"{CALENDAR_SERVICE_URL}/{path}"
        headers = dict(request.headers)
        headers.pop("host", None)
        body = await request.body()
        query_params = dict(request.query_params)
        
        logger.info(f"Calendar Service 프록시: {request.method} {url}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=body,
                params=query_params
            )
            
            response_headers = dict(response.headers)
            response_headers.pop("content-encoding", None)
            response_headers.pop("content-length", None)
            response_headers.pop("transfer-encoding", None)
            
            return JSONResponse(
                status_code=response.status_code,
                content=response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
                headers=response_headers
            )
            
    except httpx.TimeoutException:
        logger.error(f"Calendar Service 타임아웃: {url}")
        raise HTTPException(status_code=504, detail="Calendar Service 응답 시간 초과")
    except httpx.ConnectError:
        logger.error(f"Calendar Service 연결 실패: {url}")
        raise HTTPException(status_code=503, detail="Calendar Service에 연결할 수 없습니다.")
    except Exception as e:
        logger.error(f"Calendar Service 프록시 오류: {e}")
        raise HTTPException(status_code=500, detail="Calendar Service 처리 중 오류가 발생했습니다.") 