"""
Shared Database Configuration for TS Portal Services

모든 서비스에서 공통으로 사용하는 데이터베이스 설정
"""

import os
import logging
from typing import Generator, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

# 기본 데이터베이스 URL
DEFAULT_DATABASE_URL = "postgresql://tsportal:tsportal123!@postgres:5432/tsportal"

# Base 클래스 (모든 서비스에서 공통 사용)
Base = declarative_base()


class DatabaseConfig:
    """데이터베이스 설정 클래스"""
    
    def __init__(
        self,
        schema_name: str,
        service_name: str,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_recycle: int = 300,
        echo: bool = False
    ):
        self.schema_name = schema_name
        self.service_name = service_name
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool_recycle = pool_recycle
        self.echo = echo
        
        # 데이터베이스 URL (환경변수에서 가져오기)
        self.database_url = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)
        
        # SQLAlchemy 엔진 생성
        self.engine = create_engine(
            self.database_url,
            pool_pre_ping=True,
            pool_recycle=self.pool_recycle,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
            echo=self.echo
        )
        
        # 세션 팩토리 생성
        self.SessionLocal = sessionmaker(
            autocommit=False, 
            autoflush=False, 
            bind=self.engine
        )
    
    def get_db(self) -> Generator[Session, None, None]:
        """데이터베이스 세션을 생성하고 반환하는 의존성 함수"""
        db = self.SessionLocal()
        try:
            # 스키마를 기본 검색 경로로 설정
            if self.schema_name:
                db.execute(text(f"SET search_path TO {self.schema_name}, public"))
            yield db
        except Exception as e:
            logger.error(f"{self.service_name} 데이터베이스 세션 오류: {e}")
            db.rollback()
            raise
        finally:
            db.close()
    
    async def check_connection(self) -> bool:
        """데이터베이스 연결 상태 확인"""
        try:
            db = self.SessionLocal()
            # 간단한 연결 테스트
            if self.schema_name:
                # 스키마가 있는 경우 스키마 존재 여부 확인
                result = db.execute(text(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{self.schema_name}'"))
                if not result.fetchone():
                    logger.warning(f"⚠️ {self.service_name}: 스키마 '{self.schema_name}'가 존재하지 않습니다.")
            else:
                # 기본 연결 테스트
                db.execute(text("SELECT 1"))
            
            db.close()
            logger.info(f"✅ {self.service_name} 데이터베이스 연결 확인 성공")
            return True
        except SQLAlchemyError as e:
            logger.error(f"❌ {self.service_name} 데이터베이스 연결 실패: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ {self.service_name} 예상치 못한 데이터베이스 오류: {e}")
            return False
    
    def init_schema(self):
        """스키마 생성 (필요한 경우)"""
        if not self.schema_name:
            return
            
        try:
            with self.engine.connect() as conn:
                conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {self.schema_name}"))
                conn.commit()
                logger.info(f"✅ {self.service_name}: 스키마 '{self.schema_name}' 확인/생성 완료")
        except Exception as e:
            logger.error(f"❌ {self.service_name}: 스키마 생성 실패: {e}")
            raise
    
    def init_tables(self):
        """테이블 생성"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info(f"✅ {self.service_name} 데이터베이스 테이블 생성 완료")
        except Exception as e:
            logger.error(f"❌ {self.service_name} 데이터베이스 테이블 생성 실패: {e}")
            raise
    
    def init_database(self):
        """전체 데이터베이스 초기화"""
        try:
            self.init_schema()
            self.init_tables()
            logger.info(f"✅ {self.service_name} 데이터베이스 초기화 완료")
        except Exception as e:
            logger.error(f"❌ {self.service_name} 데이터베이스 초기화 실패: {e}")
            raise
    
    def get_db_info(self):
        """데이터베이스 정보 반환"""
        try:
            with self.engine.connect() as conn:
                # PostgreSQL 버전 확인
                result = conn.execute(text("SELECT version()")).fetchone()
                version = result[0] if result else "Unknown"
                
                # 스키마의 테이블 확인
                if self.schema_name:
                    tables_result = conn.execute(text(f"""
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = '{self.schema_name}'
                    """)).fetchall()
                    tables = [table[0] for table in tables_result]
                else:
                    tables = []
                
                return {
                    "service": self.service_name,
                    "type": "PostgreSQL",
                    "schema": self.schema_name,
                    "version": version,
                    "tables": tables,
                    "status": "connected"
                }
        except Exception as e:
            return {
                "service": self.service_name,
                "type": "PostgreSQL",
                "schema": self.schema_name,
                "status": "error",
                "error": str(e)
            }


# 서비스별 사전 정의된 설정
SERVICE_CONFIGS = {
    "auth-service": {
        "schema_name": "member_schema",
        "pool_size": 20,
        "max_overflow": 30
    },
    "member-service": {
        "schema_name": "member_schema", 
        "pool_size": 20,
        "max_overflow": 30
    },
    "calendar-service": {
        "schema_name": "calendar_schema",
        "pool_size": 5,
        "max_overflow": 10
    },
    "customer-service": {
        "schema_name": "customer_schema",
        "pool_size": 5,
        "max_overflow": 10
    },
    "notice-service": {
        "schema_name": "notice_schema",
        "pool_size": 5,
        "max_overflow": 10
    }
}


def create_database_config(service_name: str, **kwargs) -> DatabaseConfig:
    """서비스별 데이터베이스 설정 생성"""
    if service_name in SERVICE_CONFIGS:
        config = SERVICE_CONFIGS[service_name].copy()
        config.update(kwargs)
        return DatabaseConfig(service_name=service_name, **config)
    else:
        # 기본 설정
        return DatabaseConfig(
            schema_name=kwargs.get("schema_name", ""),
            service_name=service_name,
            **kwargs
        ) 