<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const isSidebarCollapsed = ref(false)

const toggleSidebarCollapse = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- 사이드바 -->
    <div
      :class="[
        'bg-white shadow-lg transition-all duration-300 ease-in-out',
        isSidebarCollapsed ? 'w-16' : 'w-64'
      ]"
    >
      <!-- 사이드바 헤더 -->
      <div :class="['flex items-center h-16 border-b border-gray-200', isSidebarCollapsed ? 'justify-center px-2' : 'justify-between px-4']">
        <h1 
          :class="[
            'font-bold text-gray-900 transition-all duration-300',
            isSidebarCollapsed ? 'opacity-0 text-sm' : 'opacity-100 text-xl'
          ]"
        >
          <span class="text-blue-600">TS</span><span :class="isSidebarCollapsed ? 'hidden' : ''"> - 포탈</span>
        </h1>

        <!-- 접기/펴기 버튼 -->
        <button
          @click="toggleSidebarCollapse"
          :class="[
            'p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 transition-colors',
            isSidebarCollapsed ? 'p-3' : ''
          ]"
        >
          <svg 
            :class="[
              'w-5 h-5 transition-transform duration-300',
              isSidebarCollapsed ? 'rotate-180' : ''
            ]" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
          </svg>
        </button>
      </div>

      <!-- 사이드바 메뉴 -->
      <nav :class="['mt-8', isSidebarCollapsed ? 'px-2' : 'px-4']">
        <div class="space-y-2">
          <!-- 홈 -->
          <div class="relative group">
            <router-link
              to="/"
              :class="[
                'flex items-center text-sm font-medium rounded-lg transition-all duration-200',
                isSidebarCollapsed ? 'justify-center p-3' : 'px-4 py-3',
                route.name === 'home' 
                  ? 'bg-blue-100 text-blue-700' 
                  : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
              ]"
            >
              <svg class="w-5 h-5 flex-shrink-0" :class="isSidebarCollapsed ? '' : 'mr-3'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              <span 
                :class="[
                  'transition-all duration-300',
                  isSidebarCollapsed ? 'opacity-0 w-0' : 'opacity-100'
                ]"
              >
                홈
              </span>
            </router-link>
            <!-- 툴팁 -->
            <div 
              v-if="isSidebarCollapsed"
              class="absolute left-full top-1/2 transform -translate-y-1/2 ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-50"
            >
              홈
            </div>
          </div>

          <!-- AWS 꿀팁 -->
          <div class="relative group">
            <router-link
              to="/aws-tips"
              :class="[
                'flex items-center text-sm font-medium rounded-lg transition-all duration-200',
                isSidebarCollapsed ? 'justify-center p-3' : 'px-4 py-3',
                route.name === 'aws-tips' 
                  ? 'bg-orange-100 text-orange-700' 
                  : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
              ]"
            >
              <svg class="w-5 h-5 flex-shrink-0" :class="isSidebarCollapsed ? '' : 'mr-3'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              <span 
                :class="[
                  'transition-all duration-300',
                  isSidebarCollapsed ? 'opacity-0 w-0' : 'opacity-100'
                ]"
              >
                오늘의 AWS 꿀팁
              </span>
            </router-link>
            <!-- 툴팁 -->
            <div 
              v-if="isSidebarCollapsed"
              class="absolute left-full top-1/2 transform -translate-y-1/2 ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-50"
            >
              오늘의 AWS 꿀팁
            </div>
          </div>

          <!-- TS 이벤트 -->
          <div class="relative group">
            <router-link
              to="/events"
              :class="[
                'flex items-center text-sm font-medium rounded-lg transition-all duration-200',
                isSidebarCollapsed ? 'justify-center p-3' : 'px-4 py-3',
                route.name === 'events' 
                  ? 'bg-blue-100 text-blue-700' 
                  : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
              ]"
            >
              <svg class="w-5 h-5 flex-shrink-0" :class="isSidebarCollapsed ? '' : 'mr-3'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span 
                :class="[
                  'transition-all duration-300',
                  isSidebarCollapsed ? 'opacity-0 w-0' : 'opacity-100'
                ]"
              >
                TS 주요 이벤트
              </span>
            </router-link>
            <!-- 툴팁 -->
            <div 
              v-if="isSidebarCollapsed"
              class="absolute left-full top-1/2 transform -translate-y-1/2 ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-50"
            >
              TS 주요 이벤트
            </div>
          </div>

          <!-- 점심 추천 -->
          <div class="relative group">
            <router-link
              to="/lunch"
              :class="[
                'flex items-center text-sm font-medium rounded-lg transition-all duration-200',
                isSidebarCollapsed ? 'justify-center p-3' : 'px-4 py-3',
                route.name === 'lunch' 
                  ? 'bg-green-100 text-green-700' 
                  : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
              ]"
            >
              <svg class="w-5 h-5 flex-shrink-0" :class="isSidebarCollapsed ? '' : 'mr-3'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C20.832 18.477 19.246 18 17.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
              <span 
                :class="[
                  'transition-all duration-300',
                  isSidebarCollapsed ? 'opacity-0 w-0' : 'opacity-100'
                ]"
              >
                오늘의 점심 추천
              </span>
            </router-link>
            <!-- 툴팁 -->
            <div 
              v-if="isSidebarCollapsed"
              class="absolute left-full top-1/2 transform -translate-y-1/2 ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-50"
            >
              오늘의 점심 추천
            </div>
          </div>
        </div>
      </nav>
    </div>

    <!-- 메인 컨텐츠 영역 -->
    <div class="flex-1 flex flex-col">
      <!-- 페이지 컨텐츠 -->
      <main class="flex-1 p-8">
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
