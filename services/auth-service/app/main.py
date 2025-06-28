"""
Auth Service - 인증/인가 마이크로서비스

JWT 토큰 발급, 검증, 사용자 인증을 담당하는 독립적인 서비스입니다.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import logging
import os
from typing import Optional

from .database import engine, Base, get_db, check_database_connection
from .routers import auth_router

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
    logger.info("🔐 Auth Service 시작 중...")
    
    # 데이터베이스 테이블 생성
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ 데이터베이스 테이블 생성 완료")
        
        # 데이터베이스 연결 확인
        if await check_database_connection():
            logger.info("✅ 데이터베이스 연결 확인 완료")
        else:
            logger.error("❌ 데이터베이스 연결 실패")
            
    except Exception as e:
        logger.error(f"❌ 데이터베이스 초기화 실패: {e}")
    
    logger.info("🎉 Auth Service 시작 완료!")
    
    yield
    
    # 종료 시
    logger.info("👋 Auth Service 종료 중...")

# FastAPI 애플리케이션 생성
app = FastAPI(
    title="Auth Service",
    description="인증/인가 마이크로서비스 - JWT 토큰 관리, 로그인/로그아웃",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발환경용, 운영환경에서는 구체적인 도메인 지정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Bearer 토큰 스키마
security = HTTPBearer()

# 라우터 등록
app.include_router(auth_router, prefix="/api/v1/auth", tags=["authentication"])

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "service": "Auth Service",
        "version": "1.0.0",
        "status": "healthy",
        "description": "인증/인가 마이크로서비스",
        "endpoints": {
            "/api/v1/auth/login": "로그인",
            "/api/v1/auth/logout": "로그아웃",
            "/api/v1/auth/verify": "토큰 검증",
            "/api/v1/auth/refresh": "토큰 갱신",
            "/api/v1/auth/me": "현재 사용자 정보",
            "/health": "헬스 체크",
            "/docs": "API 문서"
        }
    }

@app.get("/health")
async def health_check():
    """헬스체크 엔드포인트"""
    try:
        # 데이터베이스 연결 확인
        if await check_database_connection():
            return {
                "status": "healthy",
                "service": "auth-service",
                "database": "connected",
                "jwt_secret": "configured" if os.getenv("JWT_SECRET_KEY") else "missing"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection failed"
            )
    except Exception as e:
        logger.error(f"헬스체크 실패: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service unhealthy: {str(e)}"
        )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """전역 예외 처리"""
    logger.error(f"전역 예외 발생: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8010,
        reload=True,
        log_level="info"
    ) 