#!/bin/bash

echo "🔄 TS-Portal 서비스 재빌드 및 재시작 스크립트"
echo "================================================"

# 색상 정의
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. 기존 컨테이너 중지 및 제거
echo -e "\n${YELLOW}1. 기존 컨테이너 중지 및 제거...${NC}"
docker-compose down

# 2. 이미지 제거 (선택사항)
echo -e "\n${YELLOW}2. 기존 이미지 제거...${NC}"
docker-compose down --rmi local

# 3. 서비스 재빌드
echo -e "\n${YELLOW}3. 모든 서비스 재빌드...${NC}"
docker-compose build --no-cache

# 4. 서비스 시작
echo -e "\n${YELLOW}4. 서비스 시작...${NC}"
docker-compose up -d

# 5. 상태 확인
echo -e "\n${YELLOW}5. 서비스 상태 확인...${NC}"
sleep 5  # 서비스가 시작되길 기다림
docker-compose ps

# 6. 헬스 체크
echo -e "\n${YELLOW}6. 서비스 헬스 체크...${NC}"
services=("auth:8081" "member:8082" "customer:8083" "calendar:8084" "notice:8085" "feeds:8086")

for service in "${services[@]}"; do
    IFS=':' read -r name port <<< "$service"
    echo -n "- ${name}-service (${port}): "
    
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:${port}/health | grep -q "200"; then
        echo -e "${GREEN}✓ Healthy${NC}"
    else
        echo -e "${RED}✗ Unhealthy${NC}"
    fi
done

# 7. Kong Gateway 확인
echo -e "\n${YELLOW}7. Kong Gateway 상태...${NC}"
echo -n "- Kong Gateway (8000): "
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/status | grep -q "200"; then
    echo -e "${GREEN}✓ Running${NC}"
else
    echo -e "${RED}✗ Not Running${NC}"
fi

echo -e "\n${GREEN}✅ 완료!${NC}"
echo "================================================"
echo "접속 URL:"
echo "- 포털: http://localhost:5173"
echo "- API Gateway: http://localhost:8000"
echo "- API 문서: http://localhost:8081/docs"
echo "- pgAdmin: http://localhost:5050" 