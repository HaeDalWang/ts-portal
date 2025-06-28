# TS Portal 🚀

> **Saltware CSG - TS팀 통합 포털 사이트**  
> Vue 3 + TypeScript + FastAPI로 구축된 현대적인 팀 관리 플랫폼

![Vue 3](https://img.shields.io/badge/Vue-3.x-4FC08D?style=flat-square&logo=vue.js&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat-square&logo=typescript&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=flat-square&logo=fastapi&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.x-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat-square&logo=postgresql&logoColor=white)

## 📋 목차

- [프로젝트 개요](#-프로젝트-개요)
- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)
- [마이크로서비스 아키텍처](#-마이크로서비스-아키텍처)
- [프로젝트 구조](#-프로젝트-구조)
- [설치 및 실행](#-설치-및-실행)
- [API 문서](#-api-문서)
- [배포](#-배포)
- [기여하기](#-기여하기)

## 🎯 프로젝트 개요

TS Portal은 Saltware CSG TS팀을 위한 통합 관리 플랫폼입니다. 팀원 관리, 고객사 관리, 일정 관리, 그리고 최신 AWS 소식까지 한 곳에서 확인할 수 있는 올인원 솔루션을 제공합니다.

### 🌟 핵심 가치
- **효율성**: 분산된 정보를 하나의 플랫폼으로 통합
- **사용성**: 직관적이고 현대적인 사용자 인터페이스
- **확장성**: 마이크로서비스 아키텍처로 유연한 확장 가능
- **실시간성**: 최신 정보를 실시간으로 제공

## ✨ 주요 기능

### 🏠 대시보드 홈
- **6개 핵심 카드**: AWS 소식, TS 공지사항, 점심 추천, 팀원 프로필, 팀 대시보드, MSP 관리
- **반응형 그리드 레이아웃**: 모든 디바이스에서 최적화된 경험
- **실시간 업데이트**: 각 카드별 실시간 정보 제공

### 📰 AWS 소식 (HoneyBox)
- **RSS 피드 수집**: AWS 공식 블로그, 뉴스, 업데이트 자동 수집
- **지능형 필터링**: 품질 점수 기반 콘텐츠 필터링
- **캐싱 시스템**: Redis 기반 고성능 캐싱
- **다국어 지원**: 한국어/영어 콘텐츠 자동 분류

### 👥 팀원 프로필 관리
- **권한 시스템**: Admin, Power User, User 역할 기반 접근 제어
- **내 프로필 편집**: 사용자가 자신의 연락처, 기술 스택 등 직접 수정
- **듀얼 뷰 모드**: 카드 뷰 / 테이블 뷰 전환 가능
- **고급 검색**: 이름, 이메일, 직급, 기술스택 통합 검색
- **상세 모달**: 팀원별 상세 정보 팝업
- **실시간 통계**: 재직률, 팀 구성 현황 실시간 표시

### 🏢 MSP 고객사 관리
- **고객사 데이터베이스**: 담당자, 계약 정보, 연락처 통합 관리
- **담당자 배정**: 주/부 담당자를 팀원 중에서 선택하여 배정
- **기술지원등급**: Standard, Advanced, Enterprise 등급으로 계약 관리
- **듀얼 뷰 모드**: 카드 뷰 / 테이블 뷰 (기본값: 테이블)
- **검색 및 필터**: 다양한 조건으로 고객사 검색

### 📅 팀 대시보드 (일정 관리)
- **FullCalendar 통합**: 월/주/일 뷰 지원
- **7가지 이벤트 타입**: 휴가, 재택, 출장, 프로젝트, 교육, 회의, 기타
- **팀원별 색상 구분**: 동적 색상 생성 알고리즘 (HSL 기반)
- **실시간 통계**: 오늘 일정, 이번 주 일정 등
- **고급 필터링**: 팀원별, 이벤트 타입별 필터

### 🔒 관리자 페이지
- **팀원 관리**: 신규 팀원 생성, 정보 수정, 비활성화/삭제
- **권한 제어**: 사용자별 역할(Admin, Power User, User) 변경
- **통합 관리**: 포털의 핵심 데이터 및 설정 관리

## 🛠 기술 스택

### Frontend
- **Vue 3** - Composition API, TypeScript 지원
- **Vue Router** - SPA 라우팅 관리
- **TypeScript** - 타입 안전성과 개발 생산성
- **TailwindCSS** - 유틸리티 퍼스트 CSS 프레임워크
- **Axios** - HTTP 클라이언트 (API 통신)
- **FullCalendar** - 고급 달력 컴포넌트
- **Vite** - 빠른 개발 서버 및 빌드 도구

### Backend Services

#### 🍯 HoneyBox (RSS 수집 서비스)
- **FastAPI** - 고성능 비동기 웹 프레임워크
- **Pydantic** - 데이터 검증 및 직렬화
- **Redis** - 캐싱 및 세션 관리
- **APScheduler** - 백그라운드 작업 스케줄링

#### 🗄️ TS Portal DB (데이터 관리 서비스) → MSA로 분리 예정
- **FastAPI** - RESTful API 서버
- **SQLAlchemy** - ORM 및 데이터베이스 추상화
- **Alembic** - 데이터베이스 마이그레이션
- **Pydantic** - API 스키마 정의
- **Passlib & JWT** - 비밀번호 해싱 및 인증
- **PostgreSQL** - 프로덕션 데이터베이스 (SQLite에서 마이그레이션)

### Infrastructure
- **Docker & Docker Compose** - 컨테이너화 및 로컬 개발
- **PostgreSQL** - 메인 데이터베이스
- **Redis** - 캐싱 및 세션 저장소
- **Nginx** - 리버스 프록시
- **API Gateway** - 마이크로서비스 라우팅 (계획)
- **ECS Fargate** - 컨테이너 오케스트레이션 (프로덕션)
- **Application Load Balancer** - 로드 밸런싱
- **Route 53** - DNS 관리
- **CloudWatch** - 모니터링 및 로깅

## 🏗️ 마이크로서비스 아키텍처

### 현재 상태 (모놀리식)
```
Frontend → Nginx → ts-portal-db (모든 기능 통합)
                 → HoneyBox (독립 서비스)
```

### 목표 상태 (MSA)
```
Frontend → API Gateway → Auth Service (인증/인가)
                      → Member Service (팀원 프로필)
                      → Customer Service (고객사 관리)
                      → Calendar Service (일정 관리)
                      → Notice Service (공지사항)
                      → HoneyBox (AWS 소식)
```

### 서비스별 포트 할당 ✅
- **Auth Service**: 8010 (인증/인가 전담) ✅
- **Member Service**: 8001 (팀원 프로필 관리) ✅
- **Customer Service**: 8002 (고객사 + 담당 배정) ✅
- **Calendar Service**: 8003 (일정 관리) ✅
- **Notice Service**: 8004 (공지사항) ✅
- **HoneyBox**: 8000 (기존 유지) ✅

- **API Gateway**: 8080 (계획)

### MSA 전환 전략 (Phase 1 - Simple MSA)
1. **데이터베이스 분리**: SQLite → PostgreSQL 마이그레이션
2. **스키마 분리**: 서비스별 논리적 스키마 생성
   - `member_schema`: 회원 정보
   - `customer_schema`: 고객사 및 담당 배정
   - `calendar_schema`: 일정 관리
   - `notice_schema`: 공지사항
3. **단계적 서비스 분리**:
   - Notice Service부터 시작 (가장 독립적)
   - Calendar Service
   - Customer Service
   - Member Service
   - Auth Service (마지막)
4. **API Gateway 도입**: 인증 처리 및 라우팅 통합

## 📁 프로젝트 구조

### 현재 구조
```
ts-portal/
├── 🎨 frontend/                 # Vue 3 Frontend
│   ├── src/
│   │   ├── components/          # 재사용 컴포넌트
│   │   ├── views/              # 페이지 컴포넌트
│   │   ├── services/           # API 서비스 레이어
│   │   ├── utils/              # 유틸리티
│   │   └── router/             # Vue Router 설정
│   └── package.json
│
├── 🍯 honeybox/                 # RSS 수집 서비스
│   ├── app/
│   └── requirements.txt
│
├── 🔌 services/                 # 마이크로서비스들 (신규)
│   ├── auth-service/           # 인증/인가
│   ├── member-service/         # 팀원 관리
│   ├── customer-service/       # 고객사 관리
│   ├── calendar-service/       # 일정 관리
│   └── notice-service/         # 공지사항
│
├── 📂 db/                      # 데이터베이스 관련
│   └── init/                   # PostgreSQL 초기화 스크립트
│
├── 🌐 nginx/                   # Nginx 설정
├── 🚀 terraform/               # Infrastructure as Code
└── 📜 Docker 설정 파일들
    ├── docker-compose.yml      # 프로덕션용
    ├── docker-compose.dev.yml  # 개발용 (PostgreSQL 포함)
    └── docker-compose.db.yml   # DB 전용
```

### MSA 전환 후 구조 (완료!) ✅
```
ts-portal/
├── 🎨 frontend/                 # Vue 3 + TypeScript
├── 🔌 services/                 # 마이크로서비스들 ✅
│   ├── auth-service/           # 인증/인가 ✅
│   ├── member-service/         # 팀원 관리 ✅
│   ├── customer-service/       # 고객사 관리 ✅
│   ├── calendar-service/       # 일정 관리 ✅
│   └── notice-service/         # 공지사항 ✅
├── 🍯 honeybox/                 # AWS 소식 수집 ✅
├── 🔌 api-gateway/              # API Gateway (계획)
└── 🗄️ 공통 리소스
    ├── db/                     # PostgreSQL 스크립트
    ├── nginx/                  # Nginx 설정
    └── terraform/              # Infrastructure as Code
```

## 🚀 설치 및 실행

### 사전 요구사항
- **Docker & Docker Compose**
- **Node.js** 18+ (Frontend 개발 시)
- **Python** 3.9+ (Backend 개발 시)

### 1. 전체 마이크로서비스 실행 (권장)
```bash
# 모든 마이크로서비스 + 데이터베이스 실행
docker-compose up -d

# 서비스 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f

# 특정 서비스만 실행
docker-compose up postgres redis -d  # 데이터베이스만
docker-compose up auth-service member-service -d  # 특정 서비스만
```

### 2. 개발 모드 실행
```bash
# 특정 서비스만 개발 모드로 실행
docker-compose up postgres redis pgadmin -d  # 인프라만
# 그 후 각 서비스를 로컬에서 개발

# pgAdmin 접속: http://localhost:5050
# Email: admin@tsportal.com / Password: admin123!
```

### 3. Frontend 개발
```bash
cd frontend
npm install
npm run dev
# http://localhost:5173
```

### 4. 접속 URL
- **메인 포털**: http://localhost:5173
- **마이크로서비스 API 문서**:
  - Auth Service: http://localhost:8010/docs
  - Member Service: http://localhost:8001/docs
  - Customer Service: http://localhost:8002/docs
  - Calendar Service: http://localhost:8003/docs
  - Notice Service: http://localhost:8004/docs
  - HoneyBox: http://localhost:8000/docs
- **관리 도구**:
  - pgAdmin: http://localhost:5050
  - PostgreSQL: localhost:5432


## 📊 데이터베이스 스키마

### PostgreSQL 스키마 구조
- **member_schema**
  - members: 팀원 정보
- **customer_schema**
  - customers: 고객사 정보
  - assignments: 담당 배정
- **calendar_schema**
  - events: 팀 일정
- **notice_schema**
  - notices: 공지사항

### 접속 정보
- **Host**: localhost (Docker 내부: postgres)
- **Port**: 5432
- **Database**: tsportal
- **User**: tsportal
- **Password**: tsportal123!

## 📡 API 문서

각 서비스 실행 후 `/docs` 엔드포인트에서 최신 Swagger UI를 확인하세요.

## 🚢 배포

### AWS ECS 배포
`terraform` 디렉토리의 코드를 사용하여 배포할 수 있습니다.
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

## 🎨 UI/UX 특징

### 디자인 시스템
- **컬러 팔레트**: Purple 기반 브랜드 컬러
- **폰트 표준화**: 일관된 텍스트 크기 및 가중치
- **반응형 디자인**: 모바일/태블릿/데스크톱 최적화

### 사용자 경험
- **직관적인 워크플로우**: 사용자 역할에 맞는 명확한 기능 제공
- **피드백 시스템**: 작업 성공/실패 시 즉각적인 알림
- **로딩 상태 표시**: 비동기 작업 중 시각적 피드백 제공

## 🔄 개발 워크플로우

### 브랜치 전략
- `main`: 프로덕션 배포 브랜치
- `develop`: 개발 통합 브랜치
- `feature/*`: 기능 개발 브랜치
- `msa/*`: MSA 전환 작업 브랜치

### 코드 품질
- **TypeScript**: 타입 안전성 보장
- **ESLint/Prettier**: 코드 스타일 통일
- **Pydantic**: API 스키마 검증

## 🔮 로드맵

### Phase 1 - 기본 기능 (완료) ✅
- ✅ 기본 CRUD 기능
- ✅ 듀얼 뷰 모드
- ✅ 팀 대시보드
- ✅ RSS 피드 수집
- ✅ 사용자 인증/권한

### Phase 2 - MSA 전환 (완료!) ✅
- ✅ PostgreSQL 마이그레이션
- ✅ 마이크로서비스 분리 (완료!)
  - ✅ Notice Service (완료)
  - ✅ Calendar Service (완료)
  - ✅ Customer Service (완료)
  - ✅ Member Service (완료)
  - ✅ Auth Service (완료)
- 🚧 API Gateway 구축 (진행 중)
- ⏳ 서비스 간 통신 최적화 (대기)

### Phase 3 - 고급 기능 (계획) 📋
- 📋 실시간 알림 시스템
- 📋 보고서 생성 기능
- 📋 데이터 분석 대시보드
- 📋 모바일 앱 개발
- 📋 외부 시스템 연동

### Phase 4 - 확장 및 최적화 (미래) 🔮
- 🔮 서비스 메시 도입
- 🔮 분산 추적 시스템
- 🔮 자동 스케일링
- 🔮 다중 리전 지원

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 연락처

**TS Team** - Saltware CSG  
**Project Link**: [https://github.com/your-repo/ts-portal](https://github.com/your-repo/ts-portal)

---

<div align="center">
  <p>Made with ❤️ by TS Team</p>
  <p>© 2024 Saltware CSG. All rights reserved.</p>
</div>
