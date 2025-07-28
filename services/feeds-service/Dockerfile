# TS Portal Feeds Service Dockerfile
# UV 기반 Python 환경으로 최적화된 컨테이너 (경량화)

FROM python:3.11-slim

# 메타데이터
LABEL maintainer="Seungdo Bae <seungdobae@saltware.co.kr>"
LABEL description="TS Portal Feeds Service - AWS 소식 수집 마이크로서비스"
LABEL version="0.1.0"

# 환경 변수 설정 (UV 캐시 비활성화로 권한 문제 해결)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/root/.local/bin:$PATH" \
    UV_NO_CACHE=1 \
    UV_CACHE_DIR=/dev/null

# 시스템 패키지 업데이트 및 필수 도구 설치
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# UV 설치 (최신 버전)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# 작업 디렉토리 생성
WORKDIR /app

# 의존성 관리 파일 복사
COPY services/feeds-service/pyproject.toml services/feeds-service/uv.lock ./

# UV로 의존성 설치 (캐시 없이 안전하게)
RUN uv sync --frozen --no-dev --no-cache

# 애플리케이션 코드 복사 (경량화된 단일 파일)
COPY services/feeds-service/app/ ./app/

# 로그 디렉토리 생성
RUN mkdir -p /app/logs

# 비root 사용자 생성 및 권한 설정
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# 헬스체크 설정
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 포트 노출
EXPOSE 8000

# 환경변수 설정
ENV PYTHONPATH=/app

# UV를 사용하여 애플리케이션 실행
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 