"""Rate Limiting 미들웨어"""
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 간단한 Rate Limiting 구현 (추후 Redis 기반으로 확장)
        response = await call_next(request)
        return response 