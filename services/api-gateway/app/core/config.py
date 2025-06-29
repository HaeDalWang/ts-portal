"""
API Gateway 설정 관리
==================

환경 변수 기반 설정 관리 및 서비스 엔드포인트 정의
"""

from pydantic_settings import BaseSettings
from typing import List, Dict
import os


class Settings(BaseSettings):
    """API Gateway 설정 클래스"""
    
    # 기본 설정
    APP_NAME: str = "TS Portal API Gateway"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # 서버 설정
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    
    # JWT 설정
    JWT_SECRET_KEY: str = "your-super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440  # 24시간
    
    # CORS 설정
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",  # Vue.js 개발 서버
        "http://localhost:8080",  # API Gateway
        "http://localhost:5173",  # Vite 개발 서버
        "https://ts-portal.saltware.co.kr",  # 프로덕션 도메인
    ]
    
    # Redis 설정 (캐싱 및 Rate Limiting)
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    
    # 마이크로서비스 엔드포인트
    SERVICES: Dict[str, str] = {
        "auth": "http://auth-service:8010",
        "member": "http://member-service:8001", 
        "customer": "http://customer-service:8002",
        "calendar": "http://calendar-service:8003",
        "notice": "http://notice-service:8004",
        "feeds": "http://feeds-service:8000"
    }
    
    # 헬스체크 설정
    HEALTH_CHECK_INTERVAL: int = 30  # 30초마다 헬스체크
    HEALTH_CHECK_TIMEOUT: int = 5    # 5초 타임아웃
    
    # Rate Limiting 설정
    RATE_LIMIT_REQUESTS: int = 100   # 분당 요청 수
    RATE_LIMIT_WINDOW: int = 60      # 60초 윈도우
    
    # 로깅 설정
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 모니터링 설정
    ENABLE_METRICS: bool = True
    METRICS_PATH: str = "/metrics"
    
    # 타임아웃 설정
    REQUEST_TIMEOUT: int = 30        # 30초 요청 타임아웃
    CONNECTION_TIMEOUT: int = 10     # 10초 연결 타임아웃
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# 글로벌 설정 인스턴스
settings = Settings()


def get_service_url(service_name: str) -> str:
    """서비스 이름으로 URL 가져오기"""
    return settings.SERVICES.get(service_name, "")


def get_redis_url() -> str:
    """Redis 연결 URL 생성"""
    if settings.REDIS_PASSWORD:
        return f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
    return f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"


# 환경별 설정 오버라이드
if os.getenv("ENVIRONMENT") == "development":
    settings.DEBUG = True
    settings.LOG_LEVEL = "DEBUG"
    settings.SERVICES = {
        "auth": "http://localhost:8010",
        "member": "http://localhost:8001",
        "customer": "http://localhost:8002", 
        "calendar": "http://localhost:8003",
        "notice": "http://localhost:8004",
        "feeds": "http://localhost:8000"
    }

elif os.getenv("ENVIRONMENT") == "production":
    settings.DEBUG = False
    settings.LOG_LEVEL = "WARNING"
    # 프로덕션 환경에서는 환경 변수로 설정 