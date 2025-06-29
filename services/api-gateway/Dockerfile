# TS Portal API Gateway Dockerfile
# UV 기반 Python 환경으로 최적화된 컨테이너

FROM python:3.11-slim

# 메타데이터
LABEL maintainer="Seungdo Bae <seungdobae@saltware.co.kr>"
LABEL description="TS Portal API Gateway - 마이크로서비스 통합 게이트웨이"
LABEL version="1.0.0"

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
COPY pyproject.toml uv.lock ./

# UV로 의존성 설치 (캐시 없이 안전하게)
RUN uv sync --frozen --no-dev --no-cache

# 애플리케이션 코드 복사
COPY app/ ./app/

# 로그 디렉토리 생성
RUN mkdir -p /app/logs

# 비root 사용자 생성 및 권한 설정
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# 헬스체크 설정
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# 포트 노출
EXPOSE 8080

# UV를 사용하여 애플리케이션 실행 (진정한 UV 방식)
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"] 