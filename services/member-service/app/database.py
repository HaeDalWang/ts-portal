"""
Member Service - 데이터베이스 설정

shared/database.py를 사용한 간소화된 설정
"""

import sys
import os

# shared 모듈 import를 위한 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.database import create_database_config, Base

# Member Service용 데이터베이스 설정 생성
db_config = create_database_config("member-service")

# 기존 인터페이스 호환성을 위한 export
engine = db_config.engine
SessionLocal = db_config.SessionLocal
get_db = db_config.get_db
check_database_connection = db_config.check_connection
init_database = db_config.init_database

# 추가 편의 함수들
def get_db_info():
    """데이터베이스 정보 반환"""
    return db_config.get_db_info() 