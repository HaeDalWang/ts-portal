# Notice Service

TS Portal 공지사항 관리 마이크로서비스

## 🚀 개발 시작

```bash
# 의존성 설치 (48ms에 완료!)
uv sync

# 개발 서버 실행
uv run uvicorn app.main:app --reload --port 8004
```

## 📡 API 문서
http://localhost:8004/docs

## 🎯 주요 기능
- 공지사항 CRUD
- 고정 공지사항 관리
- 검색 및 필터링
- 권한 기반 접근 제어
- 통계 및 페이지네이션
