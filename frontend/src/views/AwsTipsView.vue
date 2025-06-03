<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

// 타입 정의
interface DailyTip {
  title: string
  link: string
  summary: string
  published_readable: string
  published: string
  quality_score: number
  tags: string[]
}

interface SelectionMetadata {
  date: string
  weekday: number
  weekday_name: string
  priority_categories: string[]
  selection_reason: string
  backup_used: boolean
  candidate_count: number
  quality_filter_applied: boolean
  selected_category?: string
  category_name?: string
}

interface DailyTipResponse {
  success: boolean
  daily_tip?: DailyTip
  selection_metadata?: SelectionMetadata
  cache_info?: {
    cached: boolean
    cache_date: string
    generated_at: string
  }
  message?: string
  suggestion?: string
}

// 반응형 데이터
const isLoading = ref(true)
const error = ref<string | null>(null)
const dailyTipData = ref<DailyTipResponse | null>(null)
const enableTranslation = ref(false)

// HoneyBox API 설정 - 환경변수 사용
const HONEYBOX_API_URL = import.meta.env.VITE_HONEYBOX_API_URL || 'http://localhost:8000'

// 개발 중 API URL 로깅 (배포시 제거 가능)
console.log('HoneyBox API URL:', HONEYBOX_API_URL)

// 오늘의 소식 가져오기
const fetchDailyTip = async () => {
  try {
    isLoading.value = true
    error.value = null
    
    const url = new URL(`${HONEYBOX_API_URL}/daily-tip`)
    if (enableTranslation.value) {
      url.searchParams.append('translate', 'true')
    }
    
    const response = await fetch(url.toString())
    
    if (!response.ok) {
      throw new Error(`API 오류: ${response.status}`)
    }
    
    const data: DailyTipResponse = await response.json()
    dailyTipData.value = data
    
  } catch (err) {
    console.error('오늘의 소식 가져오기 실패:', err)
    error.value = err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다.'
  } finally {
    isLoading.value = false
  }
}

// 컴포넌트 마운트 시 데이터 로드
onMounted(() => {
  fetchDailyTip()
})

// 품질 점수 표시용 컴퓨티드 프로퍼티
const qualityLevel = computed(() => {
  if (!dailyTipData.value?.daily_tip?.quality_score) return 'unknown'
  const score = dailyTipData.value.daily_tip.quality_score
  
  if (score >= 4) return 'excellent'
  if (score >= 3) return 'good'
  if (score >= 2) return 'fair'
  return 'basic'
})

const qualityColor = computed(() => {
  switch (qualityLevel.value) {
    case 'excellent': return 'text-green-600 bg-green-100'
    case 'good': return 'text-blue-600 bg-blue-100'
    case 'fair': return 'text-yellow-600 bg-yellow-100'
    case 'basic': return 'text-gray-600 bg-gray-100'
    default: return 'text-gray-600 bg-gray-100'
  }
})

const qualityText = computed(() => {
  switch (qualityLevel.value) {
    case 'excellent': return '최고 품질'
    case 'good': return '좋음'
    case 'fair': return '보통'
    case 'basic': return '기본'
    default: return '평가 불가'
  }
})

// 외부 링크 열기
const openExternalLink = (url: string) => {
  window.open(url, '_blank', 'noopener,noreferrer')
}

// 새로고침 함수
const refreshTip = () => {
  fetchDailyTip()
}

// 번역 토글
const toggleTranslation = () => {
  enableTranslation.value = !enableTranslation.value
  fetchDailyTip()
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center space-x-4">
        <div class="w-12 h-12 bg-gradient-to-br from-orange-400 to-orange-600 rounded-lg flex items-center justify-center shadow-lg">
          <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <div>
          <h1 class="text-3xl font-bold text-gray-900">오늘의 AWS 소식</h1>
          <p class="text-gray-600">매일 새로운 AWS 소식과 업데이트를 HoneyBox가 선별해서 전해드립니다</p>
        </div>
      </div>
      <div class="flex items-center space-x-3">
        <!-- 번역 토글 버튼 -->
        <button
          @click="toggleTranslation"
          :class="[
            'flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors',
            enableTranslation 
              ? 'bg-blue-500 hover:bg-blue-600 text-white' 
              : 'bg-gray-200 hover:bg-gray-300 text-gray-700'
          ]"
          :disabled="isLoading"
        >
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
          </svg>
          <span>{{ enableTranslation ? '한글' : '원문' }}</span>
        </button>
        <!-- 새로고침 버튼 -->
        <button
          @click="refreshTip"
          :disabled="isLoading"
          class="bg-orange-500 hover:bg-orange-600 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors"
        >
          <svg 
            class="w-4 h-4" 
            :class="{ 'animate-spin': isLoading }"
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>새로고침</span>
        </button>
      </div>
    </div>

    <!-- 로딩 상태 -->
    <div v-if="isLoading" class="bg-white rounded-xl shadow-lg border border-gray-200 p-8">
      <div class="flex items-center justify-center space-x-3">
        <svg class="animate-spin h-6 w-6 text-orange-600" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span class="text-gray-600">오늘의 AWS 소식을 불러오는 중...</span>
      </div>
    </div>

    <!-- 오류 상태 -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-xl p-6">
      <div class="flex items-center space-x-3 mb-4">
        <svg class="w-6 h-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h3 class="text-lg font-semibold text-red-900">오류 발생</h3>
      </div>
      <p class="text-red-700 mb-4">{{ error }}</p>
      <button 
        @click="refreshTip"
        class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors"
      >
        다시 시도
      </button>
    </div>

    <!-- 성공 상태: 소식이 있는 경우 -->
    <div v-else-if="dailyTipData?.success && dailyTipData.daily_tip" class="space-y-6">
      <!-- 메인 소식 카드 -->
      <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
        <!-- 헤더 -->
        <div class="bg-gradient-to-r from-orange-500 to-orange-600 p-6 text-white">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-xl font-bold mb-2">{{ dailyTipData.daily_tip.title }}</h2>
              <div class="flex items-center space-x-4 text-orange-100">
                <span class="flex items-center space-x-1">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span>{{ dailyTipData.daily_tip.published_readable }}</span>
                </span>
                <div :class="`px-2 py-1 rounded-full text-xs font-medium ${qualityColor}`">
                  {{ qualityText }} ({{ dailyTipData.daily_tip.quality_score.toFixed(1) }})
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 본문 -->
        <div class="p-6">
          <div class="prose max-w-none mb-6">
            <p class="text-gray-700 leading-relaxed">{{ dailyTipData.daily_tip.summary }}</p>
          </div>

          <!-- 태그 -->
          <div v-if="dailyTipData.daily_tip.tags.length > 0" class="mb-6">
            <h4 class="text-sm font-semibold text-gray-900 mb-2">관련 태그</h4>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="tag in dailyTipData.daily_tip.tags"
                :key="tag"
                class="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm"
              >
                {{ tag }}
              </span>
            </div>
          </div>

          <!-- 액션 버튼 -->
          <div class="flex justify-between items-center">
            <button
              @click="openExternalLink(dailyTipData.daily_tip.link)"
              class="bg-orange-600 hover:bg-orange-700 text-white px-6 py-3 rounded-lg flex items-center space-x-2 transition-colors font-medium"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
              <span>원문 보기</span>
            </button>
            
            <div class="text-sm text-gray-500">
              출처: {{ dailyTipData.selection_metadata?.category_name }}
            </div>
          </div>
        </div>
      </div>

      <!-- 선별 정보 카드 -->
      <div class="bg-gray-50 rounded-xl border border-gray-200 p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <svg class="w-5 h-5 text-gray-600 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          선별 정보
        </h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="bg-white p-4 rounded-lg">
            <dt class="text-sm font-medium text-gray-600">선별 이유</dt>
            <dd class="text-gray-900 mt-1">{{ dailyTipData.selection_metadata?.selection_reason }}</dd>
          </div>
          <div class="bg-white p-4 rounded-lg">
            <dt class="text-sm font-medium text-gray-600">후보 개수</dt>
            <dd class="text-gray-900 mt-1">{{ dailyTipData.selection_metadata?.candidate_count }}개 중 선별</dd>
          </div>
          <div class="bg-white p-4 rounded-lg">
            <dt class="text-sm font-medium text-gray-600">백업 로직 사용</dt>
            <dd class="text-gray-900 mt-1">{{ dailyTipData.selection_metadata?.backup_used ? '예' : '아니오' }}</dd>
          </div>
          <div class="bg-white p-4 rounded-lg">
            <dt class="text-sm font-medium text-gray-600">캐시 상태</dt>
            <dd class="text-gray-900 mt-1">{{ dailyTipData.cache_info?.cached ? '캐시됨' : '신규 생성' }}</dd>
          </div>
        </div>
      </div>
    </div>

    <!-- 성공이지만 소식이 없는 경우 -->
    <div v-else-if="dailyTipData && !dailyTipData.success" class="bg-yellow-50 border border-yellow-200 rounded-xl p-6">
      <div class="flex items-center space-x-3 mb-4">
        <svg class="w-6 h-6 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
        <h3 class="text-lg font-semibold text-yellow-900">오늘은 추천할 소식이 없습니다</h3>
      </div>
      <p class="text-yellow-700 mb-4">{{ dailyTipData.message }}</p>
      <p class="text-yellow-600 text-sm">{{ dailyTipData.suggestion }}</p>
    </div>
  </div>
</template>

<style scoped>
/* AWS 서비스팁 페이지 전용 스타일 */
.prose {
  line-height: 1.7;
}
</style> 