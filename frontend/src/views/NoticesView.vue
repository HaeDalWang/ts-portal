<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 공지사항 타입 정의
interface Notice {
  id: number
  title: string
  content: string
  type: 'important' | 'normal' | 'warning'
  author: string
  createdAt: string
  isRead: boolean
  priority: number
}

// 반응형 데이터
const notices = ref<Notice[]>([])
const isLoading = ref(true)

// 샘플 공지사항 데이터 (추후 API 연동 예정)
const sampleNotices: Notice[] = [
  {
    id: 1,
    title: '12월 팀 회식 관련 안내',
    content: '12월 25일 금요일 저녁 7시에 팀 회식이 예정되어 있습니다. 참석 여부를 12월 20일까지 알려주시기 바랍니다.',
    type: 'important',
    author: '팀장',
    createdAt: '2024-12-15',
    isRead: false,
    priority: 1
  },
  {
    id: 2,
    title: '연말 프로젝트 마감 일정 안내',
    content: '올해 마지막 프로젝트 마감은 12월 29일입니다. 각자 담당하신 업무의 진행상황을 주간 회의에서 공유 부탁드립니다.',
    type: 'normal',
    author: '팀장',
    createdAt: '2024-12-10',
    isRead: true,
    priority: 2
  },
  {
    id: 3,
    title: '보안 교육 필수 이수 안내',
    content: '회사 정책에 따라 모든 직원은 12월 말까지 보안 교육을 이수해야 합니다. 아직 완료하지 않으신 분들은 빠른 시일 내에 완료해 주시기 바랍니다.',
    type: 'warning',
    author: '팀장',
    createdAt: '2024-12-05',
    isRead: false,
    priority: 3
  },
  {
    id: 4,
    title: '새해 업무 계획 및 목표 설정',
    content: '2025년 업무 계획 및 개인 목표를 설정하는 시간을 가지겠습니다. 1월 첫째 주에 개별 면담을 진행할 예정이니 미리 준비해 주시기 바랍니다.',
    type: 'normal',
    author: '팀장',
    createdAt: '2024-12-03',
    isRead: true,
    priority: 4
  }
]

// 공지사항 타입별 스타일
const getNoticeStyle = (type: Notice['type']) => {
  switch (type) {
    case 'important':
      return {
        borderColor: 'border-red-200',
        bgColor: 'bg-red-50',
        badgeColor: 'bg-red-100 text-red-800',
        iconColor: 'text-red-600'
      }
    case 'warning':
      return {
        borderColor: 'border-yellow-200',
        bgColor: 'bg-yellow-50',
        badgeColor: 'bg-yellow-100 text-yellow-800',
        iconColor: 'text-yellow-600'
      }
    default:
      return {
        borderColor: 'border-blue-200',
        bgColor: 'bg-blue-50',
        badgeColor: 'bg-blue-100 text-blue-800',
        iconColor: 'text-blue-600'
      }
  }
}

// 공지사항 타입별 한글 라벨
const getTypeLabel = (type: Notice['type']) => {
  switch (type) {
    case 'important': return '중요'
    case 'warning': return '주의'
    default: return '일반'
  }
}

// 공지사항 읽음 처리
const markAsRead = (noticeId: number) => {
  const notice = notices.value.find(n => n.id === noticeId)
  if (notice) {
    notice.isRead = true
  }
}

// 컴포넌트 마운트 시 데이터 로드
onMounted(() => {
  setTimeout(() => {
    notices.value = sampleNotices.sort((a, b) => a.priority - b.priority)
    isLoading.value = false
  }, 500)
})
</script>

<template>
  <div class="space-y-6">
    <!-- 헤더 섹션 -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center space-x-4">
        <div class="w-12 h-12 bg-gradient-to-br from-blue-400 to-blue-600 rounded-lg flex items-center justify-center shadow-lg">
          <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z" />
          </svg>
        </div>
        <div>
          <h1 class="text-3xl font-bold text-gray-900">TS 공지사항</h1>
          <p class="text-gray-600">팀장님의 중요 공지사항과 주의사항을 확인하세요</p>
        </div>
      </div>
      <div class="text-right">
        <div class="text-sm text-gray-500">
          총 {{ notices.length }}개의 공지사항
        </div>
        <div class="text-xs text-gray-400 mt-1">
          미확인: {{ notices.filter(n => !n.isRead).length }}개
        </div>
      </div>
    </div>

    <!-- 로딩 상태 -->
    <div v-if="isLoading" class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      <span class="ml-2 text-gray-600">공지사항을 불러오는 중...</span>
    </div>

    <!-- 공지사항 목록 -->
    <div v-else class="space-y-4">
      <div 
        v-for="notice in notices" 
        :key="notice.id"
        :class="[
          'bg-white rounded-xl shadow-lg border-2 p-6 transition-all duration-300 cursor-pointer hover:shadow-xl',
          getNoticeStyle(notice.type).borderColor,
          !notice.isRead ? 'ring-2 ring-offset-2 ring-blue-200' : ''
        ]"
        @click="markAsRead(notice.id)"
      >
        <div class="flex items-start justify-between mb-4">
          <div class="flex items-center space-x-3">
            <!-- 공지사항 타입 아이콘 -->
            <div :class="['w-10 h-10 rounded-lg flex items-center justify-center', getNoticeStyle(notice.type).bgColor]">
              <svg v-if="notice.type === 'important'" :class="['w-5 h-5', getNoticeStyle(notice.type).iconColor]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.464 0L4.35 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
              <svg v-else-if="notice.type === 'warning'" :class="['w-5 h-5', getNoticeStyle(notice.type).iconColor]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <svg v-else :class="['w-5 h-5', getNoticeStyle(notice.type).iconColor]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            
            <div>
              <h3 class="text-lg font-semibold text-gray-900 mb-1">{{ notice.title }}</h3>
              <div class="flex items-center space-x-3 text-sm text-gray-500">
                <span>{{ notice.author }}</span>
                <span>•</span>
                <span>{{ notice.createdAt }}</span>
              </div>
            </div>
          </div>
          
          <div class="flex items-center space-x-2">
            <!-- 공지사항 타입 배지 -->
            <span :class="['px-2 py-1 rounded-full text-xs font-medium', getNoticeStyle(notice.type).badgeColor]">
              {{ getTypeLabel(notice.type) }}
            </span>
            
            <!-- 읽음 상태 표시 -->
            <div v-if="!notice.isRead" class="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
          </div>
        </div>
        
        <!-- 공지 내용 -->
        <div class="text-gray-700 leading-relaxed">
          {{ notice.content }}
        </div>
        
        <!-- 하단 액션 영역 -->
        <div class="mt-4 pt-4 border-t border-gray-100 flex items-center justify-between">
          <div class="text-xs text-gray-400">
            {{ notice.isRead ? '읽음' : '미확인' }}
          </div>
          <div class="text-blue-600 text-sm font-medium hover:text-blue-700 transition-colors">
            {{ notice.isRead ? '다시 보기' : '확인하기' }} →
          </div>
        </div>
      </div>
    </div>
    
    <!-- 공지사항이 없는 경우 -->
    <div v-if="!isLoading && notices.length === 0" class="text-center py-12">
      <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2M4 13h2m13-4h-2m-3 0h-2m-3 0h-2m-3 0H6" />
        </svg>
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">공지사항이 없습니다</h3>
      <p class="text-gray-500">새로운 공지사항이 등록되면 알려드릴게요.</p>
    </div>
  </div>
</template>

<style scoped>
/* 추가 스타일이 필요한 경우 여기에 작성 */
</style> 