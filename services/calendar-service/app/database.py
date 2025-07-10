"""
Calendar Service 데이터베이스 설정

shared/database.py를 사용한 간소화된 설정
PostgreSQL calendar_schema에 연결
"""

import sys
import os
from typing import Generator
from sqlalchemy.orm import Session

# shared 모듈 import를 위한 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.database import create_database_config, Base

# Calendar Service용 데이터베이스 설정 생성
db_config = create_database_config("calendar-service")

# 기존 인터페이스 호환성을 위한 export
engine = db_config.engine
SessionLocal = db_config.SessionLocal
Base = Base

def get_db() -> Generator[Session, None, None]:
    """데이터베이스 세션을 생성하고 반환하는 의존성 함수"""
    return db_config.get_db()

def init_db():
    """데이터베이스 초기화"""
    # 모든 모델 임포트 (테이블 생성을 위해)
    from . import models
    
    # 데이터베이스 초기화 실행
    db_config.init_database()

def get_db_info():
    """데이터베이스 정보 반환"""
    return db_config.get_db_info() 