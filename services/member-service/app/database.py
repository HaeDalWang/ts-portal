"""
Member Service - 데이터베이스 설정

PostgreSQL member_schema 연결 및 세션 관리
"""

import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

# 데이터베이스 URL (환경변수에서 가져오기)
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://tsportal:tsportal123!@localhost:5432/tsportal"
)

# SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,          # 연결 상태 확인
    pool_recycle=300,            # 5분마다 연결 재생성
    pool_size=20,                # 커넥션 풀 크기
    max_overflow=30,             # 추가 연결 허용
    echo=False                   # SQL 로깅 (개발시에만 True)
)

# 세션 로컬 클래스
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스
Base = declarative_base()

def get_db():
    """
    데이터베이스 세션 의존성
    
    FastAPI 의존성 주입용 제너레이터
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"데이터베이스 세션 오류: {e}")
        db.rollback()
        raise
    finally:
        db.close()

async def check_database_connection() -> bool:
    """
    데이터베이스 연결 상태 확인
    
    Returns:
        bool: 연결 성공 여부
    """
    try:
        db = SessionLocal()
        # member_schema가 존재하는지 확인하는 간단한 쿼리
        result = db.execute(text("SELECT 1 FROM member_schema.members LIMIT 1"))
        db.close()
        logger.info("✅ 데이터베이스 연결 확인 성공")
        return True
    except SQLAlchemyError as e:
        logger.error(f"❌ 데이터베이스 연결 실패: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ 예상치 못한 데이터베이스 오류: {e}")
        return False

def init_database():
    """
    데이터베이스 초기화
    
    테이블 생성 및 기본 데이터 설정
    """
    try:
        # 스키마별로 테이블 생성 
        Base.metadata.create_all(bind=engine)
        logger.info("✅ 데이터베이스 테이블 생성 완료")
        
    except Exception as e:
        logger.error(f"❌ 데이터베이스 초기화 실패: {e}")
        raise 