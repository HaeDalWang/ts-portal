<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import authService from '@/services/authService'

const route = useRoute()
const router = useRouter()
const isSidebarCollapsed = ref(false)

// 현재 사용자 정보를 반응형 ref로 관리
const currentUser = ref(authService.getUser())

// 라우트 변경 시 사용자 정보 업데이트
watch(route, () => {
  const user = authService.getUser()
  currentUser.value = user
  console.log('👤 사용자 정보 업데이트:', user)
}, { immediate: true })

// 컴포넌트 마운트 시 사용자 정보 로드
onMounted(() => {
  currentUser.value = authService.getUser()
})

const toggleSidebarCollapse = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

const logout = () => {
  console.log('🚪 로그아웃 실행')
  authService.logout()
  currentUser.value = null // 즉시 UI 업데이트
  console.log('👤 사용자 정보 초기화:', currentUser.value)
  router.push('/login')
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- 사이드바 -->
    <div
      :class="[
        'bg-white shadow-lg transition-all duration-300 ease-in-out flex flex-col',
        isSidebarCollapsed ? 'w-16' : 'w-52'
      ]"
    >
      <!-- 사이드바 헤더 -->
      <div :class="['flex items-center h-16 border-b border-gray-200', isSidebarCollapsed ? 'justify-center px-2' : 'justify-between px-4']">
        <!-- TS 로고 (펼쳐진 상태에서만 표시) -->
        <div v-if="!isSidebarCollapsed" class="flex items-center">
          <div 
            :class="[
              'flex items-center justify-center font-bold text-white rounded-lg shadow-md transition-all duration-300',
              'bg-gradient-to-br from-blue-500 to-blue-600',
              'w-8 h-8 text-xs'
            ]"
          >
            TS
          </div>
        </div>

        <!-- 접기/펴기 버튼 (펼쳐진 상태) -->
        <button
          v-if="!isSidebarCollapsed"
          @click="toggleSidebarCollapse"
          :class="[
            'p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 transition-colors'
          ]"
        >
          <svg 
            :class="[
              'w-5 h-5 transition-transform duration-300'
            ]" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
          </svg>
        </button>
        
        <!-- 펼치기 버튼 (접힌 상태) -->
        <button
          v-if="isSidebarCollapsed"
          @click="toggleSidebarCollapse"
          class="w-full h-full flex items-center justify-center hover:bg-gray-50 transition-colors"
        >
          <svg 
            class="w-4 h-4 text-gray-400" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      <!-- 사이드바 메뉴 -->
      <nav :class="['mt-6 flex-1', isSidebarCollapsed ? 'px-1' : 'px-4']">
        <div :class="isSidebarCollapsed ? 'space-y-1' : 'space-y-2'">
          <!-- 홈 -->
          <div class="relative group">
            <router-link
              to="/"
              :class="[
                'flex items-center text-sm font-medium rounded-lg transition-all duration-200',
                isSidebarCollapsed ? 'justify-center w-12 h-10 mx-auto' : 'px-4 py-3',
                route.name === 'home' 
                  ? 'bg-blue-100 text-blue-700' 
                  : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
              ]"
            >
              <svg class="w-5 h-5 flex-shrink-0" :class="isSidebarCollapsed ? '' : 'mr-3'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              <span v-if="!isSidebarCollapsed" class="transition-all duration-300">홈</span>
            </router-link>
            <!-- 툴팁 -->
            <div 
              v-if="isSidebarCollapsed"
              class="absolute left-full top-1/2 transform -translate-y-1/2 ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-50"
            >
              홈
            </div>
          </div>

          <!-- AWS 소식 -->
          <div class="relative group">
            <router-link
              to="/aws-tips"
              :class="[
                'flex items-center text-sm font-medium rounded-lg transition-all duration-200',
                isSidebarCollapsed ? 'justify-center w-12 h-10 mx-auto' : 'px-4 py-3',
                route.name === 'aws-tips' 
                  ? 'bg-orange-100 text-orange-700' 
                  : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
              ]"
            >
              <svg class="w-5 h-5 flex-shrink-0" :class="isSidebarCollapsed ? '' : 'mr-3'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              <span v-if="!isSidebarCollapsed" class="transition-all duration-300">오늘의 AWS 소식</span>
            </router-link>
            <!-- 툴팁 -->
            <div 
              v-if="isSidebarCollapsed"
              class="absolute left-full top-1/2 transform -translate-y-1/2 ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-50"
            >
              오늘의 AWS 소식
            </div>
          </div>

          <!-- TS 공지사항 -->
          <div class="relative group">
            <router-link
              to="/notices"
              :class="[
                'flex items-center text-sm font-medium rounded-lg transition-all duration-200',
                isSidebarCollapsed ? 'justify-center w-12 h-10 mx-auto' : 'px-4 py-3',
                route.name === 'notices' 
                  ? 'bg-blue-100 text-blue-700' 
                  : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
              ]"
            >
              <svg class="w-5 h-5 flex-shrink-0" :class="isSidebarCollapsed ? '' : 'mr-3'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z" />
              </svg>
              <span v-if="!isSidebarCollapsed" class="transition-all duration-300">TS 공지사항</span>
            </router-link>
            <!-- 툴팁 -->
            <div 
              v-if="isSidebarCollapsed"
              class="absolute left-full top-1/2 transform -translate-y-1/2 ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-50"
            >
              TS 공지사항
            </div>
          </div>

          <!-- 점심 추천 -->
          <div class="relative group">
            <router-link
              to="/lunch"
              :class="[
                'flex items-center text-sm font-medium rounded-lg transition-all duration-200',
                isSidebarCollapsed ? 'justify-center w-12 h-10 mx-auto' : 'px-4 py-3',
                route.name === 'lunch' 
                  ? 'bg-green-100 text-green-700' 
                  : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
              ]"
            >
              <svg class="w-5 h-5 flex-shrink-0" :class="isSidebarCollapsed ? '' : 'mr-3'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C20.832 18.477 19.246 18 17.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
              <span v-if="!isSidebarCollapsed" class="transition-all duration-300">오늘의 점심 추천</span>
            </router-link>
            <!-- 툴팁 -->
            <div 
              v-if="isSidebarCollapsed"
              class="absolute left-full top-1/2 transform -translate-y-1/2 ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-50"
            >
              오늘의 점심 추천
            </div>
          </div>

          <!-- 구분선 -->
          <div :class="['border-t border-gray-200', isSidebarCollapsed ? 'my-2 mx-3' : 'my-4 mx-0']"></div>

          <!-- 팀원 프로필 -->
          <div class="relative group">
            <router-link
              to="/team"
              :class="[
                'flex items-center text-sm font-medium rounded-lg transition-all duration-200',
                isSidebarCollapsed ? 'justify-center w-12 h-10 mx-auto' : 'px-4 py-3',
                route.name === 'team' 
                  ? 'bg-purple-100 text-purple-700' 
                  : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
              ]"
            >
              <svg class="w-5 h-5 flex-shrink-0" :class="isSidebarCollapsed ? '' : 'mr-3'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <span v-if="!isSidebarCollapsed" class="transition-all duration-300">팀원 프로필</span>
            </router-link>
            <!-- 툴팁 -->
            <div 
              v-if="isSidebarCollapsed"
              class="absolute left-full top-1/2 transform -translate-y-1/2 ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-50"
            >
              팀원 프로필
            </div>
          </div>

          <!-- 팀 대시보드 -->
          <div class="relative group">
            <router-link
              to="/dashboard"
              :class="[
                'flex items-center text-sm font-medium rounded-lg transition-all duration-200',
                isSidebarCollapsed ? 'justify-center w-12 h-10 mx-auto' : 'px-4 py-3',
                route.name === 'dashboard' 
                  ? 'bg-indigo-100 text-indigo-700' 
                  : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
              ]"
            >
              <svg class="w-5 h-5 flex-shrink-0" :class="isSidebarCollapsed ? '' : 'mr-3'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span v-if="!isSidebarCollapsed" class="transition-all duration-300">팀 대시보드</span>
            </router-link>
            <!-- 툴팁 -->
            <div 
              v-if="isSidebarCollapsed"
              class="absolute left-full top-1/2 transform -translate-y-1/2 ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-50"
            >
              팀 대시보드
            </div>
          </div>

          <!-- MSP 관리 -->
          <div class="relative group">
            <router-link
              to="/msp"
              :class="[
                'flex items-center text-sm font-medium rounded-lg transition-all duration-200',
                isSidebarCollapsed ? 'justify-center w-12 h-10 mx-auto' : 'px-4 py-3',
                route.name === 'msp' 
                  ? 'bg-teal-100 text-teal-700' 
                  : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
              ]"
            >
              <svg class="w-5 h-5 flex-shrink-0" :class="isSidebarCollapsed ? '' : 'mr-3'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-5 0H9m11 0a2 2 0 01-2 2H7a2 2 0 01-2-2m2-2h2m8 0h2" />
              </svg>
              <span v-if="!isSidebarCollapsed" class="transition-all duration-300">MSP 관리</span>
            </router-link>
            <!-- 툴팁 -->
            <div 
              v-if="isSidebarCollapsed"
              class="absolute left-full top-1/2 transform -translate-y-1/2 ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-50"
            >
              MSP 관리
            </div>
          </div>

          <!-- 관리자 페이지 -->
          <div v-if="currentUser && (currentUser.role === 'admin' || currentUser.role === 'power_user') && currentUser.is_active" class="relative group">
            <router-link
              to="/admin"
              :class="[
                'flex items-center text-sm font-medium rounded-lg transition-all duration-200 bg-red-50 border border-red-200',
                isSidebarCollapsed ? 'justify-center w-12 h-10 mx-auto' : 'px-4 py-3',
                route.name === 'admin' 
                  ? 'bg-red-100 text-red-700' 
                  : 'text-red-600 hover:bg-red-100 hover:text-red-700'
              ]"
            >
              <svg class="w-5 h-5 flex-shrink-0" :class="isSidebarCollapsed ? '' : 'mr-3'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <span v-if="!isSidebarCollapsed" class="transition-all duration-300">
                {{ currentUser.role === 'admin' ? '관리자 페이지' : '파워유저 페이지' }}
              </span>
            </router-link>
            <!-- 툴팁 -->
            <div 
              v-if="isSidebarCollapsed"
              class="absolute left-full top-1/2 transform -translate-y-1/2 ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-50"
            >
              {{ currentUser.role === 'admin' ? '관리자 페이지' : '파워유저 페이지' }}
            </div>
          </div>

          <!-- 내 프로필 -->
          <div class="relative group">
            <router-link
              to="/profile"
              :class="[
                'flex items-center text-sm font-medium rounded-lg transition-all duration-200',
                isSidebarCollapsed ? 'justify-center w-12 h-10 mx-auto' : 'px-4 py-3',
                route.name === 'profile' 
                  ? 'bg-gray-100 text-gray-700' 
                  : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
              ]"
            >
              <svg class="w-5 h-5 flex-shrink-0" :class="isSidebarCollapsed ? '' : 'mr-3'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <span v-if="!isSidebarCollapsed" class="transition-all duration-300">내 프로필</span>
            </router-link>
            <!-- 툴팁 -->
            <div 
              v-if="isSidebarCollapsed"
              class="absolute left-full top-1/2 transform -translate-y-1/2 ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-50"
            >
              내 프로필
            </div>
          </div>
          
          <!-- 로그아웃 -->
          <div class="relative group mt-1">
            <button
              @click="logout"
              :class="[
                'w-full flex items-center text-sm font-medium rounded-lg transition-all duration-200 text-red-600 hover:bg-red-50 hover:text-red-700',
                isSidebarCollapsed ? 'justify-center h-10 mx-auto' : 'px-4 py-3'
              ]"
            >
              <svg class="w-5 h-5 flex-shrink-0" :class="isSidebarCollapsed ? '' : 'mr-3'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              <span v-if="!isSidebarCollapsed" class="transition-all duration-300">로그아웃</span>
            </button>
            <!-- 툴팁 -->
            <div 
              v-if="isSidebarCollapsed"
              class="absolute left-full top-1/2 transform -translate-y-1/2 ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-50"
            >
              로그아웃
            </div>
          </div>
        </div>
      </nav>
    </div>

    <!-- 메인 컨텐츠 영역 -->
    <div class="flex-1 flex flex-col">
      <!-- 페이지 컨텐츠 -->
      <main class="flex-1 p-4">
        <div class="max-w-7xl mx-auto">
          <RouterView />
        </div>
      </main>

      <!-- 푸터 -->
      <footer class="bg-white border-t border-gray-200 py-4">
        <div class="max-w-7xl mx-auto px-8">
          <p class="text-center text-sm text-gray-500">
            © Saltware CSG - TS Team Portal, created by <a href="https://github.com/HaedalWang" class="text-blue-500 hover:text-blue-600">HaedalWang</a>
          </p>
        </div>
      </footer>
    </div>
  </div>
</template>

<style scoped>
/* 추가 커스텀 스타일이 필요한 경우 여기에 작성 */
</style>
