"""
Notice Service - 공지사항 마이크로서비스
TS Portal의 공지사항 관리를 담당하는 독립 서비스
"""

import logging
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .database import init_db, get_db_info
from .routers import notices_router

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="Notice Service",
    version="1.0.0",
    description="TS Portal 공지사항 마이크로서비스",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # API Gateway를 통해서만 접근하므로 나중에 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(notices_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행"""
    logger.info("Notice Service 시작 중...")
    init_db()
    logger.info("✅ Notice Service 초기화 완료")

@app.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 실행"""
    logger.info("Notice Service 종료")

@app.get("/")
async def root():
    """서비스 기본 정보"""
    return {
        "service": "Notice Service",
        "version": "1.0.0",
        "description": "TS Portal 공지사항 마이크로서비스",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "/api/notices": "공지사항 CRUD",
            "/api/notices/search": "공지사항 검색",
            "/api/notices/pinned": "고정 공지사항",
            "/api/notices/recent": "최근 공지사항",
            "/api/notices/stats": "공지사항 통계",
            "/health": "헬스 체크",
            "/docs": "API 문서"
        }
    }

@app.get("/health")
async def health_check():
    """헬스 체크"""
    db_info = get_db_info()
    return {
        "status": "healthy",
        "service": "notice-service",
        "timestamp": datetime.now().isoformat(),
        "database": db_info
    }

# 전역 예외 처리
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """전역 예외 처리기"""
    logger.error(f"처리되지 않은 예외: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Notice Service 내부 오류가 발생했습니다.",
            "service": "notice-service",
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004, reload=True) 