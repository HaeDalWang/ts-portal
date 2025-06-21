# TS Portal - Frontend 🎨

> **Vue 3 + TypeScript + TailwindCSS 기반 현대적인 팀 관리 포털**  
> Saltware CSG TS팀의 통합 관리 플랫폼 프론트엔드

![Vue 3](https://img.shields.io/badge/Vue-3.5.13-4FC08D?style=flat-square&logo=vue.js&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.8.0-3178C6?style=flat-square&logo=typescript&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4.17-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-6.2.4-646CFF?style=flat-square&logo=vite&logoColor=white)

## 📋 목차

- [프로젝트 개요](#-프로젝트-개요)
- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)
- [설치 및 실행](#-설치-및-실행)
- [프로젝트 구조](#-프로젝트-구조)
- [디자인 시스템](#-디자인-시스템)
- [컴포넌트 가이드](#-컴포넌트-가이드)
- [개발 가이드](#-개발-가이드)

## 🎯 프로젝트 개요

TS Portal Frontend는 Vue 3의 Composition API와 TypeScript를 활용하여 구축된 현대적인 SPA(Single Page Application)입니다. 팀원 관리, 고객사 관리, 일정 관리 등 팀 운영에 필요한 모든 기능을 직관적인 UI로 제공합니다.

### 🌟 핵심 특징
- **타입 안전성**: TypeScript로 런타임 에러 최소화
- **반응형 디자인**: 모든 디바이스에서 최적화된 경험
- **컴포넌트 기반**: 재사용 가능한 모듈형 아키텍처
- **실시간 업데이트**: 데이터 변경 시 즉시 UI 반영

## ✨ 주요 기능

### 🏠 대시보드 홈
- **6개 핵심 카드**: 각 기능별 진입점 제공
- **반응형 그리드**: 화면 크기에 따른 자동 배치
- **호버 효과**: 인터랙티브한 사용자 경험

### 👥 팀원 프로필 관리
- **듀얼 뷰 모드**: 카드 뷰(기본) ↔ 테이블 뷰 전환
- **실시간 검색**: 이름, 이메일, 직급, 기술스택 통합 검색
- **고급 필터링**: 재직자/전체 필터, 다중 조건 검색
- **상세 모달**: 팀원별 상세 정보 팝업
- **기술스택 시각화**: 컬러풀한 태그 시스템
- **실시간 통계**: 전체/재직/재직률 실시간 표시

### 🏢 MSP 고객사 관리
- **듀얼 뷰 모드**: 카드 뷰 ↔ 테이블 뷰(기본) 전환
- **고객사 데이터베이스**: 담당자, 계약정보, 연락처 관리
- **담당 배정 표시**: 팀원-고객사 매핑 시각화
- **상태 관리**: 활성/비활성 고객사 구분
- **검색 시스템**: 회사명, 담당자, 업종별 검색

### 📅 팀 대시보드 (일정 관리)
- **FullCalendar 통합**: 월/주/일 뷰 지원
- **7가지 이벤트 타입**: 휴가, 재택, 출장, 프로젝트, 교육, 회의, 기타
- **팀원별 색상 구분**: HSL 기반 동적 색상 생성
- **고급 필터링**: 팀원별, 이벤트 타입별 다중 필터
- **실시간 통계**: 오늘 일정, 이번 주 일정 카운트
- **아웃룩 스타일 UI**: 직관적인 달력 인터페이스

### 📰 AWS 소식
- **RSS 피드 연동**: HoneyBox 서비스와 연동
- **품질 필터링**: 고품질 콘텐츠만 선별 표시
- **실시간 업데이트**: 최신 AWS 뉴스 자동 갱신

## 🛠 기술 스택

### Core Framework
- **Vue 3.5.13** - Composition API, `<script setup>` 문법
- **TypeScript 5.8.0** - 타입 안전성과 IntelliSense
- **Vue Router 4.5.1** - SPA 라우팅 관리

### Styling & UI
- **TailwindCSS 3.4.17** - 유틸리티 퍼스트 CSS 프레임워크
- **PostCSS 8.5.4** - CSS 후처리 및 최적화
- **Autoprefixer 10.4.21** - 브라우저 호환성

### Development Tools
- **Vite 6.2.4** - 빠른 개발 서버 및 빌드 도구
- **Vue DevTools** - Vue 컴포넌트 디버깅
- **TypeScript Compiler** - 타입 체크 및 컴파일

### External Libraries
- **FullCalendar** - 고급 달력 컴포넌트
- **Axios** - HTTP 클라이언트 (API 통신)

## 🚀 설치 및 실행

### 사전 요구사항
- **Node.js** 18.0.0 이상
- **npm** 8.0.0 이상

### 설치
```bash
cd frontend
npm install
```

### 개발 서버 실행
```bash
npm run dev
```
→ http://localhost:5173 에서 확인 가능

### 빌드
```bash
# 프로덕션 빌드
npm run build

# 타입 체크
npm run type-check

# 빌드 + 타입 체크
npm run build-only
```

### 개발 도구
```bash
# Vue DevTools 활성화 상태로 개발 서버 실행
npm run dev

# 타입 체크만 실행
npm run type-check
```

## 🚀 환경별 빌드 및 배포

### 개발 환경
```bash
# 개발 서버 실행 (localhost API 사용)
npm run dev

# 개발 환경용 빌드
npm run build:dev
```

### 프로덕션 환경
```bash
# 프로덕션 빌드 (tsapi.seungdobae.com API 사용)
npm run build:prod

# 또는 기본 빌드 명령어 (프로덕션 모드)
npm run build
```

## 🔧 환경변수 설정

### 개발 환경 (.env.development)
```env
VITE_APP_ENV=development
VITE_API_BASE_URL=http://localhost:8001
VITE_HONEYBOX_API_URL=http://localhost:8000
VITE_DB_API_URL=http://localhost:8001
```

### 프로덕션 환경 (.env.production)
```env
VITE_APP_ENV=production
VITE_API_BASE_URL=https://tsapi.seungdobae.com/api/db
VITE_HONEYBOX_API_URL=https://tsapi.seungdobae.com/api/feeds
VITE_DB_API_URL=https://tsapi.seungdobae.com/api/db
```

## 📡 API 엔드포인트

### 개발 환경
- **TS Portal DB API**: http://localhost:8001
- **HoneyBox API**: http://localhost:8000

### 프로덕션 환경
- **TS Portal DB API**: https://tsapi.seungdobae.com/api/db
- **HoneyBox API**: https://tsapi.seungdobae.com/api/feeds

## 🔄 자동 환경 감지

애플리케이션은 다음 순서로 API URL을 결정합니다:

1. **환경변수 우선**: `VITE_API_BASE_URL`, `VITE_HONEYBOX_API_URL` 등
2. **자동 감지**: Vite의 `import.meta.env.DEV` 플래그 기반
   - 개발 모드: localhost URL 사용
   - 프로덕션 모드: tsapi.seungdobae.com URL 사용

## 📦 S3 + CloudFront 배포

### 1. 프로덕션 빌드
```bash
npm run build:prod
```

### 2. S3 업로드
```bash
# AWS CLI를 사용한 배포 (예시)
aws s3 sync dist/ s3://your-bucket-name --delete
```

### 3. CloudFront 캐시 무효화
```bash
# CloudFront 배포 ID로 캐시 무효화
aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"
```

---

**이제 개발 시에는 localhost로, 프로덕션에서는 tsapi.seungdobae.com으로 자동 연결됩니다!** 🎯

## 📁 프로젝트 구조

```
src/
├── 📄 App.vue                   # 루트 컴포넌트
├── 📄 main.ts                   # 애플리케이션 엔트리 포인트
├── 🎨 assets/
│   ├── base.css                 # 기본 CSS 스타일
│   ├── main.css                 # TailwindCSS 전역 스타일
│   └── logo.svg                 # 로고 이미지
├── 🧩 components/               # 재사용 컴포넌트
│   ├── HelloWorld.vue           # 샘플 컴포넌트
│   ├── TheWelcome.vue           # 웰컴 컴포넌트
│   ├── WelcomeItem.vue          # 웰컴 아이템
│   └── icons/                   # 아이콘 컴포넌트들
├── ⚙️ config/
│   └── naver.ts                 # 네이버 API 설정
├── 🛣️ router/
│   └── index.ts                 # Vue Router 설정
├── 🌐 services/                 # API 서비스 레이어
│   ├── api.ts                   # 기본 API 설정
│   ├── memberService.ts         # 팀원 관리 API
│   ├── customerService.ts       # 고객사 관리 API
│   ├── eventService.ts          # 일정 관리 API
│   └── rssService.ts            # RSS 피드 API
├── 📝 types/
│   └── index.ts                 # TypeScript 타입 정의
└── 📱 views/                    # 페이지 컴포넌트
    ├── HomeView.vue             # 🏠 대시보드 홈
    ├── TeamView.vue             # 👥 팀원 프로필
    ├── MspView.vue              # 🏢 MSP 관리
    ├── DashboardView.vue        # 📅 팀 대시보드
    ├── AwsTipsView.vue          # 💡 AWS 소식
    ├── EventsView.vue           # 📅 TS 이벤트
    └── LunchView.vue            # 🍽 점심 추천
```

## 🎨 디자인 시스템

### 🎨 컬러 팔레트
```css
/* Primary Colors */
--primary-purple: #7C3AED    /* 메인 브랜드 컬러 */
--primary-blue: #3B82F6      /* 정보 표시 */
--primary-green: #10B981     /* 성공/활성 상태 */
--primary-orange: #F59E0B    /* 경고/주의 */
--primary-red: #EF4444       /* 에러/비활성 */

/* Neutral Colors */
--gray-50: #F9FAFB           /* 배경 */
--gray-100: #F3F4F6          /* 카드 배경 */
--gray-500: #6B7280          /* 부제목 */
--gray-900: #111827          /* 메인 텍스트 */
```

### 📝 폰트 표준화 시스템

우리가 정립한 **폰트 표준화 규칙**을 모든 컴포넌트에 일관되게 적용했습니다:

#### 헤더 폰트 표준
```css
/* 페이지 제목 */
.page-title { @apply text-xl font-bold text-gray-900; }

/* 부제목 */
.page-subtitle { @apply text-sm text-gray-500; }

/* 통계 숫자 */
.stat-number { @apply text-sm font-semibold; }  /* 색상별 구분 */

/* 통계 라벨 */
.stat-label { @apply text-xs text-gray-500; }
```

#### 콘텐츠 폰트 표준
```css
/* 카드 제목 */
.card-title { @apply text-sm font-semibold text-gray-900; }

/* 카드 부제목 */
.card-subtitle { @apply text-xs text-gray-600; }

/* 정보 텍스트 */
.info-text { @apply text-xs text-gray-600; }

/* 라벨 텍스트 */
.label-text { @apply text-xs font-medium text-gray-700; }
```

#### 테이블 폰트 표준
```css
/* 테이블 헤더 */
.table-header { @apply text-xs font-medium text-gray-500 uppercase; }

/* 테이블 메인 텍스트 */
.table-main { @apply text-sm font-medium text-gray-900; }

/* 테이블 서브 텍스트 */
.table-sub { @apply text-xs text-gray-500; }

/* 배지 텍스트 */
.badge-text { @apply text-xs font-semibold; }
```

#### 폰트 크기 가이드라인
- **제목/중요정보**: `text-sm` (14px)
- **부가정보/라벨**: `text-xs` (12px)
- **페이지 제목**: `text-xl` (20px)
- **강조**: `font-semibold` 또는 `font-medium`
- **일반**: `font-normal` (기본값)

### 🧩 컴포넌트 스타일

#### 카드 컴포넌트
```css
.card-base {
  @apply bg-white rounded-xl shadow-lg border border-gray-200 p-4 
         hover:shadow-xl transition-shadow cursor-pointer;
}
```

#### 버튼 컴포넌트
```css
.btn-primary {
  @apply px-3 py-1.5 bg-purple-600 text-white rounded-md 
         hover:bg-purple-700 disabled:opacity-50 transition-colors text-sm;
}

.btn-secondary {
  @apply px-3 py-1.5 bg-gray-100 text-gray-700 rounded-md 
         hover:bg-gray-200 transition-colors text-sm;
}
```

#### 뷰 모드 전환 버튼
```css
.view-toggle {
  @apply flex bg-gray-100 rounded-lg p-1;
}

.view-toggle-btn {
  @apply px-2 py-1 rounded-md text-xs font-medium transition-colors;
}

.view-toggle-btn.active {
  @apply bg-white text-gray-900 shadow-sm;
}

.view-toggle-btn.inactive {
  @apply text-gray-600 hover:text-gray-900;
}
```

### 📱 반응형 브레이크포인트
```css
/* TailwindCSS 기본 브레이크포인트 사용 */
sm: 640px    /* 모바일 가로 */
md: 768px    /* 태블릿 */
lg: 1024px   /* 데스크톱 */
xl: 1280px   /* 대형 데스크톱 */
```

## 🧩 컴포넌트 가이드

### 뷰 컴포넌트 구조

#### 1. HomeView.vue - 대시보드 홈
```vue
<template>
  <!-- 6개 카드 그리드 레이아웃 -->
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <!-- 각 카드는 라우터 링크로 연결 -->
  </div>
</template>
```

#### 2. TeamView.vue - 팀원 프로필
```vue
<template>
  <!-- 컴팩트 헤더 + 통계 -->
  <div class="bg-white border-b border-gray-200 px-6 py-3">
    <!-- 뷰 모드 전환 버튼 포함 -->
  </div>
  
  <!-- 검색 및 필터 -->
  <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-4">
    <!-- 실시간 검색 입력 -->
  </div>
  
  <!-- 카드 뷰 / 테이블 뷰 조건부 렌더링 -->
  <div v-if="viewMode === 'cards'"><!-- 카드 그리드 --></div>
  <div v-if="viewMode === 'table'"><!-- 테이블 --></div>
</template>
```

#### 3. DashboardView.vue - 팀 대시보드
```vue
<template>
  <!-- 아웃룩 스타일 레이아웃 -->
  <div class="flex h-screen bg-gray-50">
    <!-- 좌측 사이드바 -->
    <div class="w-80 bg-white border-r border-gray-200">
      <!-- 팀원 필터, 오늘 일정, 범례 -->
    </div>
    
    <!-- 메인 달력 영역 -->
    <div class="flex-1 p-6">
      <!-- FullCalendar 컴포넌트 -->
    </div>
  </div>
</template>
```

### API 서비스 패턴
```typescript
// services/memberService.ts 예시
export const memberService = {
  async getMembers(params?: MemberListParams): Promise<MemberListResponse> {
    const response = await api.get<MemberListResponse>('/members', { params })
    return response.data
  },
  
  async getMemberStats(): Promise<MemberStats> {
    const response = await api.get<MemberStats>('/members/stats')
    return response.data
  }
}
```

### TypeScript 타입 정의
```typescript
// types/index.ts
export interface Member {
  id: number
  name: string
  email: string
  position?: string
  team: string
  skills_list: string[]
  is_active: boolean
  join_date?: string
  phone?: string
}

export interface MemberStats {
  total_members: number
  active_members: number
  inactive_members: number
  active_rate: number
}
```

## 🔧 개발 가이드

### 새로운 페이지 추가
1. `views/` 디렉토리에 새 Vue 컴포넌트 생성
2. `router/index.ts`에 라우트 추가
3. 필요시 `services/`에 API 서비스 추가
4. `types/index.ts`에 타입 정의 추가

### 컴포넌트 개발 규칙
- **Composition API** 사용 (`<script setup>` 문법)
- **TypeScript** 타입 정의 필수
- **폰트 표준화 규칙** 준수
- **반응형 디자인** 고려
- **접근성(a11y)** 고려

### 스타일링 가이드라인
- **TailwindCSS 유틸리티 클래스** 우선 사용
- **커스텀 CSS** 최소화
- **일관된 간격** 사용 (p-3, p-4, p-6 등)
- **색상 팔레트** 준수

### 상태 관리
- **Vue 3 Composition API**로 로컬 상태 관리
- **API 호출**은 서비스 레이어에서 처리
- **에러 핸들링** 일관성 유지

## 📊 성능 최적화

### 번들 크기 최적화
- **Tree Shaking**: 사용하지 않는 코드 자동 제거
- **Code Splitting**: 라우트별 청크 분할
- **Dynamic Import**: 필요시에만 컴포넌트 로드

### 런타임 최적화
- **v-memo**: 리스트 렌더링 최적화
- **Lazy Loading**: 이미지 및 컴포넌트 지연 로딩
- **Debouncing**: 검색 입력 디바운싱

## 🧪 테스트

### 테스트 전략
- **단위 테스트**: 개별 컴포넌트 및 유틸리티 함수
- **통합 테스트**: API 서비스와 컴포넌트 연동
- **E2E 테스트**: 사용자 시나리오 기반 테스트

### 테스트 도구 (계획)
- **Vitest**: 단위 테스트 프레임워크
- **Vue Test Utils**: Vue 컴포넌트 테스트
- **Cypress**: E2E 테스트

## 🔮 로드맵

### Phase 1 (완료) ✅
- ✅ Vue 3 + TypeScript 기반 구조 구축
- ✅ 6개 핵심 페이지 구현
- ✅ 듀얼 뷰 모드 (카드/테이블)
- ✅ 팀 대시보드 (FullCalendar)
- ✅ 폰트 표준화 시스템
- ✅ 반응형 디자인

### Phase 2 (진행 중) 🔄
- 🔄 사용자 인증/권한 시스템
- 🔄 실시간 알림 (WebSocket)
- 🔄 PWA (Progressive Web App)
- 🔄 다크 모드 지원

### Phase 3 (계획) 📋
- 📋 단위 테스트 작성
- 📋 E2E 테스트 자동화
- 📋 성능 모니터링
- 📋 국제화 (i18n)

## 🚨 주의사항

### 버전 호환성
- **Node.js 18+** 필수
- **Vue 3.5.13** 고정 권장
- **TailwindCSS 3.x** 유지 (v4는 설정 방식 변경)

### 개발 환경
- **VS Code** + **Volar** 확장 권장
- **TypeScript** 엄격 모드 활성화
- **ESLint** + **Prettier** 설정 권장

### 브라우저 지원
- **Chrome** 90+
- **Firefox** 88+
- **Safari** 14+
- **Edge** 90+

## 📞 기술 지원

### 문제 해결
1. **개발 서버 실행 안됨**: Node.js 버전 확인
2. **타입 에러**: `npm run type-check` 실행
3. **스타일 적용 안됨**: TailwindCSS 설정 확인
4. **API 연동 실패**: 백엔드 서비스 상태 확인

### 참고 자료
- [Vue 3 공식 문서](https://vuejs.org/)
- [TypeScript 핸드북](https://www.typescriptlang.org/docs/)
- [TailwindCSS 문서](https://tailwindcss.com/docs)
- [FullCalendar Vue 가이드](https://fullcalendar.io/docs/vue)

---

<div align="center">
  <p><strong>Made with ❤️ by TS Team</strong></p>
  <p>© 2024 Saltware CSG. All rights reserved.</p>
</div>
