# Python 3.11 슬림 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치 (필요한 경우)
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 포트 노출
EXPOSE 8000

# 비루트 사용자 생성 (보안)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 컨테이너 시작시 실행할 명령어
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 