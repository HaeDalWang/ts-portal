# TS Portal EC2 배포 가이드 🚀

EC2에서 Docker Compose를 사용한 TS Portal 백엔드 서비스 배포 가이드입니다.

## 📋 배포 구조

```
/home/ec2-user/ts-portal/
├── docker-compose.yml          # 메인 오케스트레이션
├── nginx/
│   └── nginx.conf             # Nginx 설정 (SSL + 리버스 프록시)
├── honeybox/                  # HoneyBox 소스코드 + Dockerfile
├── ts-portal-db/              # TS Portal DB 소스코드 + Dockerfile
├── data/
│   ├── sqlite/               # SQLite 데이터베이스 영구 저장
│   └── redis/                # Redis 데이터 영구 저장
├── logs/
│   ├── nginx/                # Nginx 로그
│   ├── honeybox/             # HoneyBox 애플리케이션 로그
│   └── ts-portal-db/         # TS Portal DB 애플리케이션 로그
├── ssl/
│   └── live/your-domain.com/ # SSL 인증서 파일
├── setup-directories.sh      # 디렉토리 구조 설정 스크립트
└── ssl-setup.sh              # SSL 인증서 설정 스크립트
```

## 🛠️ 서비스 구성

| 서비스 | 포트 | 역할 | 볼륨 마운트 |
|--------|------|------|-------------|
| nginx | 80, 443 | 리버스 프록시 + SSL | `./nginx/nginx.conf`, `./ssl/`, `./logs/nginx/` |
| honeybox | 8000 (내부) | AWS RSS 수집 | `./logs/honeybox/`, `./data/redis/` |
| ts-portal-db | 8001 (내부) | 팀 데이터 관리 | `./data/sqlite/`, `./logs/ts-portal-db/` |
| redis | 6379 (내부) | 캐싱 레이어 | `./data/redis/` |

## 🚀 배포 단계

### 1. EC2 인스턴스 준비

```bash
# Docker 설치
sudo yum update -y
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user

# Docker Compose 설치
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 재로그인 필요 (Docker 그룹 권한 적용)
exit
```

### 2. 프로젝트 배포

```bash
# 프로젝트 디렉토리 생성 및 이동
mkdir -p /home/ec2-user/ts-portal
cd /home/ec2-user/ts-portal

# Git에서 소스코드 다운로드 (또는 직접 업로드)
git clone <your-repo> .

# 또는 scp로 파일 업로드
# scp -r ./ts-portal ec2-user@your-ec2-ip:/home/ec2-user/
```

### 3. 디렉토리 구조 설정

```bash
# 디렉토리 구조 생성
./setup-directories.sh
```

### 4. SSL 인증서 설정

```bash
# Let's Encrypt 인증서 발급
./ssl-setup.sh
# 도메인명 입력: api.your-domain.com
```

### 5. 환경 설정

```bash
# docker-compose.yml 확인 및 수정 (필요시)
vi docker-compose.yml

# nginx.conf 확인 (도메인명이 올바르게 설정되었는지)
vi nginx/nginx.conf
```

### 6. 인증 시스템 초기화

```bash
# ts-portal-db 컨테이너에서 인증 시스템 초기화
docker-compose exec ts-portal-db python init_auth_system.py

# 또는 서비스 시작 전에 로컬에서 실행
cd ts-portal-db
python init_auth_system.py
```

**기본 관리자 계정:**
- 이메일: `admin@seungdobae.com`
- 비밀번호: `admin123!`
- ⚠️ **로그인 후 반드시 비밀번호를 변경하세요!**

### 7. 서비스 시작

```bash
# Docker 이미지 빌드 및 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

## 🔧 운영 관리

### 서비스 상태 확인

```bash
# 컨테이너 상태 확인
docker-compose ps

# 특정 서비스 로그 확인
docker-compose logs nginx
docker-compose logs honeybox
docker-compose logs ts-portal-db
docker-compose logs redis

# 실시간 로그 모니터링
docker-compose logs -f --tail=100
```

### 서비스 재시작

```bash
# 전체 서비스 재시작
docker-compose restart

# 특정 서비스만 재시작
docker-compose restart nginx
docker-compose restart honeybox
```

### 서비스 업데이트

```bash
# 코드 업데이트 후
git pull  # 또는 새 파일 업로드

# 이미지 재빌드 및 서비스 재시작
docker-compose build --no-cache
docker-compose up -d
```

## 🌐 API 엔드포인트

배포 완료 후 다음 엔드포인트로 접근 가능합니다:

### HoneyBox (AWS 뉴스 피드)
- `GET https://your-domain.com/api/feeds/` - 전체 피드 목록
- `GET https://your-domain.com/api/feeds/daily/{date}` - 일일 선별 뉴스

### TS Portal DB (팀 데이터 관리)
- `GET https://your-domain.com/api/db/` - API 기본 정보
- `GET https://your-domain.com/api/db/health` - 헬스체크
- `GET https://your-domain.com/api/db/stats` - 데이터베이스 통계

### 통합 서비스
- `GET https://your-domain.com/health` - 전체 서비스 헬스체크

## 🔐 보안 설정

### 방화벽 설정 (AWS Security Group)

```
인바운드 규칙:
- HTTP (80): 0.0.0.0/0
- HTTPS (443): 0.0.0.0/0
- SSH (22): 관리자 IP만

아웃바운드 규칙:
- All traffic: 0.0.0.0/0
```

### SSL 인증서 자동 갱신

```bash
# 크론탭 설정
sudo crontab -e

# 추가할 내용 (매월 1일 새벽 3시 갱신 시도)
0 3 1 * * certbot renew --quiet && cp -L /etc/letsencrypt/live/your-domain.com/* /home/ec2-user/ts-portal/ssl/live/your-domain.com/ && cd /home/ec2-user/ts-portal && docker-compose restart nginx
```

## 📊 모니터링

### 로그 파일 위치

```bash
# Nginx 로그
tail -f logs/nginx/access.log
tail -f logs/nginx/error.log

# 애플리케이션 로그
tail -f logs/honeybox/app.log
tail -f logs/ts-portal-db/app.log
```

### 리소스 모니터링

```bash
# Docker 컨테이너 리소스 사용량
docker stats

# 디스크 사용량
df -h
du -sh data/
```

## 🚨 문제 해결

### 일반적인 문제들

1. **SSL 인증서 오류**
   ```bash
   # 인증서 재발급
   sudo certbot delete --cert-name your-domain.com
   ./ssl-setup.sh
   ```

2. **포트 충돌**
   ```bash
   # 포트 사용 중인 프로세스 확인
   sudo netstat -tlnp | grep :80
   sudo netstat -tlnp | grep :443
   ```

3. **컨테이너 시작 실패**
   ```bash
   # 상세 로그 확인
   docker-compose logs [service-name]
   
   # 컨테이너 재빌드
   docker-compose build --no-cache [service-name]
   ```

4. **데이터베이스 연결 오류**
   ```bash
   # SQLite 파일 권한 확인
   ls -la data/sqlite/
   
   # 컨테이너 내부 확인
   docker-compose exec ts-portal-db bash
   ```

## 📈 성능 최적화

### Nginx 최적화

```nginx
# nginx.conf에 추가 가능한 설정들
worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    # 압축 설정
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript;
    
    # 캐싱 설정
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### 리소스 제한

```yaml
# docker-compose.yml에 추가
services:
  honeybox:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
```

---

**배포 완료 후 Frontend에서 API 엔드포인트를 `https://your-domain.com/api/`로 설정하세요!** 🎉 