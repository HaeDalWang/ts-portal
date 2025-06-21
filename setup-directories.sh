#!/bin/bash

# TS Portal 디렉토리 구조 설정 스크립트
# 실행 위치: /home/ec2-user/ts-portal

set -e

echo "🏗️ TS Portal 디렉토리 구조 설정 중..."

# 기본 디렉토리 생성
mkdir -p data/sqlite
mkdir -p data/redis
mkdir -p logs/nginx
mkdir -p logs/honeybox
mkdir -p logs/ts-portal-db
mkdir -p ssl
mkdir -p nginx

echo "📁 생성된 디렉토리 구조:"
tree -L 3 . || ls -la

echo ""
echo "📋 디렉토리 설명:"
echo "  data/sqlite/     - SQLite 데이터베이스 파일"
echo "  data/redis/      - Redis 데이터 파일"
echo "  logs/nginx/      - Nginx 액세스/에러 로그"
echo "  logs/honeybox/   - HoneyBox 애플리케이션 로그"
echo "  logs/ts-portal-db/ - TS Portal DB 애플리케이션 로그"
echo "  ssl/             - SSL 인증서 파일 (Let's Encrypt)"
echo "  nginx/           - Nginx 설정 파일"

echo ""
echo "🔧 권한 설정 중..."
# 로그 디렉토리 권한 설정
chmod -R 755 logs/
chmod -R 755 data/

echo ""
echo "✅ 디렉토리 구조 설정 완료!"
echo ""
echo "📝 다음 단계:"
echo "1. nginx/nginx.conf 파일에서 도메인명 수정"
echo "2. Let's Encrypt 인증서 발급"
echo "3. docker-compose up -d 실행" 