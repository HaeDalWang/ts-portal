# TS Portal - Frontend

Saltware CSG TS팀의 Portal 사이트 Frontend 프로젝트입니다.

## 📋 프로젝트 개요

- **프로젝트명**: TS Portal
- **버전**: 0.0.0
- **개발환경**: Vue 3 + TypeScript + TailwindCSS
- **빌드도구**: Vite 6

## 🛠 기술 스택 & 버전 정보

### Core Dependencies
```json
{
  "vue": "^3.5.13",
  "vue-router": "^4.5.1"
}
```

### Development Dependencies
```json
{
  "@tsconfig/node22": "^22.0.1",
  "@types/node": "^22.14.0",
  "@vitejs/plugin-vue": "^5.2.3",
  "@vue/tsconfig": "^0.7.0",
  "autoprefixer": "^10.4.21",
  "npm-run-all2": "^7.0.2",
  "postcss": "^8.5.4",
  "tailwindcss": "^3.4.17",
  "typescript": "~5.8.0",
  "vite": "^6.2.4",
  "vite-plugin-vue-devtools": "^7.7.2",
  "vue-tsc": "^2.2.8"
}
```

## 🚀 시작하기

### 설치
```bash
npm install
```

### 개발 서버 실행
```bash
npm run dev
```
→ http://localhost:5173 에서 확인 가능

### 빌드
```bash
npm run build
```

### 타입 체크
```bash
npm run type-check
```

## 📁 프로젝트 구조

```
src/
├── App.vue              # 메인 애플리케이션 컴포넌트
├── main.ts              # 애플리케이션 엔트리 포인트
├── assets/
│   └── main.css         # TailwindCSS 전역 스타일
├── components/          # 재사용 가능한 컴포넌트들
├── router/
│   └── index.ts         # Vue Router 설정
└── views/               # 페이지 컴포넌트들
    ├── HomeView.vue     # 홈 대시보드
    ├── AwsTipsView.vue  # AWS 꿀팁 페이지
    ├── EventsView.vue   # TS 이벤트 페이지
    └── LunchView.vue    # 점심 추천 페이지
```

## 🎨 UI/UX 특징

### 레이아웃
- **반응형 사이드바**: 접고 펼 수 있는 좌측 네비게이션
  - 데스크톱: 고정 사이드바
  - 모바일: 햄버거 메뉴로 토글
- **현대적인 디자인**: TailwindCSS 기반 클린한 인터페이스

### 네비게이션
- 📱 **홈**: 메인 대시보드 (카드 레이아웃)
- 💡 **오늘의 AWS 꿀팁**: AWS 서비스 활용 팁
- 📅 **TS 주요 이벤트**: 팀 회의, 교육 세션, 마일스톤
- 🍽 **오늘의 점심 추천**: 주변 맛집 정보

### 디자인 시스템
- **색상 테마**: 
  - Primary: Blue (#3B82F6)
  - AWS Tips: Orange (#EA580C)
  - Events: Blue (#2563EB)
  - Lunch: Green (#16A34A)
- **타이포그래피**: 시스템 폰트 스택
- **컴포넌트**: 카드 기반 레이아웃, 호버 효과

## ⚙️ 설정 파일들

### TailwindCSS (`tailwind.config.js`)
```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### PostCSS (`postcss.config.js`)
```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### Vite (`vite.config.ts`)
```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
```

## 🔧 주요 기능

### 1. 사이드바 네비게이션
- Vue Router와 연동된 동적 메뉴
- 현재 페이지 하이라이트
- 모바일 반응형 지원

### 2. 대시보드 카드
- 3개 주요 섹션의 카드형 레이아웃
- 호버 효과와 클릭 시 페이지 이동
- 아이콘과 설명 텍스트 포함

### 3. 반응형 디자인
- 모바일 퍼스트 접근
- Breakpoints: sm(640px), md(768px), lg(1024px)
- 사이드바 토글 기능

## 📝 개발 히스토리

### v0.0.0 (초기 설정)
- ✅ Vue 3 + TypeScript 프로젝트 초기화
- ✅ TailwindCSS v3.4.17 설정 (PostCSS 방식)
- ✅ Vue Router 4.5.1 설정
- ✅ 사이드바 레이아웃 구현
- ✅ 4개 페이지 생성 (홈, AWS꿀팁, 이벤트, 점심)
- ✅ 반응형 디자인 적용

## 🚨 주의사항

### 버전 고정 권장
현재 설정된 버전들로 고정하여 사용하는 것을 권장합니다:
- **Vue**: 3.5.13
- **TailwindCSS**: 3.4.17  
- **Vite**: 6.2.4
- **Vue Router**: 4.5.1

### TailwindCSS v4 호환성
- 현재 TailwindCSS v3 사용 중
- v4로 업그레이드 시 설정 방식이 달라짐 (`@import "tailwindcss"`)

## 🔮 향후 계획

- [ ] AWS 꿀팁 컨텐츠 추가
- [ ] TS 이벤트 캘린더 기능
- [ ] 점심 추천 시스템
- [ ] 사용자 인증 시스템
- [ ] 실시간 알림 기능

---

**개발자**: Saltware CSG TS Team  
**최종 업데이트**: 2024-12-18
