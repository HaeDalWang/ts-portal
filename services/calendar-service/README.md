# Calendar Service

TS Portal 팀 일정 관리 마이크로서비스

## 🚀 개발 시작

```bash
# 의존성 설치 (48ms에 완료!)
uv sync

# 개발 서버 실행
uv run uvicorn app.main:app --reload --port 8003
```

## 📡 API 문서
http://localhost:8003/docs

## 🎯 주요 기능
- 팀 일정 관리
- 7가지 이벤트 타입 (휴가, 재택, 출장, 프로젝트, 교육, 회의, 기타)
- FullCalendar 형식 지원
- 팀원별 동적 색상 생성
- 실시간 통계 및 필터링
