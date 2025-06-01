<script setup lang="ts">
// 홈페이지 로직
</script>

<template>
  <div class="space-y-6">
    <!-- Welcome Section -->
    <div>
      <h2 class="text-3xl font-bold text-gray-900 mb-2">안녕하세요! TS팀 포탈입니다 🎉</h2>
      <p class="text-gray-600">Saltware CSG TS팀의 모든 정보를 한곳에서 확인하세요.</p>
    </div>

    <!-- Dashboard Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- AWS 꿀팁 카드 -->
      <router-link 
        to="/aws-tips"
        class="bg-white rounded-xl shadow-lg border border-gray-200 p-6 hover:shadow-xl transition-shadow cursor-pointer"
      >
        <div class="flex items-center mb-4">
          <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-orange-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 ml-3">오늘의 AWS 꿀팁</h3>
        </div>
        <p class="text-gray-600 text-sm mb-4">
          매일 업데이트되는 AWS 서비스 활용 팁과 모범 사례들을 확인해보세요.
        </p>
        <div class="flex items-center text-blue-600 text-sm font-medium">
          더 보기 →
        </div>
      </router-link>

      <!-- TS 주요 이벤트 카드 -->
      <router-link 
        to="/events"
        class="bg-white rounded-xl shadow-lg border border-gray-200 p-6 hover:shadow-xl transition-shadow cursor-pointer"
      >
        <div class="flex items-center mb-4">
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 ml-3">TS 주요 이벤트</h3>
        </div>
        <p class="text-gray-600 text-sm mb-4">
          팀 회의, 교육 세션, 중요 마일스톤 등 놓치면 안 되는 이벤트들을 확인하세요.
        </p>
        <div class="flex items-center text-blue-600 text-sm font-medium">
          더 보기 →
        </div>
      </router-link>

      <!-- 오늘의 점심 추천 카드 -->
      <router-link 
        to="/lunch"
        class="bg-white rounded-xl shadow-lg border border-gray-200 p-6 hover:shadow-xl transition-shadow cursor-pointer"
      >
        <div class="flex items-center mb-4">
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C20.832 18.477 19.246 18 17.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 ml-3">오늘의 점심 추천</h3>
        </div>
        <p class="text-gray-600 text-sm mb-4">
          주변 맛집 정보와 팀원들의 추천 메뉴를 확인하고 점심 고민을 해결하세요.
        </p>
        <div class="flex items-center text-blue-600 text-sm font-medium">
          더 보기 →
        </div>
      </router-link>
    </div>
  </div>
</template>

<style scoped>
/* 추가 스타일이 필요한 경우 여기에 작성 */
</style> 