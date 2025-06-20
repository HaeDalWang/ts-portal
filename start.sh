#!/bin/bash

# logs 디렉토리 생성
mkdir -p logs

# frontend 실행 (포트: 5173)
echo "[INFO] frontend(dev) 실행... (http://localhost:5173)"
cd frontend
npm install
touch ../logs/frontend.log
nohup npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# honeybox 실행 (포트: 8000)
echo "[INFO] honeybox(FastAPI) 실행... (http://localhost:8000)"
cd honeybox
source venv/bin/activate
pip install -r requirements.txt
touch ../logs/honeybox.log
nohup python main.py > ../logs/honeybox.log 2>&1 &
HONEYBOX_PID=$!
deactivate
cd ..

# ts-portal-db 실행 (포트: 8001)
echo "[INFO] ts-portal-db(FastAPI) 실행... (http://localhost:8001)"
cd ts-portal-db
# Python 가상환경이 있다면 활성화 (선택적)
if [ -d "venv" ]; then
    source venv/bin/activate
fi
pip install -r requirements.txt
touch ../logs/ts-portal-db.log
nohup python3 main.py > ../logs/ts-portal-db.log 2>&1 &
TS_PORTAL_DB_PID=$!
if [ -d "venv" ]; then
    deactivate
fi
cd ..

# PID 출력
echo "[INFO] frontend PID: $FRONTEND_PID"
echo "[INFO] honeybox PID: $HONEYBOX_PID"
echo "[INFO] ts-portal-db PID: $TS_PORTAL_DB_PID"

echo "[INFO] 모든 서비스가 백그라운드에서 실행 중입니다."
echo "[INFO] 서비스 주소:"
echo "  - Frontend: http://localhost:5173"
echo "  - HoneyBox API: http://localhost:8000"
echo "  - TS Portal DB API: http://localhost:8001"
echo "  - TS Portal DB API 문서: http://localhost:8001/docs" 