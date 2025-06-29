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

// HoneyBox API URL을 환경변수 기반으로 설정
const HONEYBOX_API_URL = import.meta.env.VITE_API_BASE_URL 
  ? `${import.meta.env.VITE_API_BASE_URL}/feeds`
  : 'http://localhost:8080/api/feeds'

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
  <div class="min-h-screen bg-gray-50">
    <!-- 컴팩트 헤더 -->
    <div class="bg-white border-b border-gray-200 px-6 py-3">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-xl font-bold text-gray-900">AWS 소식</h1>
          <p class="text-sm text-gray-500">HoneyBox가 매일 선별하는 AWS 뉴스와 업데이트</p>
        </div>
        
        <!-- 통계 정보 -->
        <div class="flex items-center space-x-4">
          <div class="text-center">
            <div class="text-sm font-semibold text-orange-600">{{ dailyTipData?.daily_tip ? '1' : '0' }}</div>
            <div class="text-xs text-gray-500">오늘의 소식</div>
          </div>
          <div class="text-center">
            <div class="text-sm font-semibold text-blue-600">{{ dailyTipData?.selection_metadata?.candidate_count || 0 }}</div>
            <div class="text-xs text-gray-500">후보 기사</div>
          </div>
          <div class="text-center">
            <div class="text-sm font-semibold text-green-600">{{ qualityText }}</div>
            <div class="text-xs text-gray-500">품질 등급</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 메인 컨텐츠 -->
    <div class="p-6 space-y-6">
      <!-- 컨트롤 버튼 -->
      <div class="flex items-center justify-end space-x-3">
        <!-- 번역 토글 버튼 -->
        <button
          @click="toggleTranslation"
          :class="[
            'flex items-center space-x-2 px-3 py-2 rounded-lg transition-colors text-xs',
            enableTranslation 
              ? 'bg-blue-500 hover:bg-blue-600 text-white' 
              : 'bg-gray-200 hover:bg-gray-300 text-gray-700'
          ]"
          :disabled="isLoading"
        >
          <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
          </svg>
          <span>{{ enableTranslation ? '한글' : '원문' }}</span>
        </button>
        
        <!-- 새로고침 버튼 -->
        <button
          @click="refreshTip"
          :disabled="isLoading"
          class="bg-orange-500 hover:bg-orange-600 disabled:bg-gray-400 text-white px-3 py-2 rounded-lg flex items-center space-x-2 transition-colors text-xs"
        >
          <svg 
            class="w-3 h-3" 
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

      <!-- 로딩 상태 -->
      <div v-if="isLoading" class="bg-white rounded-xl shadow-lg border border-gray-200 p-8">
        <div class="flex items-center justify-center space-x-3">
          <svg class="animate-spin h-5 w-5 text-orange-600" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span class="text-xs text-gray-600">오늘의 AWS 소식을 불러오는 중...</span>
        </div>
      </div>

      <!-- 오류 상태 -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-xl p-6">
        <div class="flex items-center space-x-3 mb-4">
          <svg class="w-5 h-5 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h3 class="text-sm font-semibold text-red-800">오류가 발생했습니다</h3>
        </div>
        <p class="text-xs text-red-700 mb-4">{{ error }}</p>
        <button
          @click="refreshTip"
          class="bg-red-600 hover:bg-red-700 text-white px-3 py-2 rounded-lg text-xs"
        >
          다시 시도
        </button>
      </div>

      <!-- 성공 상태 - 오늘의 소식 -->
      <div v-else-if="dailyTipData?.success && dailyTipData.daily_tip" class="space-y-6">
        <!-- 메인 소식 카드 -->
        <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
          <!-- 카드 헤더 -->
          <div class="bg-gradient-to-r from-orange-50 to-orange-100 px-6 py-4 border-b border-orange-200">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="w-8 h-8 bg-gradient-to-br from-orange-400 to-orange-600 rounded-lg flex items-center justify-center">
                  <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <div>
                  <h3 class="text-sm font-semibold text-gray-900">오늘의 AWS 소식</h3>
                  <p class="text-xs text-gray-600">{{ dailyTipData.daily_tip.published_readable }}</p>
                </div>
              </div>
              
              <!-- 품질 배지 -->
              <div :class="['px-2 py-1 rounded-full text-xs font-medium', qualityColor]">
                {{ qualityText }}
              </div>
            </div>
          </div>

          <!-- 카드 본문 -->
          <div class="p-6">
            <h2 class="text-sm font-semibold text-gray-900 mb-3 leading-relaxed">
              {{ dailyTipData.daily_tip.title }}
            </h2>
            
            <p class="text-xs text-gray-600 mb-4 leading-relaxed">
              {{ dailyTipData.daily_tip.summary }}
            </p>

            <!-- 태그 -->
            <div v-if="dailyTipData.daily_tip.tags?.length" class="flex flex-wrap gap-2 mb-4">
              <span
                v-for="tag in dailyTipData.daily_tip.tags"
                :key="tag"
                class="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full"
              >
                {{ tag }}
              </span>
            </div>

            <!-- 액션 버튼 -->
            <div class="flex items-center justify-between pt-4 border-t border-gray-100">
              <button
                @click="openExternalLink(dailyTipData.daily_tip.link)"
                class="flex items-center space-x-2 bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg transition-colors text-xs"
              >
                <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
                <span>원문 보기</span>
              </button>
              
              <div class="text-xs text-gray-500">
                품질 점수: {{ dailyTipData.daily_tip.quality_score.toFixed(1) }}/5.0
              </div>
            </div>
          </div>
        </div>

        <!-- 선별 정보 -->
        <div v-if="dailyTipData.selection_metadata" class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
          <h3 class="text-sm font-semibold text-gray-900 mb-4 flex items-center">
            <svg class="w-4 h-4 text-gray-600 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            선별 정보
          </h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="space-y-2">
              <div class="flex justify-between text-xs">
                <span class="font-medium text-gray-700">선별 날짜:</span>
                <span class="text-gray-600">{{ dailyTipData.selection_metadata.date }}</span>
              </div>
              <div class="flex justify-between text-xs">
                <span class="font-medium text-gray-700">요일:</span>
                <span class="text-gray-600">{{ dailyTipData.selection_metadata.weekday_name }}</span>
              </div>
              <div class="flex justify-between text-xs">
                <span class="font-medium text-gray-700">후보 기사 수:</span>
                <span class="text-gray-600">{{ dailyTipData.selection_metadata.candidate_count }}개</span>
              </div>
            </div>
            
            <div class="space-y-2">
              <div class="flex justify-between text-xs">
                <span class="font-medium text-gray-700">백업 사용:</span>
                <span class="text-gray-600">{{ dailyTipData.selection_metadata.backup_used ? '예' : '아니오' }}</span>
              </div>
              <div class="flex justify-between text-xs">
                <span class="font-medium text-gray-700">품질 필터:</span>
                <span class="text-gray-600">{{ dailyTipData.selection_metadata.quality_filter_applied ? '적용됨' : '미적용' }}</span>
              </div>
              <div class="flex justify-between text-xs">
                <span class="font-medium text-gray-700">선별 카테고리:</span>
                <span class="text-gray-600">{{ dailyTipData.selection_metadata.category_name || '일반' }}</span>
              </div>
            </div>
          </div>

          <!-- 선별 이유 -->
          <div class="mt-4 pt-4 border-t border-gray-100">
            <h4 class="text-xs font-medium text-gray-700 mb-2">선별 이유:</h4>
            <p class="text-xs text-gray-600 leading-relaxed">
              {{ dailyTipData.selection_metadata.selection_reason }}
            </p>
          </div>

          <!-- 우선순위 카테고리 -->
          <div v-if="dailyTipData.selection_metadata.priority_categories?.length" class="mt-4 pt-4 border-t border-gray-100">
            <h4 class="text-xs font-medium text-gray-700 mb-2">우선순위 카테고리:</h4>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="category in dailyTipData.selection_metadata.priority_categories"
                :key="category"
                class="px-2 py-1 bg-blue-100 text-blue-600 text-xs rounded-full"
              >
                {{ category }}
              </span>
            </div>
          </div>
        </div>

        <!-- 캐시 정보 -->
        <div v-if="dailyTipData.cache_info" class="bg-gray-50 rounded-xl p-4">
          <div class="flex items-center justify-between text-xs text-gray-600">
            <div class="flex items-center space-x-2">
              <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>{{ dailyTipData.cache_info.cached ? '캐시됨' : '실시간' }}</span>
            </div>
            <span>생성: {{ dailyTipData.cache_info.generated_at }}</span>
          </div>
        </div>
      </div>

      <!-- 데이터 없음 상태 -->
      <div v-else class="bg-white rounded-xl shadow-lg border border-gray-200 p-8 text-center">
        <svg class="w-12 h-12 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2M4 13h2m13-8V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v1M7 8h10l-1 8H8L7 8z" />
        </svg>
        <h3 class="text-sm font-semibold text-gray-900 mb-2">소식이 없습니다</h3>
        <p class="text-xs text-gray-600 mb-4">
          {{ dailyTipData?.message || '오늘의 AWS 소식을 준비 중입니다.' }}
        </p>
        <button
          @click="refreshTip"
          class="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg text-xs"
        >
          다시 확인
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* AWS 서비스팁 페이지 전용 스타일 */
.prose {
  line-height: 1.7;
}
</style> 