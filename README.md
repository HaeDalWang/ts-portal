# TS Portal

> Saltware CSG TS팀 내부 포털 사이트

## 개요

Vue 3 + FastAPI 마이크로서비스 기반의 팀 관리 포털입니다.

- 팀원 프로필 관리 (아이디/비밀번호 로그인)
- 고객사(MSP) 관리 및 담당자 배정
- 팀 일정 관리 (캘린더)
- 공지사항 관리
- AWS 소식 피드 (RSS)

## 기술 스택

### Frontend
- **Vue 3** + TypeScript
- **TailwindCSS** (UI 프레임워크)
- **Vite** (빌드 도구)
- **Pinia** (상태 관리)

### Backend
- **FastAPI** (Python 3.11)
- **UV** 패키지 매니저
- **PostgreSQL 15** (데이터베이스)
- **Kong 3.9.1** (API Gateway)
- **Redis** (캐싱)
- **Docker Compose** (컨테이너 오케스트레이션)

### 아키텍처
- **6개 마이크로서비스** (독립 배포)
- **Kong API Gateway** (통합 라우팅)
- **JWT 인증** (Bearer Token)
- **통일된 API 경로** (`/api/*` 패턴)

## 프로젝트 구조

```
ts-portal/
├── frontend/                    # Vue 3 프론트엔드 (현재 운영)
│   ├── src/
│   │   ├── components/         # 32개 컴포넌트 (모듈화)
│   │   │   ├── layout/        # 레이아웃 컴포넌트
│   │   │   ├── common/        # 공통 컴포넌트
│   │   │   ├── member/        # 팀원 관련
│   │   │   ├── customer/      # 고객사 관련
│   │   │   ├── calendar/      # 일정 관련
│   │   │   └── notice/        # 공지사항 관련
│   │   ├── views/             # 7개 페이지
│   │   ├── services/          # API 서비스 레이어
│   │   └── router/            # Vue Router 설정
│   └── package.json
│
├── frontend-new/                # Vue 3 경량화 버전 (개발 중)
│   └── 최적화된 새 프론트엔드 (포트: 5174)
│
├── services/                    # 마이크로서비스
│   ├── auth-service/          # 인증/인가 (8081)
│   ├── member-service/        # 팀원 관리 (8082)
│   ├── customer-service/      # 고객사 관리 (8083)
│   ├── calendar-service/      # 일정 관리 (8084)
│   ├── notice-service/        # 공지사항 (8085)
│   └── feeds-service/         # AWS 피드 (8086)
│
├── kong/                      # Kong API Gateway 설정
│   └── kong.yml              # 라우팅 규칙
│
├── db/                        # DB 초기화 스크립트
├── terraform/                 # AWS 인프라 코드
└── docker-compose.yml         # 전체 서비스 정의
```

## 🚀 실행 방법

### 전체 실행 (권장)
```bash
# 모든 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 서비스 상태 확인
docker-compose ps
```

### 개발 모드
```bash
# 인프라만 실행 (DB, Redis, Kong)
docker-compose up postgres redis kong -d

# 개별 서비스 개발
cd services/auth-service
uv sync
uv run uvicorn app.main:app --reload --port 8000

# 프론트엔드 개발
cd frontend
npm install
npm run dev
```

## 🌐 접속 URL

| 서비스 | URL | 설명 |
|--------|-----|------|
| **포털 사이트** | http://localhost:5173 | Vue 3 프론트엔드 (현재 운영) |
| **포털 사이트 (New)** | http://localhost:5174 | Vue 3 경량화 버전 (개발 중) |
| **API Gateway** | http://localhost:8000 | Kong 통합 API |
| **API 문서** | http://localhost:8081/docs | Auth Service API |
| **pgAdmin** | http://localhost:5050 | DB 관리 도구 |
| **Kong 관리** | http://localhost:8001 | Kong Admin API |

### 기본 로그인 정보
- **아이디**: `admin`
- **비밀번호**: `admin`

## 📊 API 경로 구조

모든 API가 `/api/*` 패턴으로 통일되었습니다:

| 서비스 | API 경로 | 설명 |
|--------|----------|------|
| Auth | `/api/auth/*` | 로그인, 토큰 관리 |
| Member | `/api/members/*` | 팀원 CRUD |
| Customer | `/api/customers/*` | 고객사 CRUD |
| Assignment | `/api/assignments/*` | 담당자 배정 |
| Calendar | `/api/events/*` | 일정 CRUD |
| Notice | `/api/notices/*` | 공지사항 CRUD |
| Feeds | `/api/feeds/*` | AWS 피드 |

### Kong 라우팅
```yaml
# Kong이 모든 요청을 적절한 마이크로서비스로 라우팅
# (모든 서비스는 내부적으로 8000 포트 사용)
/api/auth/login → auth-service:8000/api/auth/login
/api/members/   → member-service:8000/api/members/
/api/customers/ → customer-service:8000/api/customers/
/api/events/    → calendar-service:8000/api/events/
/api/notices/   → notice-service:8000/api/notices/
/api/feeds/     → feeds-service:8000/api/feeds/
```

## 🗄️ 데이터베이스

PostgreSQL 스키마별 테이블:

### member_schema
- `members`: 팀원 정보 (username, password, role)
- `skills`: 기술 스택

### customer_schema  
- `customers`: 고객사 정보
- `assignments`: 담당자 배정

### calendar_schema
- `events`: 일정 정보

### notice_schema
- `notices`: 공지사항

## 🛠️ 개발 환경 설정

### 사전 요구사항
- **Docker** & **Docker Compose**
- **Node.js 18+** (프론트엔드 개발 시)
- **UV** (백엔드 개발 시)

### 설치 및 실행
```bash
# UV 설치 (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 프로젝트 클론
git clone <repository-url>
cd ts-portal

# 전체 서비스 실행
docker-compose up -d

# 프론트엔드 접속
open http://localhost:5173
```

## 🔧 서비스 포트

| 서비스 | 포트 | 컨테이너명 | 상태 |
|--------|------|------------|------|
| **Kong Gateway** | 8000 | ts-portal-kong | ✅ 운영 |
| **Auth Service** | 8081 | ts-portal-auth-service | ✅ 운영 |
| **Member Service** | 8082 | ts-portal-member-service | ✅ 운영 |
| **Customer Service** | 8083 | ts-portal-customer-service | ✅ 운영 |
| **Calendar Service** | 8084 | ts-portal-calendar-service | ✅ 운영 |
| **Notice Service** | 8085 | ts-portal-notice-service | ✅ 운영 |
| **Feeds Service** | 8086 | ts-portal-feeds-service | ✅ 운영 |
| **PostgreSQL** | 5432 | ts-portal-postgres | ✅ 운영 |
| **Redis** | 6379 | ts-portal-redis | ✅ 운영 |
| **pgAdmin** | 5050 | ts-portal-pgadmin | ✅ 운영 |

## 🔄 최근 주요 업데이트

### v1.3.0 (2025-01-02)
- ✅ **서비스 포트 정리** (8081~8086으로 순차 배치)
- ✅ **내부 포트 통일** (모든 서비스 내부 8000 포트 사용)
- ✅ **frontend-new 개발 시작** (경량화된 새 버전)

### v1.2.0 (2025-06-29)
- ✅ **Kong API Gateway 도입** (기존 자체 개발 API Gateway 대체)
- ✅ **API 경로 통일** (모든 서비스 `/api/*` 패턴)
- ✅ **로그인 시스템 개선** (이메일 → 아이디 로그인)
- ✅ **프론트엔드 컴포넌트 모듈화** (4개 거대 파일 → 32개 작은 컴포넌트)
- ✅ **코드 정리 및 최적화** (중복 파일 제거, 구조 개선)

### 주요 기능
- 🔐 JWT 기반 인증 시스템
- 👥 팀원 프로필 관리 (기술스택, 권한)
- 🏢 고객사 관리 및 담당자 자동 배정
- 📅 팀 캘린더 (일정 공유)
- 📢 공지사항 시스템
- 📰 AWS 최신 소식 피드

---

**Created by**: Seungdo Bae (TS Team)  
**Contact**: Saltware CSG  
**Version**: 1.3.0 (Port Standardization)
