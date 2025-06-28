# TS Portal - Frontend 🎨

> **Vue 3 + TypeScript + TailwindCSS 기반 현대적인 팀 관리 포털**  
> Saltware CSG TS팀의 통합 관리 플랫폼 프론트엔드

![Vue 3](https://img.shields.io/badge/Vue-3.x-4FC08D?style=flat-square&logo=vue.js&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat-square&logo=typescript&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.x-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-6.x-646CFF?style=flat-square&logo=vite&logoColor=white)

## 📋 목차

- [프로젝트 개요](#-프로젝트-개요)
- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)
- [설치 및 실행](#-설치-및-실행)
- [프로젝트 구조](#-프로젝트-구조)
- [개발 가이드](#-개발-가이드)

## 🎯 프로젝트 개요

TS Portal Frontend는 Vue 3의 Composition API와 TypeScript를 활용하여 구축된 현대적인 SPA(Single Page Application)입니다. 팀원 관리, 고객사 관리, 일정 관리 등 팀 운영에 필요한 모든 기능을 직관적인 UI로 제공하며, 역할 기반 접근 제어(RBAC)를 통해 보안과 사용성을 강화했습니다.

### 🌟 핵심 특징
- **타입 안전성**: TypeScript로 런타임 에러 최소화
- **반응형 디자인**: 모든 디바이스에서 최적화된 경험
- **컴포넌트 기반**: 재사용 가능한 모듈형 아키텍처
- **역할 기반 접근 제어**: Admin, Power User, User 역할에 따른 기능 제한

## ✨ 주요 기능

### 🔐 인증 및 권한
- **로그인**: JWT 기반의 안전한 인증 시스템
- **역할별 메뉴**: 사용자의 역할(Admin, Power User, User)에 따라 사이드바 메뉴 동적 렌더링
- **페이지 접근 제어**: 라우터 가드를 통해 권한 없는 페이지 접근 차단

### 🏠 대시보드 홈
- **6개 핵심 카드**: 각 기능별 진입점 제공
- **반응형 그리드**: 화면 크기에 따른 자동 배치

### 👥 팀원 프로필 및 관리
- **내 프로필 수정**: 사용자가 직접 자신의 이메일, 연락처, 기술 스택 수정
- **관리자 페이지 (`AdminView`)**: Admin 및 Power User만 접근 가능
- **팀원 CRUD**: 관리자는 팀원 생성, 정보 수정, 비활성화/삭제 가능
- **듀얼 뷰 모드**: 카드 뷰 ↔ 테이블 뷰 전환
- **검색 및 필터링**: 다양한 조건으로 팀원 검색

### 🏢 MSP 고객사 관리 (`MspView`)
- **고객사 CRUD**: `CustomerCreateModal` 컴포넌트를 통한 고객사 생성 및 수정
- **담당자 배정**: 주/부 담당자를 활성 팀원 목록에서 선택하여 지정
- **기술지원등급 관리**: 계약 상태를 Standard, Advanced, Enterprise 등급으로 관리
- **듀얼 뷰 모드**: 카드 뷰 ↔ 테이블 뷰 전환

### 📅 팀 대시보드 (일정 관리)
- **FullCalendar 통합**: 월/주/일 뷰 지원
- **7가지 이벤트 타입**: 휴가, 재택, 출장 등
- **팀원별 색상 구분**: 동적 색상 생성 알고리즘
- **고급 필터링**: 팀원별, 이벤트 타입별 필터

## 🛠 기술 스택

### Core Framework
- **Vue 3** - Composition API, `<script setup>` 문법
- **TypeScript** - 타입 안전성과 IntelliSense
- **Vue Router** - SPA 라우팅 관리

### Styling & UI
- **TailwindCSS** - 유틸리티 퍼스트 CSS 프레임워크
- **PostCSS** - CSS 후처리 및 최적화

### Development Tools
- **Vite** - 빠른 개발 서버 및 빌드 도구
- **Vue DevTools** - Vue 컴포넌트 디버깅

### External Libraries
- **FullCalendar** - 고급 달력 컴포넌트
- **Axios** - HTTP 클라이언트 (API 통신)

## 🚀 설치 및 실행

### 사전 요구사항
- **Node.js** 18.0.0 이상

### 설치 및 실행
```bash
cd frontend
npm install
npm run dev
```
→ http://localhost:5173 에서 확인 가능

## 📁 프로젝트 구조

```
src/
├── 📄 App.vue                   # 루트 컴포넌트, 라우터 뷰 및 레이아웃 관리
├── 📄 main.ts                   # 애플리케이션 엔트리 포인트, Vue 앱 초기화
├── 🎨 assets/                   # 정적 자원 (CSS, 이미지)
├── 🧩 components/               # 재사용 컴포넌트
│   └── CustomerCreateModal.vue  # 고객사 생성/수정/할당 모달
├── 🛣️ router/
│   └── index.ts                 # Vue Router 설정, 라우트 가드 (인증/권한 체크)
├── 🌐 services/                 # API 서비스 레이어
│   ├── api.ts                   # Axios 인스턴스 설정 및 인터셉터
│   ├── authService.ts           # 인증 관련 API
│   ├── customerService.ts       # 고객사 관리 API
│   └── memberService.ts         # 팀원 관리 API
├── 📝 types/
│   └── index.ts                 # 프로젝트 전역 TypeScript 타입 정의
├── 🛠️ utils/
│   └── permissions.ts           # 역할(Role) 기반 권한 체크 유틸리티
└── 📱 views/                    # 페이지 컴포넌트
    ├── AdminView.vue            # 🔒 관리자 페이지
    ├── MspView.vue              # 🏢 MSP 고객사 관리
    ├── ProfileView.vue          # 👤 내 프로필
    └── LoginView.vue            # 🔑 로그인 페이지
```

## 👨‍💻 개발 가이드

### 🔑 인증 및 권한 처리

1.  **로그인**: `LoginView`에서 `authService.login()`을 호출하여 JWT 토큰을 발급받습니다.
2.  **토큰 저장**: 발급받은 토큰은 `localStorage`에 저장하여 사용자의 세션을 유지합니다.
3.  **API 요청**: `api.ts`의 Axios 요청 인터셉터는 모든 API 요청 헤더에 자동으로 `Authorization: Bearer <token>`을 추가합니다.
4.  **라우트 가드**: `router/index.ts`의 `beforeEach` 가드는 페이지 이동 시 사용자의 인증 상태와 역할을 확인하여 접근을 제어합니다.
5.  **UI 제어**: `utils/permissions.ts`의 유틸리티 함수를 사용하여 컴포넌트 내에서 특정 UI 요소(예: 수정/삭제 버튼)를 사용자의 역할에 따라 표시하거나 숨깁니다.

### 📦 상태 관리

이 프로젝트는 Vue 3의 Composition API 네이티브 기능인 `ref`, `reactive`, `computed`를 사용하여 컴포넌트 내 상태를 관리합니다. 별도의 상태 관리 라이브러리(Vuex, Pinia)는 사용하지 않으며, 필요 시 `provide/inject`를 통해 상태를 공유할 수 있습니다.

### ♻️ 컴포넌트 가이드

#### `CustomerCreateModal.vue`
- **다목적 모달**: 고객사 생성, 수정, 담당자 할당 세 가지 모드를 지원합니다.
- **Props**: `isVisible`, `mode`, `customer`, `members` 등을 받아 동작을 제어합니다.
- **Emits**: `close`, `submit` 이벤트를 통해 부모 컴포넌트(`MspView`)와 통신합니다.
- **유효성 검사**: 필수 입력 필드(회사명, 주담당자 등)에 대한 클라이언트 사이드 유효성 검사를 수행합니다.
