# 🚀 UV 기반 Dockerfile - 극도로 빠른 빌드!
FROM python:3.11-slim

LABEL maintainer="TS Portal Team"
LABEL description="calendar-service - UV 기반 마이크로서비스"

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# UV 설치 (공식 설치 스크립트)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Python 프로젝트 파일 복사
COPY services/calendar-service/pyproject.toml services/calendar-service/uv.lock* ./

# UV로 의존성 설치 (가상환경 없이 시스템에 직접 설치)
ENV UV_SYSTEM_PYTHON=1
RUN uv sync --frozen --no-dev

# 애플리케이션 코드 복사
COPY services/calendar-service/app/ ./app/

# shared 모듈 복사
COPY services/shared/ ./shared/

# 로그 디렉토리 생성
RUN mkdir -p /app/logs

# 포트 노출
EXPOSE 8000

# 헬스체크 설정
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 환경변수 설정
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# UV로 애플리케이션 실행
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 