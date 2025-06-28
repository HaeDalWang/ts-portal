"""
Customer Service 데이터베이스 설정
PostgreSQL customer_schema에 연결
"""

import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 데이터베이스 URL 설정
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://tsportal:tsportal123!@postgres:5432/tsportal"
)

# SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    echo=False  # 개발시 True로 변경 가능
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 생성
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """데이터베이스 세션을 생성하고 반환하는 의존성 함수"""
    db = SessionLocal()
    try:
        # customer_schema를 기본 스키마로 설정
        db.execute(text("SET search_path TO customer_schema, public"))
        yield db
    finally:
        db.close()

def init_db():
    """데이터베이스 초기화"""
    try:
        # customer_schema 스키마 확인 및 생성
        with engine.connect() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS customer_schema"))
            conn.commit()
        
        # 모든 모델 임포트 (테이블 생성을 위해)
        from . import models
        
        # 테이블 생성 (customer_schema에)
        Base.metadata.create_all(bind=engine)
        
        logger.info("✅ Customer Service 데이터베이스 초기화 완료")
        
    except Exception as e:
        logger.error(f"❌ Customer Service 데이터베이스 초기화 실패: {e}")
        raise

def get_db_info():
    """데이터베이스 정보 반환"""
    try:
        with engine.connect() as conn:
            # PostgreSQL 버전 확인
            result = conn.execute(text("SELECT version()")).fetchone()
            version = result[0] if result else "Unknown"
            
            # customer_schema 테이블 확인
            tables_result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'customer_schema'
            """)).fetchall()
            
            tables = [table[0] for table in tables_result]
            
            return {
                "type": "PostgreSQL",
                "schema": "customer_schema",
                "version": version,
                "tables": tables,
                "status": "connected"
            }
    except Exception as e:
        return {
            "type": "PostgreSQL",
            "schema": "customer_schema",
            "status": "error",
            "error": str(e)
        } 