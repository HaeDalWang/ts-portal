"""
Calendar Service - 팀 일정 관리 마이크로서비스
TS Portal의 일정 관리를 담당하는 독립 서비스
"""

import logging
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .database import init_db, get_db_info
from .routers import events_router

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="Calendar Service",
    version="1.0.0",
    description="TS Portal 팀 일정 관리 마이크로서비스",
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
app.include_router(events_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행"""
    logger.info("Calendar Service 시작 중...")
    init_db()
    logger.info("✅ Calendar Service 초기화 완료")

@app.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 실행"""
    logger.info("Calendar Service 종료")

@app.get("/")
async def root():
    """서비스 기본 정보"""
    return {
        "service": "Calendar Service",
        "version": "1.0.0",
        "description": "TS Portal 팀 일정 관리 마이크로서비스",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "/api/events": "일정 CRUD",
            "/api/events/calendar": "달력용 일정 조회",
            "/api/events/today": "오늘 일정",
            "/api/events/upcoming": "다가오는 일정",
            "/api/events/search": "일정 검색",
            "/api/events/stats": "일정 통계",
            "/api/events/types": "일정 타입 목록",
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
        "service": "calendar-service",
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
            "detail": "Calendar Service 내부 오류가 발생했습니다.",
            "service": "calendar-service",
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 