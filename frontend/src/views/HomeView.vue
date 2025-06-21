<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { api } from '@/services/api'
import authService from '@/services/authService'

// 현재 날짜와 시간 정보
const today = computed(() => {
  const now = new Date()
  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  }
  return now.toLocaleDateString('ko-KR', options)
})

const currentTime = computed(() => {
  const now = new Date()
  return now.toLocaleTimeString('ko-KR', { 
    hour: '2-digit', 
    minute: '2-digit',
    hour12: false
  })
})

const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return '좋은 아침입니다! ☀️'
  if (hour < 18) return '좋은 오후입니다! 🌤️'
  return '좋은 저녁입니다! 🌙'
})

// 사용자 정보
const currentUser = computed(() => authService.getUser())

const userName = computed(() => {
  return currentUser.value?.name || '사용자'
})

const userInitials = computed(() => {
  if (!currentUser.value?.name) return 'U'
  return currentUser.value.name
    .split(' ')
    .map(word => word.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2)
})

// 통계 데이터
const stats = ref({
  members: 0,  // API에서 가져올 값
  customers: 0 // API에서 가져올 값
})

const isLoading = ref(true)

// 통계 데이터 로드
const loadStats = async () => {
  try {
    isLoading.value = true
    
    // 팀원 수 조회
    const membersResponse = await api.get('/members/')
    stats.value.members = Array.isArray(membersResponse) ? membersResponse.length : 0
    
    // 고객사 수 조회
    const customersResponse = await api.get('/customers/')
    stats.value.customers = Array.isArray(customersResponse) ? customersResponse.length : 0
    
  } catch (error) {
    console.error('통계 데이터 로드 실패:', error)
    // 에러 시 기본값 유지
    stats.value.members = 0
    stats.value.customers = 0
  } finally {
    isLoading.value = false
  }
}

// 컴포넌트 마운트 시 데이터 로드
onMounted(() => {
  loadStats()
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 확장된 헤더 -->
    <div class="bg-gradient-to-r from-purple-500 to-blue-600 px-6 py-6 text-white rounded-b-xl">
      <div class="flex items-center justify-between">
        <div class="flex-1">
          <div class="mb-3">
            <h1 class="text-2xl font-bold text-white">{{ greeting }}</h1>
            <p class="text-purple-100 text-sm">Saltware CSG TS팀 통합 관리 플랫폼</p>
          </div>
          
          <div class="flex items-center space-x-4 text-xs text-purple-100">
            <div class="flex items-center space-x-2">
              <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span>{{ today }}</span>
            </div>
            <div class="flex items-center space-x-2">
              <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>{{ currentTime }}</span>
            </div>
          </div>
        </div>
        
        <!-- 통계 정보 -->
        <div class="flex items-center space-x-8">
          <div class="text-center">
            <div class="text-lg font-bold text-white">
              {{ isLoading ? '...' : stats.members }}
            </div>
            <div class="text-xs text-purple-100">팀원</div>
          </div>
          <div class="text-center">
            <div class="text-lg font-bold text-white">
              {{ isLoading ? '...' : stats.customers }}
            </div>
            <div class="text-xs text-purple-100">고객사</div>
          </div>
          
          <!-- 프로필 버튼 -->
          <router-link 
            to="/profile"
            class="flex items-center space-x-2 bg-white/10 hover:bg-white/20 rounded-lg px-3 py-2 transition-colors"
          >
            <div class="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center text-white text-sm font-bold">
              {{ userInitials }}
            </div>
            <div class="text-left">
              <div class="text-xs font-medium text-white">{{ userName }}</div>
              <div class="text-xs text-purple-100">프로필</div>
            </div>
          </router-link>
        </div>
      </div>
    </div>

    <!-- 메인 컨텐츠 -->
    <div class="p-6">
      <!-- Dashboard Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <!-- AWS 소식 카드 -->
        <router-link 
          to="/aws-tips"
          class="bg-white rounded-xl shadow-lg border border-gray-200 p-4 hover:shadow-xl transition-shadow cursor-pointer"
        >
          <div class="flex items-center space-x-3 mb-3">
            <div class="w-10 h-10 bg-gradient-to-br from-orange-400 to-orange-600 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <div class="flex-1">
              <h3 class="text-sm font-semibold text-gray-900">AWS 소식</h3>
              <p class="text-xs text-gray-600">최신 AWS 뉴스 및 업데이트</p>
            </div>
            <div class="bg-orange-100 text-orange-600 text-xs px-2 py-1 rounded-full font-medium">
              NEW
            </div>
          </div>
          
          <p class="text-xs text-gray-600 mb-3">
            매일 업데이트되는 AWS 서비스 활용 팁과 모범 사례들을 확인해보세요.
          </p>
          
          <div class="flex items-center text-orange-600 text-xs font-medium">
            더 보기 →
          </div>
        </router-link>

        <!-- TS 공지사항 카드 -->
        <router-link 
          to="/notices"
          class="bg-white rounded-xl shadow-lg border border-gray-200 p-4 hover:shadow-xl transition-shadow cursor-pointer"
        >
          <div class="flex items-center space-x-3 mb-3">
            <div class="w-10 h-10 bg-gradient-to-br from-blue-400 to-blue-600 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z" />
              </svg>
            </div>
            <div class="flex-1">
              <h3 class="text-sm font-semibold text-gray-900">TS 공지사항</h3>
              <p class="text-xs text-gray-600">팀 공지 및 중요 알림</p>
            </div>
            <div class="bg-blue-100 text-blue-600 text-xs px-2 py-1 rounded-full font-medium">
              중요
            </div>
          </div>
          
          <p class="text-xs text-gray-600 mb-3">
            팀장님의 중요 공지사항과 주의사항들을 확인하고 놓치지 마세요.
          </p>
          
          <div class="flex items-center text-blue-600 text-xs font-medium">
            더 보기 →
          </div>
        </router-link>

        <!-- 점심 추천 카드 -->
        <router-link 
          to="/lunch"
          class="bg-white rounded-xl shadow-lg border border-gray-200 p-4 hover:shadow-xl transition-shadow cursor-pointer"
        >
          <div class="flex items-center space-x-3 mb-3">
            <div class="w-10 h-10 bg-gradient-to-br from-green-400 to-green-600 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C20.832 18.477 19.246 18 17.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
            <div class="flex-1">
              <h3 class="text-sm font-semibold text-gray-900">점심 추천</h3>
              <p class="text-xs text-gray-600">오늘의 맛집 추천</p>
            </div>
          </div>
          
          <p class="text-xs text-gray-600 mb-3">
            주변 맛집 정보와 팀원들의 추천 메뉴를 확인하고 점심 고민을 해결하세요.
          </p>
          
          <div class="flex items-center text-green-600 text-xs font-medium">
            더 보기 →
          </div>
        </router-link>

        <!-- 팀원 프로필 카드 -->
        <router-link 
          to="/team"
          class="bg-white rounded-xl shadow-lg border border-gray-200 p-4 hover:shadow-xl transition-shadow cursor-pointer"
        >
          <div class="flex items-center space-x-3 mb-3">
            <div class="w-10 h-10 bg-gradient-to-br from-purple-400 to-purple-600 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <div class="flex-1">
              <h3 class="text-sm font-semibold text-gray-900">팀원 프로필</h3>
              <p class="text-xs text-gray-600">팀원 정보 및 조직도</p>
            </div>
          </div>
          
          <p class="text-xs text-gray-600 mb-3">
            팀원들의 프로필과 조직도를 확인하고 연락처 정보를 찾아보세요.
          </p>
          
          <div class="flex items-center text-purple-600 text-xs font-medium">
            더 보기 →
          </div>
        </router-link>

        <!-- 팀 대시보드 카드 -->
        <router-link 
          to="/dashboard"
          class="bg-white rounded-xl shadow-lg border border-gray-200 p-4 hover:shadow-xl transition-shadow cursor-pointer"
        >
          <div class="flex items-center space-x-3 mb-3">
            <div class="w-10 h-10 bg-gradient-to-br from-indigo-400 to-indigo-600 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div class="flex-1">
              <h3 class="text-sm font-semibold text-gray-900">팀 대시보드</h3>
              <p class="text-xs text-gray-600">일정 관리 및 현황</p>
            </div>
          </div>
          
          <p class="text-xs text-gray-600 mb-3">
            달력 기반 팀 전체 일정과 현황을 한눈에 확인할 수 있습니다.
          </p>
          
          <div class="flex items-center text-indigo-600 text-xs font-medium">
            더 보기 →
          </div>
        </router-link>

        <!-- MSP 관리 카드 -->
        <router-link 
          to="/msp"
          class="bg-white rounded-xl shadow-lg border border-gray-200 p-4 hover:shadow-xl transition-shadow cursor-pointer"
        >
          <div class="flex items-center space-x-3 mb-3">
            <div class="w-10 h-10 bg-gradient-to-br from-teal-400 to-teal-600 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-5 0H9m11 0a2 2 0 01-2 2H7a2 2 0 01-2-2m2-2h2m8 0h2" />
              </svg>
            </div>
            <div class="flex-1">
              <h3 class="text-sm font-semibold text-gray-900">MSP 관리</h3>
              <p class="text-xs text-gray-600">고객사 담당 현황</p>
            </div>
          </div>
          
          <p class="text-xs text-gray-600 mb-3">
            보드 기반으로 팀원별 고객사 담당 현황을 관리하고 확인하세요.
          </p>
          
          <div class="flex items-center text-teal-600 text-xs font-medium">
            더 보기 →
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

 