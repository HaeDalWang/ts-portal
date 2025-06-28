# Auth Service

TS Portal 인증/인가 마이크로서비스

## 🚀 개발 시작

```bash
# 의존성 설치 (48ms에 완료!)
uv sync

# 개발 서버 실행
uv run uvicorn app.main:app --reload --port 8010
```

## 📡 API 문서
http://localhost:8010/docs

## 🎯 주요 기능
- JWT 토큰 발급/검증
- 사용자 로그인/로그아웃
- 권한 관리 (Admin, Power User, User)
- 토큰 갱신
- API Gateway 연동 