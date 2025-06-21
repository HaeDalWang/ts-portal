#!/bin/bash

# TS Portal Frontend S3 배포 스크립트
set -e

echo "🚀 TS Portal Frontend 배포를 시작합니다..."

# 환경 변수 설정
S3_BUCKET="ts.seungdobae.com"
CLOUDFRONT_DISTRIBUTION_ID="E3CMX2PEQAEFNT"  # CloudFront 배포 ID

# 빌드 확인
if [ ! -d "dist" ]; then
    echo "❌ dist 폴더가 없습니다. 먼저 빌드를 실행하세요:"
    echo "   npm run build:prod"
    exit 1
fi

echo "📁 빌드 파일 확인 완료"

# S3 업로드
echo "📤 S3에 파일 업로드 중..."

# 정적 자원 (CSS, JS, 이미지) - 1년 캐시
aws s3 sync dist/ s3://$S3_BUCKET --delete \
  --cache-control "public, max-age=31536000" \
  --exclude "*.html" \
  --exclude "*.txt" \
  --exclude "*.json"

# HTML 파일 - 캐시 없음
aws s3 sync dist/ s3://$S3_BUCKET \
  --cache-control "no-cache, no-store, must-revalidate" \
  --include "*.html"

# 기타 파일 (manifest.json, robots.txt 등)
aws s3 sync dist/ s3://$S3_BUCKET \
  --cache-control "public, max-age=86400" \
  --include "*.txt" \
  --include "*.json" \
  --exclude "*.html"

echo "✅ S3 업로드 완료!"

# CloudFront 캐시 무효화 (선택적)
if [ ! -z "$CLOUDFRONT_DISTRIBUTION_ID" ]; then
    echo "🔄 CloudFront 캐시 무효화 중..."
    aws cloudfront create-invalidation \
      --distribution-id $CLOUDFRONT_DISTRIBUTION_ID \
      --paths "/*" \
      --no-cli-pager
    echo "✅ CloudFront 캐시 무효화 완료!"
fi

echo ""
echo "🎉 배포 완료!"
echo "🌐 사이트 URL: https://$S3_BUCKET"
echo ""
echo "📊 배포 통계:"
aws s3 ls s3://$S3_BUCKET --recursive --human-readable --summarize | tail -2 