# TS Portal

> Saltware CSG TS팀 내부 포털 사이트

## 개요

Vue 3 + FastAPI 마이크로서비스 기반의 팀 관리 포털입니다.

- 팀원 프로필 관리
- 고객사(MSP) 관리
- 팀 일정 관리
- 공지사항 관리
- AWS 소식 피드

## 기술 스택

### Frontend
- Vue 3 + TypeScript
- TailwindCSS
- Vite

### Backend
- FastAPI (Python 3.11)
- UV 패키지 매니저
- PostgreSQL 15
- Docker Compose

### 아키텍처
- 6개 마이크로서비스
- API Gateway
- JWT 인증

## 프로젝트 구조

```
ts-portal/
├── frontend/                    # Vue 3 프론트엔드
│   ├── src/
│   │   ├── components/         # 컴포넌트
│   │   ├── views/             # 페이지
│   │   ├── services/          # API 서비스
│   │   └── router/            # 라우터
│   └── package.json
│
├── services/                    # 마이크로서비스
│   ├── api-gateway/           # API Gateway (8080)
│   ├── auth-service/          # 인증 (8010)
│   ├── member-service/        # 팀원 관리 (8001)
│   ├── customer-service/      # 고객사 관리 (8002)
│   ├── calendar-service/      # 일정 관리 (8003)
│   ├── notice-service/        # 공지사항 (8004)
│   └── feeds-service/         # AWS 피드 (8000)
│
├── db/                        # DB 초기화 스크립트
├── terraform/                 # 인프라 코드
└── docker-compose.yml         # 컨테이너 설정
```

## 실행 방법

### 전체 실행
```bash
docker-compose up -d
```

### 개발 모드
```bash
# 인프라만 실행
docker-compose up postgres redis -d

# 개별 서비스 개발
cd services/member-service
uv sync
uv run uvicorn app.main:app --reload --port 8001

# 프론트엔드
cd frontend
npm install
npm run dev
```

## 접속 URL

- **포털**: http://localhost:5173
- **API Gateway**: http://localhost:8080
- **API 문서**: http://localhost:8080/docs
- **pgAdmin**: http://localhost:5050

## 데이터베이스

PostgreSQL 스키마:
- `member_schema`: 팀원 정보
- `customer_schema`: 고객사 정보
- `calendar_schema`: 일정 정보
- `notice_schema`: 공지사항

## 환경 설정

### 사전 요구사항
- Docker & Docker Compose
- Node.js 18+ (개발 시)
- UV (개발 시)

### 개발 환경
```bash
# UV 설치
curl -LsSf https://astral.sh/uv/install.sh | sh

# 프로젝트 클론
git clone <repository-url>
cd ts-portal

# 실행
docker-compose up -d
```

## 서비스 포트

| 서비스 | 포트 | 설명 |
|--------|------|------|
| Frontend | 5173 | Vue 3 개발 서버 |
| API Gateway | 8080 | 통합 라우팅 |
| Auth Service | 8010 | 인증/인가 |
| Member Service | 8001 | 팀원 관리 |
| Customer Service | 8002 | 고객사 관리 |
| Calendar Service | 8003 | 일정 관리 |
| Notice Service | 8004 | 공지사항 |
| Feeds Service | 8000 | AWS 피드 |
| PostgreSQL | 5432 | 데이터베이스 |
| pgAdmin | 5050 | DB 관리 도구 |

---

**Created by**: Seungdo Bae (TS Team)  
**Contact**: Saltware CSG
