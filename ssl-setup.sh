#!/bin/bash

# Let's Encrypt SSL 인증서 설정 스크립트
# 실행 위치: /home/ec2-user/ts-portal

set -e

# 도메인명 입력 받기
read -p "🌐 도메인명을 입력하세요 (예: api.your-domain.com): " DOMAIN

if [ -z "$DOMAIN" ]; then
    echo "❌ 도메인명이 입력되지 않았습니다."
    exit 1
fi

echo "🔐 SSL 인증서 설정을 시작합니다..."
echo "도메인: $DOMAIN"

# Certbot 설치 확인
if ! command -v certbot &> /dev/null; then
    echo "📦 Certbot 설치 중..."
    sudo apt update
    sudo apt install -y certbot
fi

# 기존 Nginx 중지 (포트 80 사용 중일 수 있음)
echo "🛑 기존 서비스 중지 중..."
docker-compose down 2>/dev/null || true

# Let's Encrypt 인증서 발급
echo "📜 SSL 인증서 발급 중..."
sudo certbot certonly \
    --standalone \
    --email your-email@example.com \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN

# 인증서를 프로젝트 디렉토리로 복사
echo "📋 인증서 복사 중..."
sudo mkdir -p ./ssl/live/$DOMAIN
sudo cp -L /etc/letsencrypt/live/$DOMAIN/* ./ssl/live/$DOMAIN/
sudo chown -R $USER:$USER ./ssl/

# Nginx 설정 파일에서 도메인명 업데이트
echo "⚙️ Nginx 설정 업데이트 중..."
sed -i "s/your-domain.com/$DOMAIN/g" nginx/nginx.conf
sed -i "s/server_name _;/server_name $DOMAIN;/g" nginx/nginx.conf

echo "✅ SSL 인증서 설정 완료!"
echo ""
echo "📋 설정된 내용:"
echo "  - 도메인: $DOMAIN"
echo "  - 인증서 위치: ./ssl/live/$DOMAIN/"
echo "  - Nginx 설정 업데이트 완료"
echo ""
echo "🚀 이제 docker-compose up -d 를 실행하세요!"

# 자동 갱신 크론탭 설정 안내
echo ""
echo "📅 SSL 인증서 자동 갱신 설정:"
echo "다음 명령어로 크론탭에 추가하세요:"
echo "sudo crontab -e"
echo ""
echo "추가할 내용:"
echo "0 3 1 * * certbot renew --quiet && cp -L /etc/letsencrypt/live/$DOMAIN/* /home/ec2-user/ts-portal/ssl/live/$DOMAIN/ && cd /home/ec2-user/ts-portal && docker-compose restart nginx" 