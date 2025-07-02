# TS Portal Frontend (New)

> Vue 3 + TypeScript 최신 프론트엔드

## 개요

Vue 3 Composition API와 TypeScript를 활용한 최신 프론트엔드입니다. 기존 frontend를 완전히 재구성하여 성능과 유지보수성을 대폭 개선했습니다.

## 🚀 주요 특징

- **Vue 3 Composition API** - 더 나은 타입 추론과 로직 재사용
- **TypeScript 100%** - 완전한 타입 안정성
- **Composables 패턴** - 재사용 가능한 상태 관리
- **서비스 레이어 분리** - API 호출 로직 모듈화
- **컴포넌트 최적화** - 단일 책임 원칙 적용

## 📁 프로젝트 구조

```
frontend-new/
├── src/
│   ├── components/              # 재사용 가능한 컴포넌트
│   │   ├── calendar/           # 캘린더 관련
│   │   │   ├── EventCard.vue   # 이벤트 카드
│   │   │   └── EventModal.vue  # 이벤트 생성/수정 모달
│   │   ├── common/             # 공통 컴포넌트
│   │   │   ├── BaseModal.vue   # 기본 모달
│   │   │   ├── LoadingSpinner.vue
│   │   │   └── ErrorMessage.vue
│   │   ├── customer/           # 고객사 관련
│   │   ├── layout/             # 레이아웃 컴포넌트
│   │   │   ├── AppHeader.vue
│   │   │   ├── AppNavigation.vue
│   │   │   └── AppSidebar.vue
│   │   ├── member/             # 팀원 관련
│   │   └── notices/            # 공지사항 관련
│   │
│   ├── composables/            # Vue 3 Composables
│   │   ├── useAuth.ts         # 인증 관련 상태/로직
│   │   ├── useCalendar.ts     # 캘린더 상태/로직
│   │   ├── useCustomer.ts     # 고객사 상태/로직
│   │   ├── useFeeds.ts        # 피드 상태/로직
│   │   ├── useMember.ts       # 팀원 상태/로직
│   │   └── useNotices.ts      # 공지사항 상태/로직
│   │
│   ├── services/              # API 서비스 레이어
│   │   ├── api.ts            # Kong Gateway API 클라이언트
│   │   ├── auth.ts           # 인증 서비스
│   │   ├── calendar.ts       # 캘린더 서비스
│   │   ├── customer.ts       # 고객사 서비스
│   │   ├── feeds.ts          # 피드 서비스
│   │   ├── member.ts         # 팀원 서비스
│   │   └── notices.ts        # 공지사항 서비스
│   │
│   ├── types/                 # TypeScript 타입 정의
│   │   ├── api.ts            # 공통 API 타입
│   │   ├── auth.ts           # 인증 관련 타입
│   │   ├── calendar.ts       # 캘린더 타입
│   │   ├── customer.ts       # 고객사 타입
│   │   ├── feeds.ts          # 피드 타입
│   │   ├── member.ts         # 팀원 타입
│   │   └── notices.ts        # 공지사항 타입
│   │
│   ├── views/                 # 페이지 컴포넌트
│   │   ├── AuthView.vue      # 로그인 페이지
│   │   ├── AwsFeedsView.vue  # AWS 피드 페이지
│   │   ├── CalendarView.vue  # 캘린더 페이지
│   │   ├── CustomerView.vue  # 고객사 관리 페이지
│   │   ├── DashboardView.vue # 대시보드
│   │   ├── MemberView.vue    # 팀원 관리 페이지
│   │   └── NoticesView.vue   # 공지사항 페이지
│   │
│   ├── router/               # Vue Router 설정
│   │   └── index.ts         # 라우트 정의
│   │
│   ├── styles/              # 스타일
│   │   ├── global.css       # 전역 스타일
│   │   └── variables.css    # CSS 변수
│   │
│   ├── utils/               # 유틸리티
│   │   └── jwt.ts          # JWT 토큰 처리
│   │
│   ├── config/              # 설정
│   │   ├── api.config.ts   # API 설정
│   │   └── app.config.ts   # 앱 설정
│   │
│   ├── App.vue              # 루트 컴포넌트
│   ├── main.ts             # 앱 진입점
│   └── vite-env.d.ts       # Vite 타입 정의
│
├── public/                  # 정적 파일
├── package.json
├── tsconfig.json           # TypeScript 설정
├── vite.config.ts          # Vite 설정
└── README.md
```

## 🛠️ 기술 스택

- **Vue 3.4+** - Composition API, `<script setup>`
- **TypeScript 5.0+** - 완전한 타입 안전성
- **Vite 5.0+** - 빠른 개발 서버 & 빌드
- **Vue Router 4** - 타입 안전한 라우팅
- **TailwindCSS 3** - 유틸리티 퍼스트 CSS
- **Lucide Vue** - 아이콘 라이브러리

## 🚀 실행 방법

### 개발 서버 실행
```bash
# 의존성 설치
npm install

# 개발 서버 시작 (포트: 5174)
npm run dev

# 브라우저에서 접속
open http://localhost:5174
```

### 빌드
```bash
# 프로덕션 빌드
npm run build

# 빌드 결과 미리보기
npm run preview
```

### 타입 체크
```bash
# TypeScript 타입 체크
npm run type-check

# Vue 컴포넌트 타입 체크
npm run build-only
```

## 📚 주요 컴포넌트

### 인증 (`useAuth`)
- JWT 토큰 기반 인증
- 자동 토큰 갱신
- 라우트 가드

```typescript
const { login, logout, user, isAuthenticated } = useAuth()

// 로그인
await login('admin', 'admin123!')

// 사용자 정보 접근
console.log(user.value?.name)
```

### 캘린더 (`useCalendar`)
- 일정 CRUD 작업
- 실시간 통계
- 타입별 필터링

```typescript
const { 
  events, 
  todayEvents, 
  loading, 
  createEvent, 
  loadEvents 
} = useCalendar()

// 이벤트 생성
await createEvent({
  title: '팀 회의',
  start_time: '2025-07-02T14:00:00',
  end_time: '2025-07-02T15:00:00',
  event_type: EventType.MEETING
})
```

### 고객사 관리 (`useCustomer`)
- 고객사 CRUD
- 담당자 배정
- 검색 및 필터링

```typescript
const { 
  customers, 
  assignments, 
  createCustomer, 
  assignMember 
} = useCustomer()
```

## 🎨 컴포넌트 설계 원칙

### 1. Single Responsibility
각 컴포넌트는 하나의 책임만 가집니다.

```vue
<!-- ❌ 거대한 컴포넌트 -->
<template>
  <!-- 모든 기능이 한 컴포넌트에 -->
</template>

<!-- ✅ 단일 책임 컴포넌트 -->
<template>
  <EventCard :event="event" @edit="onEdit" />
  <EventModal v-if="showModal" @save="onSave" />
</template>
```

### 2. Props & Emits 타입 정의
```vue
<script setup lang="ts">
interface Props {
  event: EventResponse
  readonly?: boolean
}

interface Emits {
  edit: [eventId: number]
  delete: [eventId: number]
}

const props = withDefaults(defineProps<Props>(), {
  readonly: false
})

const emit = defineEmits<Emits>()
</script>
```

### 3. Composables 활용
상태와 로직을 재사용 가능한 composables로 분리합니다.

```typescript
// composables/useModal.ts
export function useModal() {
  const isOpen = ref(false)
  
  const open = () => isOpen.value = true
  const close = () => isOpen.value = false
  
  return { isOpen, open, close }
}
```

## 🔄 상태 관리 패턴

### Service Layer Pattern
API 호출을 서비스 레이어로 분리:

```typescript
// services/calendar.ts
export class CalendarService {
  async getEvents(params: SearchParams): Promise<EventListResponse> {
    return await kongApi.get<EventListResponse>('/api/events', { params })
  }
}

// composables/useCalendar.ts
export function useCalendar() {
  const events = ref<EventResponse[]>([])
  
  const loadEvents = async () => {
    try {
      const response = await calendarService.getEvents()
      events.value = response.events
    } catch (error) {
      // 에러 처리
    }
  }
  
  return { events, loadEvents }
}
```

## 🚦 라우팅

타입 안전한 라우팅 설정:

```typescript
// router/index.ts
const routes: RouteRecordRaw[] = [
  {
    path: '/calendar',
    name: 'Calendar',
    component: () => import('@/views/CalendarView.vue'),
    meta: { requiresAuth: true }
  }
]

// 네비게이션 가드
router.beforeEach((to) => {
  const { isAuthenticated } = useAuth()
  
  if (to.meta.requiresAuth && !isAuthenticated.value) {
    return '/auth'
  }
})
```

## 🎯 성능 최적화

### 1. 코드 스플리팅
```typescript
// 라우트 레벨 코드 스플리팅
const CalendarView = () => import('@/views/CalendarView.vue')
```

### 2. 컴포넌트 최적화
```vue
<script setup lang="ts">
// computed 활용
const filteredEvents = computed(() => {
  return events.value.filter(event => 
    event.title.includes(searchQuery.value)
  )
})

// 불필요한 re-render 방지
const eventCardProps = computed(() => ({
  event: props.event,
  readonly: props.readonly
}))
</script>
```

## 🔧 개발 도구

### VS Code 권장 확장
- **Vue Language Features (Volar)**
- **TypeScript Vue Plugin (Volar)**
- **Tailwind CSS IntelliSense**
- **Auto Rename Tag**

### 설정 파일
```json
// .vscode/settings.json
{
  "typescript.preferences.importModuleSpecifier": "relative",
  "vue.codeActions.enabled": true,
  "tailwindCSS.includeLanguages": {
    "vue": "html",
    "vue-html": "html"
  }
}
```

## 🐛 디버깅

### Vue DevTools
Vue 3 DevTools를 사용하여 상태를 모니터링할 수 있습니다.

### 로그 레벨
```typescript
// config/app.config.ts
export const APP_CONFIG = {
  LOG_LEVEL: import.meta.env.DEV ? 'debug' : 'error'
}

// 서비스에서 로깅
console.log('📅 이벤트 로드 성공:', events.length, '개')
```

## 🚀 배포

### 빌드 최적화
```bash
# 프로덕션 빌드
npm run build

# 빌드 결과 확인
ls -la dist/
```

### 환경 변수
```bash
# .env.production
VITE_API_BASE_URL=https://api.tsportal.com
VITE_APP_VERSION=1.4.0
```

## 📈 향후 계획

- [ ] **PWA 지원** - 오프라인 캐싱, 푸시 알림
- [ ] **다크 테마** - 테마 전환 기능
- [ ] **국제화 (i18n)** - 다국어 지원
- [ ] **E2E 테스트** - Playwright 도입
- [ ] **Storybook** - 컴포넌트 문서화

---

**Version**: 1.4.0  
**Last Updated**: 2025-07-02  
**Port**: 5174 (Development)  
**Build Tool**: Vite 5  
**Framework**: Vue 3 + TypeScript