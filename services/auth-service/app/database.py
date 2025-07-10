"""
Auth Service - 데이터베이스 설정

shared/database.py를 사용한 간소화된 설정
Member 모델 (인증용) - member_schema.members 테이블 참조
"""

import sys
import os

# shared 모듈 import를 위한 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.database import create_database_config, Base

# Auth Service용 데이터베이스 설정 생성
db_config = create_database_config("auth-service")

# 기존 인터페이스 호환성을 위한 export
engine = db_config.engine
SessionLocal = db_config.SessionLocal
get_db = db_config.get_db
check_database_connection = db_config.check_connection

# Auth Service는 별도 테이블 생성 없이 기존 member 테이블 사용
def init_database():
    """
    데이터베이스 초기화
    
    Auth Service는 별도 테이블을 생성하지 않고 member_schema.members를 참조
    """
    # Auth Service는 스키마 확인만 수행
    db_config.init_schema()
    # 테이블 생성은 하지 않음 (member-service에서 담당)

# 추가 편의 함수들
def get_db_info():
    """데이터베이스 정보 반환"""
    return db_config.get_db_info() 