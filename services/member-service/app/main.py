"""
Member Service - 팀원 관리 마이크로서비스

팀원 정보 관리, 프로필 업데이트, 권한 관리를 담당하는 독립적인 서비스입니다.
"""

from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import os
from typing import Optional

from .database import engine, Base, get_db, check_database_connection
from .routers import member_router

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
    logger.info("🚀 Member Service 시작 중...")
    
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
    
    logger.info("🎉 Member Service 시작 완료!")
    
    yield
    
    # 종료 시
    logger.info("👋 Member Service 종료 중...")

# FastAPI 애플리케이션 생성
app = FastAPI(
    title="Member Service",
    description="팀원 관리 마이크로서비스 - 프로필, 권한, 인증 정보 관리",
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

# 라우터 등록
app.include_router(member_router, prefix="/api/v1/members", tags=["members"])

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "service": "Member Service",
        "version": "1.0.0",
        "status": "healthy",
        "description": "팀원 관리 마이크로서비스"
    }

@app.get("/health")
async def health_check():
    """헬스체크 엔드포인트"""
    try:
        # 데이터베이스 연결 확인
        if await check_database_connection():
            return {
                "status": "healthy",
                "service": "member-service",
                "database": "connected"
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
        port=8001,
        reload=True,
        log_level="info"
    ) 