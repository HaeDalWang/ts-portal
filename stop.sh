#!/bin/bash

# frontend(Vue) 종료 (포트 5173)
FRONTEND_PID=$(lsof -ti:5173)
if [ -n "$FRONTEND_PID" ]; then
  echo "[INFO] frontend(Vue) 프로세스 종료 중... (PID: $FRONTEND_PID)"
  kill $FRONTEND_PID
  sleep 1
  if ps -p $FRONTEND_PID > /dev/null; then
    echo "[WARN] frontend 프로세스가 완전히 종료되지 않았습니다. 강제 종료 시도..."
    kill -9 $FRONTEND_PID
  fi
  echo "[INFO] frontend(Vue) 종료 완료."
else
  echo "[INFO] frontend(Vue) 실행 중인 프로세스가 없습니다."
fi

# honeybox(FastAPI) 종료 (포트 8000)
HONEYBOX_PID=$(lsof -ti:8000)
if [ -n "$HONEYBOX_PID" ]; then
  echo "[INFO] honeybox(FastAPI) 프로세스 종료 중... (PID: $HONEYBOX_PID)"
  kill $HONEYBOX_PID
  sleep 1
  if ps -p $HONEYBOX_PID > /dev/null; then
    echo "[WARN] honeybox 프로세스가 완전히 종료되지 않았습니다. 강제 종료 시도..."
    kill -9 $HONEYBOX_PID
  fi
  echo "[INFO] honeybox(FastAPI) 종료 완료."
else
  echo "[INFO] honeybox(FastAPI) 실행 중인 프로세스가 없습니다."
fi

# ts-portal-db(FastAPI) 종료 (포트 8001)
TS_PORTAL_DB_PID=$(lsof -ti:8001)
if [ -n "$TS_PORTAL_DB_PID" ]; then
  echo "[INFO] ts-portal-db(FastAPI) 프로세스 종료 중... (PID: $TS_PORTAL_DB_PID)"
  kill $TS_PORTAL_DB_PID
  sleep 1
  if ps -p $TS_PORTAL_DB_PID > /dev/null; then
    echo "[WARN] ts-portal-db 프로세스가 완전히 종료되지 않았습니다. 강제 종료 시도..."
    kill -9 $TS_PORTAL_DB_PID
  fi
  echo "[INFO] ts-portal-db(FastAPI) 종료 완료."
else
  echo "[INFO] ts-portal-db(FastAPI) 실행 중인 프로세스가 없습니다."
fi

echo "[INFO] 모든 서비스 종료 처리 완료." 