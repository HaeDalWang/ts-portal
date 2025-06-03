# 🚀 Frontend Deployment Guide

## 📋 환경변수 설정

### 1. 로컬 개발환경
```bash
# .env 파일
VITE_HONEYBOX_API_URL=http://localhost:8000
```

### 2. AWS ECS 배포시
```bash
# Docker 환경변수로 설정
docker run -e VITE_HONEYBOX_API_URL=https://honeybox-api.your-domain.com your-frontend-image

# docker-compose.yml
environment:
  - VITE_HONEYBOX_API_URL=https://honeybox-api.your-domain.com
```

### 3. AWS EKS 배포시
```yaml
# kubernetes deployment.yaml
env:
  - name: VITE_HONEYBOX_API_URL
    value: "https://honeybox-api.your-domain.com"
```

### 4. CI/CD 파이프라인에서
```bash
# GitHub Actions에서
echo "VITE_HONEYBOX_API_URL=https://honeybox-api.your-domain.com" > .env

# AWS CodeBuild에서  
echo "VITE_HONEYBOX_API_URL=$HONEYBOX_API_URL" > .env
```

## 🔧 빌드 시점 환경변수 주입

Vite는 빌드 시점에 환경변수를 번들에 포함시킵니다:

```bash
# 빌드시 환경변수 덮어쓰기
VITE_HONEYBOX_API_URL=https://prod-api.com npm run build

# 또는 .env.production 파일 사용
echo "VITE_HONEYBOX_API_URL=https://prod-api.com" > .env.production
npm run build
```

## 📝 주의사항

- `VITE_` 접두사를 반드시 사용해야 클라이언트에서 접근 가능
- 환경변수는 빌드 시점에 정적으로 대체됨 (런타임 변경 불가)
- 민감한 정보는 환경변수에 포함하지 말 것

## 🌐 도메인 예시

```bash
# 내부 서비스 통신 (같은 클러스터)
VITE_HONEYBOX_API_URL=http://honeybox-service:8000

# ALB를 통한 외부 접근
VITE_HONEYBOX_API_URL=https://api.ts-portal.com/honeybox

# CloudFront + ALB
VITE_HONEYBOX_API_URL=https://d1234567890.cloudfront.net/api
``` 