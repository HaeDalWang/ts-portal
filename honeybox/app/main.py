"""
HoneyBox - AWS 소식 RSS 수집기
FastAPI 메인 애플리케이션
"""

import logging
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .models.schemas import APIInfoResponse, HealthResponse
from .routers import feeds_router, daily_news_router

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(feeds_router)
app.include_router(daily_news_router)


@app.get("/", response_model=APIInfoResponse)
async def root():
    """API 기본 정보를 반환합니다."""
    return APIInfoResponse(
        message="HoneyBox - AWS 소식 RSS 수집기에 오신 것을 환영합니다!",
        version=settings.APP_VERSION,
        endpoints={
            "/feeds": "사용 가능한 RSS 피드 목록",
            "/feeds/all": "모든 피드에서 최신 게시물 수집",
            "/feeds/{feed_id}": "특정 피드 조회",
            "/daily-tip": "오늘의 AWS 소식",
            "/health": "헬스 체크",
            "/docs": "API 문서 (Swagger UI)",
            "/redoc": "API 문서 (ReDoc)"
        }
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """서비스 헬스 체크를 수행합니다."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat()
    )


@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행되는 이벤트"""
    logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} 시작됨")
    logger.info(f"번역 기능: {'활성화' if settings.ENABLE_TRANSLATION else '비활성화'}")
    logger.info(f"설정된 RSS 피드 수: {len(settings.AWS_BLOG_FEEDS)}")


@app.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 실행되는 이벤트"""
    logger.info("HoneyBox 애플리케이션 종료")


# 전역 예외 처리
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """전역 예외 처리기"""
    logger.error(f"처리되지 않은 예외: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "내부 서버 오류가 발생했습니다.",
            "error": str(exc) if settings.ENABLE_TRANSLATION else "Internal server error"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 