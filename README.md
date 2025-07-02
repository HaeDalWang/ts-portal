# TS Portal

> Saltware CSG TS팀 내부 포털 사이트

## 개요

Vue 3 + FastAPI 마이크로서비스 기반의 팀 관리 포털입니다.

- 팀원 프로필 관리 (아이디/비밀번호 로그인)
- 고객사(MSP) 관리 및 담당자 배정
- 팀 일정 관리 (캘린더) - **✅ 완전 안정화**
- 공지사항 관리 
- AWS 소식 피드 (RSS)

## 기술 스택

### Frontend
- **Vue 3** + TypeScript
- **TailwindCSS** (UI 프레임워크)
- **Vite** (빌드 도구)
- **Vue Router** (라우팅)

### Backend
- **FastAPI** (Python 3.11)
- **UV** 패키지 매니저
- **SQLAlchemy** + **Pydantic** (ORM/Validation)
- **PostgreSQL 15** (데이터베이스)
- **Kong 3.9.1** (API Gateway)
- **Redis** (캐싱)
- **Docker Compose** (컨테이너 오케스트레이션)

### 아키텍처
- **6개 마이크로서비스** (독립 배포)
- **Kong API Gateway** (통합 라우팅, trailing slash 처리)
- **JWT 인증** (Bearer Token)
- **통일된 API 경로** (`/api/*` 패턴)

## 프로젝트 구조

```
ts-portal/
├── frontend/                    # Vue 3 프론트엔드 (기존)
│   ├── src/
│   │   ├── components/         # 32개 컴포넌트 (모듈화)
│   │   ├── views/             # 7개 페이지
│   │   ├── services/          # API 서비스 레이어
│   │   └── router/            # Vue Router 설정
│   └── package.json
│
├── frontend-new/                # Vue 3 최신 버전 (🆕 활성 개발)
│   ├── src/
│   │   ├── components/        # 완전 재구성된 컴포넌트
│   │   ├── views/             # 최적화된 페이지
│   │   ├── services/          # 개선된 API 서비스
│   │   ├── composables/       # Vue 3 Composition API
│   │   └── types/             # TypeScript 타입 정의
│   └── 포트: 5174 (개발 서버)
│
├── services/                    # 마이크로서비스
│   ├── auth-service/          # 인증/인가 (8081)
│   ├── member-service/        # 팀원 관리 (8082)
│   ├── customer-service/      # 고객사 관리 (8083)
│   ├── calendar-service/      # 일정 관리 (8084) ✅ 완전 안정화
│   ├── notice-service/        # 공지사항 (8085)
│   └── feeds-service/         # AWS 피드 (8086)
│
├── kong/                      # Kong API Gateway 설정
│   └── kong.yml              # 라우팅 규칙 (trailing slash 처리)
│
├── db/                        # DB 초기화 스크립트
├── terraform/                 # AWS 인프라 코드
├── TROUBLESHOOTING.md         # 🆕 문제 해결 가이드
└── docker-compose.yml         # 전체 서비스 정의
```

## 🚀 실행 방법

### 전체 실행 (권장)
```bash
# 모든 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 특정 서비스 로그만 확인
docker-compose logs -f calendar-service

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

# 프론트엔드 개발 (최신 버전)
cd frontend-new
npm install
npm run dev
```

### 서비스 재시작 (문제 발생 시)
```bash
# 특정 서비스만 재시작
docker-compose restart calendar-service

# 완전 재구성 (캐시 제거)
docker-compose stop calendar-service
docker-compose rm -f calendar-service
docker-compose build calendar-service
docker-compose up -d calendar-service

# Kong 설정 변경 시
docker-compose restart kong
```

## 🌐 접속 URL

| 서비스 | URL | 설명 |
|--------|-----|------|
| **포털 사이트 (기존)** | http://localhost:5173 | Vue 3 프론트엔드 |
| **🆕 포털 사이트 (최신)** | http://localhost:5174 | Vue 3 최신 버전 (권장) |
| **API Gateway** | http://localhost:8000 | Kong 통합 API |
| **API 문서** | http://localhost:8081/docs | Auth Service API |
| **pgAdmin** | http://localhost:5050 | DB 관리 도구 |
| **Kong 관리** | http://localhost:8001 | Kong Admin API |

### 기본 로그인 정보
- **아이디**: `admin`
- **비밀번호**: `admin123!`

## 📊 API 경로 구조

모든 API가 `/api/*` 패턴으로 통일되었습니다:

| 서비스 | API 경로 | 설명 | 상태 |
|--------|----------|------|------|
| Auth | `/api/auth/*` | 로그인, 토큰 관리 | ✅ 안정 |
| Member | `/api/members/*` | 팀원 CRUD | ✅ 안정 |
| Customer | `/api/customers/*` | 고객사 CRUD | ✅ 안정 |
| Assignment | `/api/assignments/*` | 담당자 배정 | ✅ 안정 |
| Calendar | `/api/events/*` | 일정 CRUD | ✅ **완전 안정화** |
| Notice | `/api/notices/*` | 공지사항 CRUD | ✅ 안정 |
| Feeds | `/api/feeds/*` | AWS 피드 | ✅ 안정 |

### Kong 라우팅 (개선됨)
```yaml
# Kong이 모든 요청을 적절한 마이크로서비스로 라우팅
# trailing slash 리다이렉트 문제 해결됨
/api/auth/login → auth-service:8000/api/auth/login
/api/members/   → member-service:8000/api/members/
/api/customers/ → customer-service:8000/api/customers/
/api/events/    → calendar-service:8000/api/events/   # ✅ 리다이렉트 문제 해결
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

### calendar_schema ✅ 최신 스키마
- `events`: 일정 정보
  - `attendees` (JSONB) - 참가자 정보
  - `is_all_day` (Boolean) - 종일 일정 여부
  - `end_time` (NOT NULL) - 종료 시간 필수

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

# 최신 프론트엔드 접속 (권장)
open http://localhost:5174
```

## 🔧 서비스 포트

| 서비스 | 포트 | 컨테이너명 | 상태 |
|--------|------|------------|------|
| **Kong Gateway** | 8000 | ts-portal-kong | ✅ 운영 |
| **Auth Service** | 8081 | ts-portal-auth-service | ✅ 운영 |
| **Member Service** | 8082 | ts-portal-member-service | ✅ 운영 |
| **Customer Service** | 8083 | ts-portal-customer-service | ✅ 운영 |
| **Calendar Service** | 8084 | ts-portal-calendar-service | ✅ **완전 안정화** |
| **Notice Service** | 8085 | ts-portal-notice-service | ✅ 운영 |
| **Feeds Service** | 8086 | ts-portal-feeds-service | ✅ 운영 |
| **PostgreSQL** | 5432 | ts-portal-postgres | ✅ 운영 |
| **Redis** | 6379 | ts-portal-redis | ✅ 운영 |
| **pgAdmin** | 5050 | ts-portal-pgadmin | ✅ 운영 |

## 🔄 최근 주요 업데이트

### v1.4.0 (2025-07-02) - Calendar Service 완전 안정화
- ✅ **Calendar Service 완전 안정화** 
  - SQLAlchemy 모델과 DB 스키마 100% 일치
  - `participants` → `attendees` (JSONB) 필드 변경
  - `all_day` → `is_all_day` 필드 변경  
  - `end_time` NOT NULL 강제 적용
- ✅ **Kong Gateway trailing slash 문제 해결**
  - request-transformer 플러그인 적용
  - 리다이렉트 오류 완전 해결
- ✅ **Pydantic 스키마 최적화**
  - computed_field 제거하고 service 레이어에서 직접 처리
  - 하위 호환성 유지
- ✅ **frontend-new 활성 개발**
  - Vue 3 Composition API 적용
  - TypeScript 타입 안정성 개선
  - 모든 기능 정상 작동 확인

### v1.3.0 (2025-01-02)
- ✅ **서비스 포트 정리** (8081~8086으로 순차 배치)
- ✅ **내부 포트 통일** (모든 서비스 내부 8000 포트 사용)
- ✅ **frontend-new 개발 시작** (경량화된 새 버전)

### v1.2.0 (2025-06-29)
- ✅ **Kong API Gateway 도입** (기존 자체 개발 API Gateway 대체)
- ✅ **API 경로 통일** (모든 서비스 `/api/*` 패턴)
- ✅ **로그인 시스템 개선** (이메일 → 아이디 로그인)
- ✅ **프론트엔드 컴포넌트 모듈화** (4개 거대 파일 → 32개 작은 컴포넌트)

### 주요 기능
- 🔐 JWT 기반 인증 시스템
- 👥 팀원 프로필 관리 (기술스택, 권한)
- 🏢 고객사 관리 및 담당자 자동 배정
- 📅 **팀 캘린더** (일정 공유) - **완전 안정화**
- 📢 공지사항 시스템 (우선순위별 권한)
- 📰 AWS 최신 소식 피드

## ⚠️ 문제 해결

문제가 발생하면 다음 문서를 참조하세요:
- **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)** - 상세한 문제 해결 가이드

### 빠른 문제 해결
```bash
# 서비스 재시작
docker-compose restart <service-name>

# 로그 확인
docker-compose logs -f <service-name>

# 완전 재구성 (심각한 문제 시)
docker-compose stop <service-name>
docker-compose rm -f <service-name>  
docker-compose build <service-name>
docker-compose up -d <service-name>
```

---

**Created by**: Seungdo Bae (TS Team)  
**Contact**: Saltware CSG  
**Version**: 1.4.0 (Calendar Service Stabilization)  
**Last Updated**: 2025-07-02
