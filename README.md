# TS Portal 🚀

> **Saltware CSG - TS팀 통합 포털 사이트**  
> Vue 3 + TypeScript + FastAPI 마이크로서비스로 구축된 현대적인 팀 관리 플랫폼

![Vue 3](https://img.shields.io/badge/Vue-3.x-4FC08D?style=flat-square&logo=vue.js&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat-square&logo=typescript&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=flat-square&logo=fastapi&logoColor=white)
![UV](https://img.shields.io/badge/UV-Rust--based-DE3910?style=flat-square&logo=rust&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat-square&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)

## 📋 목차

- [프로젝트 개요](#-프로젝트-개요)
- [주요 기능](#-주요-기능)
- [마이크로서비스 아키텍처](#-마이크로서비스-아키텍처)
- [기술 스택](#-기술-스택)
- [프로젝트 구조](#-프로젝트-구조)
- [설치 및 실행](#-설치-및-실행)
- [API 문서](#-api-문서)
- [배포](#-배포)
- [기여하기](#-기여하기)

## 🎯 프로젝트 개요

TS Portal은 Saltware CSG TS팀을 위한 **완전한 마이크로서비스 기반** 통합 관리 플랫폼입니다. 팀원 관리, 고객사 관리, 일정 관리, 그리고 최신 AWS 소식까지 한 곳에서 확인할 수 있는 올인원 솔루션을 제공합니다.

### 🌟 핵심 가치
- **현대적 아키텍처**: 완전한 마이크로서비스 + API Gateway 구조
- **극단적 성능**: UV 기반 Python 환경으로 10-100배 빠른 의존성 관리
- **확장성**: 서비스별 독립 배포 및 스케일링 가능
- **개발자 경험**: 48ms 의존성 설치, 2-3초 서비스 시작

### 🏆 **MSA 전환 완료!** (2025.06)
- ✅ **6개 마이크로서비스** 완전 분리
- ✅ **API Gateway** 통합 라우팅
- ✅ **UV 기반** 모든 서비스 현대화
- ✅ **PostgreSQL** 스키마 분리
- ✅ **Docker Compose** 통합 오케스트레이션

## ✨ 주요 기능

### 🏠 대시보드 홈
- **6개 핵심 카드**: AWS 소식, TS 공지사항, 점심 추천, 팀원 프로필, 팀 대시보드, MSP 관리
- **반응형 그리드 레이아웃**: 모든 디바이스에서 최적화된 경험
- **마이크로서비스 통합**: API Gateway를 통한 통합 데이터 제공

### 📰 AWS 소식 (Feeds Service) - **🆕 경량화 완료!**
- **극단적 경량화**: 600+ 라인 → 183라인 (3배 감소)
- **단일 파일 구조**: 복잡한 모듈 구조 → 단일 main.py
- **3개 핵심 피드**: AWS Blog, AWS What's New, AWS Security Blog
- **비동기 처리**: httpx + feedparser로 고성능 RSS 수집
- **2-3초 시작**: UV 최적화로 극단적 시작 속도

### 👥 팀원 프로필 관리 (Member Service)
- **권한 시스템**: Admin, Power User, User 역할 기반 접근 제어
- **내 프로필 편집**: 사용자가 자신의 연락처, 기술 스택 등 직접 수정
- **듀얼 뷰 모드**: 카드 뷰 / 테이블 뷰 전환 가능
- **고급 검색**: 이름, 이메일, 직급, 기술스택 통합 검색
- **실시간 통계**: 재직률, 팀 구성 현황 실시간 표시

### 🏢 MSP 고객사 관리 (Customer Service)
- **고객사 데이터베이스**: 담당자, 계약 정보, 연락처 통합 관리
- **담당자 배정**: 주/부 담당자를 팀원 중에서 선택하여 배정
- **기술지원등급**: Standard, Advanced, Enterprise 등급으로 계약 관리
- **듀얼 뷰 모드**: 카드 뷰 / 테이블 뷰 (기본값: 테이블)
- **검색 및 필터**: 다양한 조건으로 고객사 검색

### 📅 팀 대시보드 (Calendar Service)
- **FullCalendar 통합**: 월/주/일 뷰 지원
- **7가지 이벤트 타입**: 휴가, 재택, 출장, 프로젝트, 교육, 회의, 기타
- **팀원별 색상 구분**: 동적 색상 생성 알고리즘 (HSL 기반)
- **실시간 통계**: 오늘 일정, 이번 주 일정 등
- **고급 필터링**: 팀원별, 이벤트 타입별 필터

### 📢 공지사항 (Notice Service)
- **권한 기반 작성**: Admin, Power User만 작성 가능
- **마크다운 지원**: 풍부한 텍스트 편집
- **검색 및 필터링**: 제목, 내용, 작성자 통합 검색
- **페이지네이션**: 대용량 데이터 효율적 처리

### 🔐 인증 시스템 (Auth Service)
- **JWT 토큰**: 무상태 인증 시스템
- **API Gateway 통합**: 모든 요청 자동 인증 처리
- **권한 관리**: 서비스별 세밀한 권한 제어

## 🏗️ 마이크로서비스 아키텍처

### **현재 상태 (MSA 완료!)** ✅
```
┌─────────────────────────────────────────────────────────┐
│                 Vue 3 Frontend (5173)                  │
│            TypeScript + TailwindCSS                     │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                API Gateway (8080)                      │
│         FastAPI + JWT 인증 + 라우팅 통합                │
└─────────────────────┬───────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
  ┌─────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐
  │Auth Service│ │Member Svc │ │Customer   │
  │   (8010)   │ │  (8001)   │ │Svc (8002) │
  │  UV 기반   │ │  UV 기반  │ │  UV 기반  │
  └───────────┘ └───────────┘ └───────────┘
        
  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
  │Calendar Svc │ │ Notice Svc  │ │ Feeds Svc   │
  │   (8003)    │ │   (8004)    │ │   (8000)    │
  │  UV 기반    │ │  UV 기반    │ │  UV 기반    │
  └─────────────┘ └─────────────┘ └─────────────┘
                      │
              ┌───────▼───────┐
              │ PostgreSQL 15 │
              │  (스키마 분리) │
              └───────────────┘
```

### 서비스별 책임 분리
- **🔐 Auth Service (8010)**: JWT 토큰 발급/검증, 로그인/로그아웃
- **👥 Member Service (8001)**: 팀원 프로필, 권한 관리, 기술스택
- **🏢 Customer Service (8002)**: 고객사 정보, 담당자 배정
- **📅 Calendar Service (8003)**: 팀 일정, 이벤트 관리, 통계
- **📢 Notice Service (8004)**: 공지사항 CRUD, 검색, 필터링
- **📰 Feeds Service (8000)**: AWS 소식 수집, RSS 파싱

### API Gateway 기능
- **통합 라우팅**: `/api/{service}/*` 패턴으로 자동 라우팅
- **JWT 인증**: 모든 요청 자동 인증 처리
- **헬스체크**: 모든 서비스 상태 실시간 모니터링
- **Prometheus 메트릭**: 성능 지표 수집
- **Rate Limiting**: API 호출 제한

## 🛠 기술 스택

### Frontend
- **Vue 3** - Composition API, TypeScript 지원
- **Vue Router** - SPA 라우팅 관리
- **TypeScript** - 타입 안전성과 개발 생산성
- **TailwindCSS** - 유틸리티 퍼스트 CSS 프레임워크
- **Axios** - HTTP 클라이언트 (API 통신)
- **FullCalendar** - 고급 달력 컴포넌트
- **Vite** - 빠른 개발 서버 및 빌드 도구

### Backend - **🚀 UV 기반 현대화 완료!**

#### ⚡ **UV (Ultra-fast Python Package Manager)**
- **속도**: pip 대비 **10-100배 빠름** (48ms에 의존성 설치 완료!)
- **Rust 기반**: 네이티브 성능으로 극단적 최적화
- **현대적**: pyproject.toml + uv.lock 사용
- **통합 도구**: 가상환경, 패키지 관리, 실행을 하나로

#### 🔧 **모든 서비스 UV 통일**
```bash
# 모든 서비스가 동일한 현대적 구조
├── pyproject.toml       # UV 프로젝트 설정
├── uv.lock             # 정확한 의존성 버전 고정
├── Dockerfile          # UV 기반 컨테이너
└── app/                # FastAPI 애플리케이션
```

#### 🎯 **마이크로서비스별 기술 스택**
- **FastAPI** - 고성능 비동기 웹 프레임워크
- **Pydantic** - 데이터 검증 및 직렬화
- **SQLAlchemy** - ORM 및 데이터베이스 추상화
- **httpx** - 비동기 HTTP 클라이언트
- **JWT** - 무상태 인증 토큰
- **feedparser** - RSS 파싱 (Feeds Service)

### Database & Infrastructure
- **PostgreSQL 15** - 메인 데이터베이스 (스키마 분리)
- **Redis** - 캐싱 및 세션 저장소
- **Docker & Docker Compose** - 컨테이너화 및 오케스트레이션
- **pgAdmin** - 데이터베이스 관리 도구

### 클라우드 & 배포
- **AWS ECS Fargate** - 컨테이너 오케스트레이션
- **Application Load Balancer** - 로드 밸런싱
- **Route 53** - DNS 관리
- **CloudWatch** - 모니터링 및 로깅
- **Terraform** - Infrastructure as Code

## 📁 프로젝트 구조

### **MSA 완료 후 구조** ✅
```
ts-portal/
├── 🎨 frontend/                 # Vue 3 + TypeScript
│   ├── src/
│   │   ├── components/          # 재사용 컴포넌트
│   │   ├── views/              # 페이지 컴포넌트
│   │   ├── services/           # API 서비스 레이어
│   │   └── router/             # Vue Router 설정
│   └── package.json
│
├── 🔌 services/                 # 마이크로서비스들 ✅
│   ├── api-gateway/            # 🚪 API Gateway (8080)
│   │   ├── app/
│   │   ├── pyproject.toml      # UV 기반
│   │   └── uv.lock
│   ├── auth-service/           # 🔐 인증/인가 (8010)
│   │   ├── app/
│   │   ├── pyproject.toml      # UV 기반
│   │   └── uv.lock
│   ├── member-service/         # 👥 팀원 관리 (8001)
│   │   ├── app/
│   │   ├── pyproject.toml      # UV 기반
│   │   └── uv.lock
│   ├── customer-service/       # 🏢 고객사 관리 (8002)
│   │   ├── app/
│   │   ├── pyproject.toml      # UV 기반
│   │   └── uv.lock
│   ├── calendar-service/       # 📅 일정 관리 (8003)
│   │   ├── app/
│   │   ├── pyproject.toml      # UV 기반
│   │   └── uv.lock
│   ├── notice-service/         # 📢 공지사항 (8004)
│   │   ├── app/
│   │   ├── pyproject.toml      # UV 기반
│   │   └── uv.lock
│   └── feeds-service/          # 📰 AWS 소식 (8000)
│       ├── app/
│       │   └── main.py         
│       ├── pyproject.toml      # UV 기반
│       └── uv.lock
│
├── 📂 db/                      # 데이터베이스 관련
│   └── init/                   # PostgreSQL 초기화 스크립트
│       └── 01_create_schemas.sql
│
├── 🚀 terraform/               # Infrastructure as Code
└── 📜 Docker 설정 파일들
    └── docker-compose.yml      # 통합 오케스트레이션
```

### 🗄️ **PostgreSQL 스키마 분리**
```sql
-- 서비스별 논리적 스키마 분리
├── member_schema
│   └── members              # 팀원 정보
├── customer_schema
│   ├── customers           # 고객사 정보
│   └── assignments         # 담당 배정
├── calendar_schema
│   └── events              # 팀 일정
└── notice_schema
    └── notices             # 공지사항
```

## 🚀 설치 및 실행

### 사전 요구사항
- **Docker & Docker Compose** (필수)
- **UV** (개발 시) - `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Node.js** 18+ (Frontend 개발 시)

### 1. **전체 MSA 스택 실행** (권장) 🚀
```bash
# 🚀 모든 마이크로서비스 + 인프라 한 번에 실행
docker-compose up -d

# 📊 서비스 상태 확인
docker-compose ps

# 📋 로그 확인
docker-compose logs -f

# 🏥 헬스체크
curl http://localhost:8080/health
```

### 2. **개발 모드 실행** ⚡
```bash
# 1️⃣ 인프라만 먼저 실행
docker-compose up postgres redis pgadmin -d

# 2️⃣ 각 서비스를 UV로 개발 모드 실행
cd services/auth-service
uv sync                    # 48ms에 의존성 설치 완료!
uv run uvicorn app.main:app --reload --port 8010

# 다른 터미널에서
cd services/member-service
uv sync
uv run uvicorn app.main:app --reload --port 8001

# API Gateway도 개발 모드로
cd services/api-gateway
uv sync
uv run uvicorn app.main:app --reload --port 8080
```

### 3. **Frontend 개발**
```bash
cd frontend
npm install
npm run dev
# 🌐 http://localhost:5173
```

### 4. **주요 접속 URL**
- **🏠 메인 포털**: http://localhost:5173
- **🚪 API Gateway**: http://localhost:8080
- **📚 통합 API 문서**: http://localhost:8080/docs

#### **마이크로서비스별 API 문서**:
- **🔐 Auth Service**: http://localhost:8010/docs
- **👥 Member Service**: http://localhost:8001/docs
- **🏢 Customer Service**: http://localhost:8002/docs
- **📅 Calendar Service**: http://localhost:8003/docs
- **📢 Notice Service**: http://localhost:8004/docs
- **📰 Feeds Service**: http://localhost:8000/docs

#### **관리 도구**:
- **🗄️ pgAdmin**: http://localhost:5050
  - Email: `admin@tsportal.com` / Password: `admin123!`
- **🐘 PostgreSQL**: localhost:5432
  - Database: `tsportal` / User: `tsportal` / Password: `tsportal123!`

## ⚡ UV 기반 개발 경험

### **극단적 성능 향상**
```bash
# 기존 pip 방식 (느림)
pip install -r requirements.txt  # 10-30초

# 🚀 UV 방식 (극속)
uv sync                          # 48ms! (50-200배 빠름)
```

### **모든 서비스 동일한 현대적 구조**
```bash
# 어떤 서비스든 동일한 명령어
cd services/{any-service}
uv sync                    # 의존성 설치
uv run uvicorn app.main:app --reload  # 개발 서버 실행
uv add {package}          # 패키지 추가
uv lock --upgrade         # 의존성 업데이트
```

### **Docker 빌드 최적화**
```dockerfile
# UV 기반 Dockerfile (모든 서비스 동일)
FROM python:3.11-slim
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-cache
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

## 📊 **MSA 전환 성과**

### **개발 생산성**
| 항목 | 모놀리식 (이전) | MSA + UV (현재) | 개선도 |
|------|----------------|-----------------|--------|
| **서비스 시작** | 10-15초 | **2-3초** | **5배 빠름** |
| **의존성 설치** | 10-30초 | **48ms** | **200배 빠름** |
| **코드 복잡도** | 높음 (통합) | **낮음 (분리)** | **유지보수 용이** |
| **배포 단위** | 전체 | **서비스별** | **독립 배포** |
| **스케일링** | 제한적 | **서비스별** | **유연한 확장** |

### **서비스별 경량화**
- **Feeds Service**: 600+ 라인 → **183라인** (3배 감소)
- **Notice Service**: 복잡한 구조 → **단순한 CRUD**
- **Auth Service**: 통합 인증 → **JWT 전용**

## 📡 API 문서

### **통합 API Gateway**
```bash
# 🚪 API Gateway를 통한 통합 접근
curl http://localhost:8080/api/auth/login      # Auth Service
curl http://localhost:8080/api/members/        # Member Service
curl http://localhost:8080/api/customers/      # Customer Service
curl http://localhost:8080/api/calendar/       # Calendar Service
curl http://localhost:8080/api/notices/        # Notice Service
curl http://localhost:8080/api/feeds/          # Feeds Service
```

### **헬스체크 시스템**
```bash
# 전체 시스템 상태 확인
curl http://localhost:8080/health

# 개별 서비스 상태 확인
curl http://localhost:8010/health  # Auth
curl http://localhost:8001/health  # Member
curl http://localhost:8002/health  # Customer
curl http://localhost:8003/health  # Calendar
curl http://localhost:8004/health  # Notice
curl http://localhost:8000/health  # Feeds
```

## 🚢 배포

### **AWS ECS 배포**
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### **Docker 기반 배포**
```bash
# 전체 스택 프로덕션 배포
docker-compose -f docker-compose.yml up -d

# 특정 서비스만 업데이트
docker-compose up -d member-service customer-service
```

## 🔮 로드맵

### **Phase 1 - 기본 기능** ✅ (완료)
- ✅ 기본 CRUD 기능
- ✅ 듀얼 뷰 모드
- ✅ 팀 대시보드
- ✅ RSS 피드 수집
- ✅ 사용자 인증/권한

### **Phase 2 - MSA 전환** ✅ (완료!)
- ✅ PostgreSQL 마이그레이션
- ✅ **6개 마이크로서비스 완전 분리**
- ✅ **API Gateway 구축**
- ✅ **UV 기반 현대화**
- ✅ **Feeds Service 경량화**

### **Phase 3 - 고급 기능** 🚧 (진행 중)
- 🚧 실시간 알림 시스템
- 📋 보고서 생성 기능
- 📋 데이터 분석 대시보드
- 📋 서비스 메시 도입
- 📋 분산 추적 시스템

## 🎨 UI/UX 특징

### **디자인 시스템**
- **컬러 팔레트**: Purple 기반 브랜드 컬러
- **폰트 표준화**: 일관된 텍스트 크기 및 가중치
- **반응형 디자인**: 모바일/태블릿/데스크톱 최적화

### **사용자 경험**
- **마이크로서비스 투명성**: 사용자는 MSA 복잡성을 느끼지 않음
- **빠른 응답**: UV 최적화로 극단적 성능
- **실시간 피드백**: 작업 성공/실패 즉각 알림

## 🤝 기여하기

### **개발 환경 설정**
```bash
# 1. UV 설치
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 프로젝트 클론
git clone https://github.com/your-repo/ts-portal.git
cd ts-portal

# 3. 인프라 실행
docker-compose up postgres redis -d

# 4. 원하는 서비스 개발
cd services/member-service
uv sync
uv run uvicorn app.main:app --reload --port 8001
```

### **브랜치 전략**
- `main`: 프로덕션 배포 브랜치
- `develop`: 개발 통합 브랜치
- `feature/*`: 기능 개발 브랜치
- `service/*`: 서비스별 개발 브랜치

## 📞 연락처

**TS Team** - Saltware CSG  
**Project Maintainer**: Seungdo Bae  
**Architecture**: Microservices + API Gateway + UV

---

<div align="center">
  <p><strong>🚀 완전한 마이크로서비스 아키텍처로 전환 완료!</strong></p>
  <p>Made with ❤️ by TS Team Seungdo Bae</p>
  <p>© 2025 Saltware CSG. All rights reserved.</p>
</div>
