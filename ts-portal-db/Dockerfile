# TS Portal Database API Dockerfile
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치 (SQLite 관련)
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 파일 복사
COPY requirements.txt .

# Python 의존성 설치
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY app/ ./app/
COPY main.py .
COPY init_sample_data.py .

# 데이터 디렉토리 생성 (볼륨 마운트용)
RUN mkdir -p /app/data

# 비루트 사용자 생성 및 권한 설정
RUN groupadd -r tsportal && useradd -r -g tsportal tsportal && \
    chown -R tsportal:tsportal /app

# 비루트 사용자로 전환
USER tsportal

# 포트 노출
EXPOSE 8001

# 헬스체크 추가
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8001/health')" || exit 1

# 애플리케이션 실행
CMD ["python", "main.py"] 