# TS Portal Frontend v2.0

> 최적화된 Vue 3 프론트엔드 - MSA 서비스 연동 최우선 설계

## 🎯 프로젝트 목표

기존 프론트엔드의 무거움을 해결하고, **MSA 서비스들과의 완벽한 연동**을 최우선으로 하는 경량화된 새 프론트엔드 구축

### 핵심 설계 원칙
- 🔗 **MSA 서비스 중심 설계** (Kong API Gateway 완전 활용)
- ⚡ **최적화 우선** (번들 크기, 로딩 속도, 런타임 성능)
- 🎨 **일관된 디자인** (기능 완성 후 일괄 적용)
- 🔄 **중복 최소화** (컴포넌트, 로직, 스타일)
- 📦 **적은 라이브러리** (필수 의존성만 사용)
- 🛠️ **기능 중심** (디자인보다 MSA 연동 우선)

## 🏗️ 아키텍처 설계

### 기술 스택 (최소화)
- **Vue 3** (Composition API)
- **TypeScript** (타입 안전성)
- **Vite** (빌드 도구)
- **CSS Modules** (스타일링)
- **Fetch API** (HTTP 클라이언트)

### 제거된 의존성
- ❌ TailwindCSS (CSS 직접 작성)
- ❌ Axios (Fetch API 사용)
- ❌ Pinia (Composition API로 대체)
- ❌ 무거운 UI 라이브러리들

## 📁 프로젝트 구조

```
frontend-new/
├── src/
│   ├── services/           # MSA 서비스별 API 레이어 ⭐
│   │   ├── api.ts         # Kong Gateway 기본 클래스
│   │   ├── auth.ts        # Auth Service (8010)
│   │   ├── member.ts      # Member Service (8001)
│   │   ├── customer.ts    # Customer Service (8002)
│   │   ├── calendar.ts    # Calendar Service (8003)
│   │   ├── notice.ts      # Notice Service (8004)
│   │   └── feeds.ts       # Feeds Service (8000)
│   │
│   ├── components/         # 기능별 컴포넌트
│   │   ├── auth/          # 로그인/인증 관련
│   │   ├── member/        # 팀원 관리 컴포넌트
│   │   ├── customer/      # 고객사 관리 컴포넌트
│   │   ├── calendar/      # 일정 관리 컴포넌트
│   │   ├── notice/        # 공지사항 컴포넌트
│   │   ├── feeds/         # AWS 피드 컴포넌트
│   │   └── common/        # 공통 컴포넌트
│   │
│   ├── views/             # 페이지 컴포넌트 (7개)
│   │   ├── LoginView.vue
│   │   ├── DashboardView.vue
│   │   ├── MemberView.vue
│   │   ├── CustomerView.vue
│   │   ├── CalendarView.vue
│   │   ├── NoticeView.vue
│   │   └── FeedsView.vue
│   │
│   ├── composables/       # 재사용 로직 (Vue 3 Composables)
│   │   ├── useAuth.ts     # 인증 상태 관리
│   │   ├── useApi.ts      # API 호출 공통 로직
│   │   └── useError.ts    # 에러 처리
│   │
│   ├── utils/             # 유틸리티 함수
│   │   ├── jwt.ts         # JWT 토큰 관리
│   │   ├── storage.ts     # LocalStorage 관리
│   │   └── format.ts      # 데이터 포맷팅
│   │
│   ├── styles/            # CSS 스타일
│   │   ├── global.css     # 글로벌 스타일
│   │   ├── variables.css  # CSS 변수
│   │   └── components/    # 컴포넌트별 CSS
│   │
│   ├── types/             # TypeScript 타입 정의
│   │   ├── auth.ts
│   │   ├── member.ts
│   │   ├── customer.ts
│   │   └── api.ts
│   │
│   ├── router/            # Vue Router 설정
│   │   └── index.ts
│   │
│   ├── App.vue            # 루트 컴포넌트
│   └── main.ts            # 엔트리 포인트
│
├── public/                # 정적 파일
├── package.json           # 의존성 (최소화)
├── vite.config.ts         # Vite 설정
├── tsconfig.json          # TypeScript 설정
└── README.md              # 이 문서
```

## 🚀 개발 로드맵

### Phase 1: 핵심 인프라 구축 (1주)
1. **API Service Layer 구축** ⭐
   - Kong Gateway 연동 기본 클래스
   - JWT 토큰 관리 시스템
   - 에러 핸들링 (네트워크, 인증, 비즈니스 로직)
   - 각 MSA별 서비스 클래스 작성

2. **기본 프로젝트 설정**
   - Vite + Vue 3 + TypeScript 설정
   - 라우터 기본 구조
   - CSS 변수 및 글로벌 스타일

### Phase 2: 핵심 기능 개발 (2-3주)
1. **Auth System (최우선)**
   - 로그인/로그아웃 기능
   - JWT 토큰 관리 및 갱신
   - 라우터 가드 구현

2. **각 MSA별 순차 개발**
   - Member Service 연동 (팀원 관리)
   - Customer Service 연동 (고객사 관리)
   - Calendar Service 연동 (일정 관리)
   - Notice Service 연동 (공지사항)
   - Feeds Service 연동 (AWS 피드)

### Phase 3: 최적화 및 폴리싱 (1주)
1. **성능 최적화**
   - 번들 크기 분석 및 최적화
   - 컴포넌트 lazy loading
   - API 호출 최적화

2. **UI/UX 개선**
   - 일관된 디자인 시스템 적용
   - 반응형 디자인
   - 접근성 개선

## 🔧 핵심 설계 결정사항

### 1. 상태 관리 전략
```typescript
// 글로벌 상태 최소화, 각 서비스별 독립적 상태 관리
const useAuthStore = () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const isAuthenticated = computed(() => !!token.value)
  // ...
}
```

### 2. API 호출 패턴
```typescript
// Composable 기반 API 호출
const useMembers = () => {
  const members = ref<Member[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  
  const fetchMembers = async () => {
    loading.value = true
    try {
      members.value = await memberService.getAll()
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }
  
  return { members, loading, error, fetchMembers }
}
```

### 3. 컴포넌트 구조
- **중간 크기 컴포넌트** (너무 크지도 작지도 않게)
- **기능별 그룹핑** (MSA 서비스 단위)
- **Props 최소화** (필요한 데이터만 전달)

### 4. 에러 처리 전략
- **MSA 서비스별 개별 장애 대응**
- **사용자 친화적 에러 메시지**
- **네트워크 오류 vs 비즈니스 로직 오류 구분**
- **Fallback UI 제공**

## 🎯 MSA 서비스 연동 우선순위

| 순서 | 서비스 | 포트 | 주요 기능 | 개발 우선도 |
|------|--------|------|-----------|-------------|
| 1 | Auth Service | 8010 | 로그인, JWT 관리 | 🔴 최우선 |
| 2 | Member Service | 8001 | 팀원 CRUD | 🟡 높음 |
| 3 | Customer Service | 8002 | 고객사 CRUD | 🟡 높음 |
| 4 | Calendar Service | 8003 | 일정 CRUD | 🟢 보통 |
| 5 | Notice Service | 8004 | 공지사항 CRUD | 🟢 보통 |
| 6 | Feeds Service | 8000 | AWS 피드 조회 | 🔵 낮음 |

## 📊 성능 목표

### 번들 크기
- **Initial Bundle**: < 200KB (gzipped)
- **Total Assets**: < 500KB
- **Third-party Libraries**: < 100KB

### 로딩 성능
- **First Contentful Paint**: < 1.5초
- **Time to Interactive**: < 3초
- **API Response Time**: < 500ms (Kong 경유)

### 런타임 성능
- **메모리 사용량**: < 50MB
- **컴포넌트 렌더링**: < 16ms
- **라우터 전환**: < 100ms

## 🛠️ 개발 가이드라인

### 코딩 스타일
- **TypeScript Strict Mode** 사용
- **Composition API** 우선 사용
- **단일 책임 원칙** 준수
- **명확한 네이밍** (기능 중심)

### API 호출 규칙
- **모든 API는 Kong Gateway 경유** (localhost:8080)
- **에러 처리 필수** (try-catch)
- **로딩 상태 표시** 필수
- **JWT 토큰 자동 첨부**

### 컴포넌트 규칙
- **Props 타입 정의** 필수
- **Emit 이벤트 명시** 필수
- **CSS Modules** 사용
- **접근성 고려** (semantic HTML)

## 🚦 현재 상태

- ✅ **설계 완료** (이 문서)
- ⏳ **개발 준비 중**
- 🔄 **기존 프론트엔드와 병렬 개발**

---

**Goal**: MSA 서비스들과 완벽하게 연동되는 경량화된 프론트엔드  
**Timeline**: 4-5주 예상  
**Success Criteria**: 기존 대비 50% 이상 성능 개선 