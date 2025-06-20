<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 반응형 데이터
const loading = ref(false)

// 새로고침 함수
const refreshRecommendations = async () => {
  loading.value = true
  try {
    // TODO: 네이버 지도 API 연동 후 맛집 데이터 가져오기
    await new Promise(resolve => setTimeout(resolve, 1000)) // 임시 로딩 시뮬레이션
  } catch (error) {
    console.error('추천 맛집을 가져오는 중 오류가 발생했습니다:', error)
  } finally {
    loading.value = false
  }
}

// 컴포넌트 마운트 시 실행
onMounted(() => {
  // TODO: 네이버 지도 API 초기화
  console.log('점심 추천 페이지 로드됨 - 네이버 지도 API 연동 예정')
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 컴팩트 헤더 -->
    <div class="bg-white border-b border-gray-200 px-6 py-3">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-xl font-bold text-gray-900">점심 추천</h1>
          <p class="text-sm text-gray-500">맛있는 점심을 찾아보세요</p>
        </div>
        
        <!-- 컴팩트 통계 및 컨트롤 -->
        <div class="flex items-center space-x-4">
          <!-- 통계 -->
          <div class="flex items-center space-x-3">
            <div class="text-center">
              <div class="text-sm font-semibold text-blue-600">0</div>
              <div class="text-xs text-gray-500">추천</div>
            </div>
            <div class="text-center">
              <div class="text-sm font-semibold text-green-600">준비중</div>
              <div class="text-xs text-gray-500">지도</div>
            </div>
          </div>
          
          <!-- 구분선 -->
          <div class="h-8 w-px bg-gray-300"></div>
          
          <button 
            @click="refreshRecommendations"
            :disabled="loading"
            class="px-3 py-1.5 bg-orange-600 text-white rounded-md hover:bg-orange-700 disabled:opacity-50 transition-colors text-sm"
          >
            <svg v-if="loading" class="animate-spin -ml-1 mr-1 h-3 w-3 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            새로고침
          </button>
        </div>
      </div>
    </div>

    <!-- 메인 컨텐츠 -->
    <div class="p-6 space-y-6">
      <!-- 지도 영역 -->
      <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200 bg-gray-50">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-semibold text-gray-900">주변 맛집 지도</h3>
              <p class="text-sm text-gray-500">네이버 지도 API 연동 예정</p>
            </div>
            <div class="flex items-center space-x-2">
              <div class="px-2 py-1 bg-orange-100 text-orange-600 rounded-full text-xs font-semibold">
                🗺️ 지도
              </div>
            </div>
          </div>
        </div>
        <div id="map" class="h-96 bg-gray-100 flex items-center justify-center">
          <div class="text-center">
            <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-1.447-.894L15 4m0 13V4m0 0L9 7" />
            </svg>
            <p class="text-gray-500 text-lg">네이버 지도 API 연결 예정</p>
            <p class="text-gray-400 text-sm mt-2">주변 맛집을 지도에서 확인하실 수 있습니다</p>
          </div>
        </div>
      </div>

      <!-- 추천 목록 영역 -->
      <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200 bg-gray-50">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-semibold text-gray-900">추천 맛집</h3>
              <p class="text-sm text-gray-500">네이버 지도 API와 연동하여 추천</p>
            </div>
            <div class="flex items-center space-x-2">
              <div class="px-2 py-1 bg-green-100 text-green-600 rounded-full text-xs font-semibold">
                🍽️ 맛집
              </div>
            </div>
          </div>
        </div>
        <div class="p-8">
          <div class="text-center">
            <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            <p class="text-gray-500 text-lg">맛집 추천 기능 준비 중</p>
            <p class="text-gray-400 text-sm mt-2">네이버 지도 API와 연동하여 주변 맛집을 추천해드릴 예정입니다</p>
          </div>
        </div>
      </div>

      <!-- 기능 안내 -->
      <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">💡 점심 추천 서비스 안내</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600">
          <div class="space-y-2">
            <div class="flex items-start space-x-2">
              <svg class="w-4 h-4 text-green-500 mt-0.5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>현재 위치 기반 맛집 추천</span>
            </div>
            <div class="flex items-start space-x-2">
              <svg class="w-4 h-4 text-green-500 mt-0.5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>네이버 지도 연동 서비스</span>
            </div>
          </div>
          <div class="space-y-2">
            <div class="flex items-start space-x-2">
              <svg class="w-4 h-4 text-green-500 mt-0.5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>거리 및 평점 정보 제공</span>
            </div>
            <div class="flex items-start space-x-2">
              <svg class="w-4 h-4 text-green-500 mt-0.5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>실시간 맛집 정보 업데이트</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 점심 추천 페이지 전용 스타일 */

/* 카드 호버 효과 */
.hover-card {
  transition: all 0.3s ease;
}

.hover-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* 버튼 애니메이션 */
button {
  transition: all 0.2s ease;
}

button:hover:not(:disabled) {
  transform: translateY(-1px);
}

button:active:not(:disabled) {
  transform: translateY(0);
}
</style> 