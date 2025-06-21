"""
데이터베이스 설정 및 연결 관리
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# 데이터베이스 파일 경로
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "data")
DATABASE_PATH = os.path.join(DATABASE_DIR, "ts_portal.db")

# 데이터 디렉토리 생성
os.makedirs(DATABASE_DIR, exist_ok=True)

# SQLite 연결 URL
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# SQLAlchemy 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,  # SQLite의 스레드 체크 비활성화
        "timeout": 20,  # 타임아웃 설정
    },
    poolclass=StaticPool,  # 연결 풀 설정
    pool_pre_ping=True,  # 연결 상태 확인
    pool_recycle=300,  # 연결 재활용 시간
    echo=False,  # SQL 쿼리 로그 (개발 시 True로 변경 가능)
)

# 세션 생성기
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 (모든 모델의 부모 클래스)
Base = declarative_base()


def get_db():
    """
    데이터베이스 세션을 생성하고 반환하는 의존성 함수
    FastAPI의 Depends와 함께 사용
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    데이터베이스 초기화 함수
    - 테이블 생성
    - SQLite 최적화 설정
    """
    # SQLite 최적화 설정
    with engine.connect() as conn:
        # WAL 모드 활성화 (동시 읽기 가능)
        conn.execute(text("PRAGMA journal_mode=WAL;"))
        # 동기화 모드 설정 (성능 향상)
        conn.execute(text("PRAGMA synchronous=NORMAL;"))
        # 캐시 크기 설정
        conn.execute(text("PRAGMA cache_size=1000;"))
        # 임시 저장소를 메모리에 설정
        conn.execute(text("PRAGMA temp_store=memory;"))
        # 외래 키 제약 조건 활성화
        conn.execute(text("PRAGMA foreign_keys=ON;"))
        conn.commit()
    
    # 모든 테이블 생성
    Base.metadata.create_all(bind=engine)
    print(f"✅ 데이터베이스 초기화 완료: {DATABASE_PATH}")


def get_database_url():
    """
    데이터베이스 URL 반환
    """
    return SQLALCHEMY_DATABASE_URL


def get_db_info():
    """
    데이터베이스 정보 반환
    """
    return {
        "database_path": DATABASE_PATH,
        "database_exists": os.path.exists(DATABASE_PATH),
        "database_size": os.path.getsize(DATABASE_PATH) if os.path.exists(DATABASE_PATH) else 0,
    } 