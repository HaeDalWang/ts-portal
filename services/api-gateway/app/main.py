"""
TS Portal API Gateway
===================

마이크로서비스 아키텍처를 위한 중앙 집중식 API Gateway

주요 기능:
- JWT 기반 인증 및 권한 관리
- 마이크로서비스 라우팅 및 프록시
- 요청/응답 로깅 및 모니터링
- Rate Limiting 및 캐싱
- 헬스체크 통합
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from datetime import datetime

from app.middleware.auth import AuthMiddleware
from app.middleware.logging import LoggingMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.routes import auth, members, customers, calendar, notices, feeds
from app.core.config import settings
from app.core.health import health_checker
from app.services.service_registry import service_registry

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    # 시작 시
    logger.info("🚀 TS Portal API Gateway 시작 중...")
    
    # 서비스 레지스트리 초기화
    await service_registry.initialize()
    
    # 헬스체커 시작
    await health_checker.start()
    
    logger.info("✅ API Gateway 시작 완료!")
    
    yield
    
    # 종료 시
    logger.info("🛑 API Gateway 종료 중...")
    await health_checker.stop()
    await service_registry.cleanup()
    logger.info("✅ API Gateway 종료 완료!")


# FastAPI 애플리케이션 생성
app = FastAPI(
    title="TS Portal API Gateway",
    description="""
    ## TS Portal 마이크로서비스 API Gateway
    
    ### 주요 기능
    - 🔐 **JWT 인증**: 통합 인증 및 권한 관리
    - 🔄 **스마트 라우팅**: 마이크로서비스 자동 라우팅
    - 📊 **모니터링**: 실시간 성능 및 헬스 모니터링
    - 🛡️ **보안**: Rate Limiting, CORS, 보안 헤더
    - 📝 **로깅**: 구조화된 요청/응답 로깅
    
    ### 지원 서비스
    - Auth Service (인증/권한)
    - Member Service (팀원 관리)
    - Customer Service (고객사 관리)
    - Calendar Service (일정 관리)
    - Notice Service (공지사항)
    - HoneyBox (AWS 소식)
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 커스텀 미들웨어 추가
app.add_middleware(AuthMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)


# 라우터 등록
app.include_router(auth.router, prefix="/api/auth", tags=["🔐 Authentication"])
app.include_router(members.router, prefix="/api/members", tags=["👥 Members"])
app.include_router(customers.router, prefix="/api/customers", tags=["🏢 Customers"])
app.include_router(calendar.router, prefix="/api/calendar", tags=["📅 Calendar"])
app.include_router(notices.router, prefix="/api/notices", tags=["📢 Notices"])
app.include_router(feeds.router, prefix="/api/feeds", tags=["📰 Feeds"])


@app.get("/", tags=["🏠 Root"])
async def root():
    """API Gateway 루트 엔드포인트"""
    return {
        "service": "TS Portal API Gateway",
        "version": "1.0.0",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "documentation": "/docs",
        "services": {
            "auth": "/api/auth",
            "members": "/api/members", 
            "customers": "/api/customers",
            "calendar": "/api/calendar",
            "notices": "/api/notices",
            "feeds": "/api/feeds"
        }
    }


@app.get("/health", tags=["🏥 Health"])
async def health_check():
    """통합 헬스체크 엔드포인트"""
    try:
        health_status = await health_checker.check_all_services()
        
        # 모든 서비스가 정상이면 200, 하나라도 문제가 있으면 503
        status_code = 200 if all(
            service["status"] == "healthy" 
            for service in health_status["services"].values()
        ) else 503
        
        return JSONResponse(
            status_code=status_code,
            content={
                "status": "healthy" if status_code == 200 else "unhealthy",
                "gateway": "TS Portal API Gateway",
                "timestamp": datetime.now().isoformat(),
                **health_status
            }
        )
    except Exception as e:
        logger.error(f"헬스체크 실패: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "gateway": "TS Portal API Gateway",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )


@app.get("/metrics", tags=["📊 Metrics"])
async def metrics():
    """Prometheus 메트릭 엔드포인트"""
    from app.core.metrics import generate_metrics
    return generate_metrics()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP 예외 처리"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url),
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """일반 예외 처리"""
    logger.error(f"예상치 못한 오류: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "서버 내부 오류가 발생했습니다.",
            "path": str(request.url),
            "timestamp": datetime.now().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    ) 