# TS Portal 🚀

> **Saltware CSG - TS팀 통합 포털 사이트**  
> Vue 3 + TypeScript + FastAPI로 구축된 현대적인 팀 관리 플랫폼

![Vue 3](https://img.shields.io/badge/Vue-3.x-4FC08D?style=flat-square&logo=vue.js&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat-square&logo=typescript&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=flat-square&logo=fastapi&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.x-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)

## 📋 목차

- [프로젝트 개요](#-프로젝트-개요)
- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)
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
- **완전한 CRUD**: 팀원 정보 생성, 조회, 수정, 삭제
- **듀얼 뷰 모드**: 카드 뷰 / 테이블 뷰 전환 가능
- **고급 검색**: 이름, 이메일, 직급, 기술스택 통합 검색
- **기술스택 관리**: 컬러풀한 태그 시스템으로 기술 역량 시각화
- **상세 모달**: 팀원별 상세 정보 팝업
- **실시간 통계**: 재직률, 팀 구성 현황 실시간 표시

### 🏢 MSP 고객사 관리
- **고객사 데이터베이스**: 담당자, 계약 정보, 연락처 통합 관리
- **담당 배정 시스템**: 팀원-고객사 매핑 및 이력 관리
- **듀얼 뷰 모드**: 카드 뷰 / 테이블 뷰 (기본값: 테이블)
- **상태 관리**: 활성/비활성 고객사 구분
- **검색 및 필터**: 다양한 조건으로 고객사 검색

### 📅 팀 대시보드 (일정 관리)
- **FullCalendar 통합**: 월/주/일 뷰 지원
- **7가지 이벤트 타입**: 휴가, 재택, 출장, 프로젝트, 교육, 회의, 기타
- **팀원별 색상 구분**: 동적 색상 생성 알고리즘 (HSL 기반)
- **실시간 통계**: 오늘 일정, 이번 주 일정 등
- **고급 필터링**: 팀원별, 이벤트 타입별 필터
- **아웃룩 스타일 UI**: 직관적인 달력 인터페이스

## 🛠 기술 스택

### Frontend
- **Vue 3** - Composition API, TypeScript 지원
- **TypeScript** - 타입 안전성과 개발 생산성
- **TailwindCSS** - 유틸리티 퍼스트 CSS 프레임워크
- **FullCalendar** - 고급 달력 컴포넌트
- **Vite** - 빠른 개발 서버 및 빌드 도구

### Backend Services

#### 🍯 HoneyBox (RSS 수집 서비스)
- **FastAPI** - 고성능 비동기 웹 프레임워크
- **Pydantic** - 데이터 검증 및 직렬화
- **Redis** - 캐싱 및 세션 관리
- **APScheduler** - 백그라운드 작업 스케줄링

#### 🗄️ TS Portal DB (데이터 관리 서비스)
- **FastAPI** - RESTful API 서버
- **SQLAlchemy** - ORM 및 데이터베이스 추상화
- **SQLite** - 경량 데이터베이스 (개발/운영)
- **Pydantic** - API 스키마 정의

### Infrastructure
- **ECS Fargate** - 컨테이너 오케스트레이션
- **EFS** - 영구 스토리지 (SQLite 데이터베이스)
- **Application Load Balancer** - 로드 밸런싱
- **Route 53** - DNS 관리
- **CloudWatch** - 모니터링 및 로깅

## 📁 프로젝트 구조

```
ts-portal/
├── 🎨 frontend/                 # Vue 3 Frontend
│   ├── src/
│   │   ├── components/          # 재사용 가능한 컴포넌트
│   │   ├── views/              # 페이지 컴포넌트
│   │   │   ├── HomeView.vue    # 대시보드 홈
│   │   │   ├── TeamView.vue    # 팀원 프로필
│   │   │   ├── MspView.vue     # MSP 관리
│   │   │   └── DashboardView.vue # 팀 대시보드
│   │   ├── services/           # API 서비스 레이어
│   │   ├── types/              # TypeScript 타입 정의
│   │   └── router/             # Vue Router 설정
│   ├── package.json
│   └── vite.config.ts
│
├── 🍯 honeybox/                 # RSS 수집 서비스
│   ├── app/
│   │   ├── routers/            # API 라우터
│   │   ├── services/           # 비즈니스 로직
│   │   └── utils/              # 유틸리티 함수
│   ├── Dockerfile
│   └── requirements.txt
│
├── 🗄️ ts-portal-db/            # 데이터 관리 서비스
│   ├── app/
│   │   ├── models/             # SQLAlchemy 모델
│   │   ├── routers/            # API 라우터
│   │   ├── schemas/            # Pydantic 스키마
│   │   └── services/           # 비즈니스 로직
│   ├── data/                   # SQLite 데이터베이스
│   └── requirements.txt
│
├── 🚀 terraform/               # Infrastructure as Code
│   ├── cicd.tf                 # CI/CD 파이프라인
│   └── buildspec/              # CodeBuild 설정
│
├── 📜 start.sh                 # 개발 서버 시작 스크립트
├── 📜 stop.sh                  # 개발 서버 중지 스크립트
└── 📖 README.md
```

## 🚀 설치 및 실행

### 사전 요구사항
- **Node.js** 18+ 
- **Python** 3.9+
- **Redis** (HoneyBox 캐싱용)

### 1. 저장소 클론
```bash
git clone <repository-url>
cd ts-portal
```

### 2. 간편 실행 (권장)
```bash
# 모든 서비스 시작
./start.sh

# 모든 서비스 중지
./stop.sh
```

### 3. 개별 서비스 실행

#### Frontend (포트 5173)
```bash
cd frontend
npm install
npm run dev
```

#### HoneyBox RSS 서비스 (포트 8000)
```bash
cd honeybox
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

#### TS Portal DB 서비스 (포트 8001)
```bash
cd ts-portal-db
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 4. 접속 URL
- **메인 포털**: http://localhost:5173
- **HoneyBox API**: http://localhost:8000/docs
- **TS Portal DB API**: http://localhost:8001/docs

## 📊 데이터베이스 스키마

### 핵심 테이블
- **MEMBERS**: 팀원 정보 (이름, 이메일, 직급, 기술스택, 입사일 등)
- **CUSTOMERS**: 고객사 정보 (회사명, 담당자, 계약정보, 연락처 등)
- **ASSIGNMENTS**: 담당 배정 (팀원-고객사 매핑, 시작일, 종료일 등)
- **EVENTS**: 팀 일정 (제목, 날짜, 타입, 참석자, 설명 등)

### 샘플 데이터
- **14명 팀원**: Leaf/Tiger/Aqua 파트 + 함인용 상무
- **6개 고객사**: 네이버클라우드플랫폼, 카카오엔터프라이즈, 삼성SDS 등
- **26개 일정**: 2025년 5-7월 다양한 팀 이벤트

## 📡 API 문서

### HoneyBox API (포트 8000)
- `GET /feeds/aws-news` - AWS 뉴스 피드 조회
- `GET /feeds/daily-news` - 일일 뉴스 요약
- `GET /health` - 서비스 상태 확인

### TS Portal DB API (포트 8001)
- `GET /members` - 팀원 목록 조회
- `POST /members` - 팀원 추가
- `GET /customers` - 고객사 목록 조회
- `GET /events` - 일정 목록 조회
- `GET /events/today` - 오늘 일정 조회

**상세 API 문서**: 각 서비스 실행 후 `/docs` 엔드포인트에서 Swagger UI 확인

## 🚢 배포

### AWS ECS 배포
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### 환경 변수
```bash
# .env 파일 생성
REDIS_URL=redis://localhost:6379
DATABASE_URL=sqlite:///./data/ts_portal.db
```

## 🎨 UI/UX 특징

### 디자인 시스템
- **컬러 팔레트**: Purple 기반 브랜드 컬러
- **폰트 표준화**: 일관된 텍스트 크기 및 가중치
- **반응형 디자인**: 모바일/태블릿/데스크톱 최적화
- **다크 모드**: 준비 중

### 사용자 경험
- **듀얼 뷰 모드**: 카드/테이블 뷰 자유 전환
- **실시간 검색**: 타이핑과 동시에 결과 업데이트
- **스마트 필터링**: 다중 조건 필터 지원
- **직관적 네비게이션**: 명확한 정보 구조

## 🔄 개발 워크플로우

### 브랜치 전략
- `main`: 프로덕션 배포 브랜치
- `develop`: 개발 통합 브랜치
- `feature/*`: 기능 개발 브랜치

### 코드 품질
- **TypeScript**: 타입 안전성 보장
- **ESLint/Prettier**: 코드 스타일 통일
- **Pydantic**: API 스키마 검증

## 🔮 로드맵

### Phase 1 (완료)
- ✅ 기본 CRUD 기능
- ✅ 듀얼 뷰 모드
- ✅ 팀 대시보드
- ✅ RSS 피드 수집

### Phase 2 (진행 중)
- 🔄 사용자 인증/권한
- 🔄 알림 시스템
- 🔄 모바일 앱

### Phase 3 (계획)
- 📋 보고서 생성
- 📋 데이터 분석
- 📋 외부 시스템 연동

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
