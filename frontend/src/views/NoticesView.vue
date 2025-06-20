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
  <div class="min-h-screen bg-gray-50">
    <!-- 컴팩트 헤더 -->
    <div class="bg-white border-b border-gray-200 px-6 py-3">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-xl font-bold text-gray-900">TS 공지사항</h1>
          <p class="text-sm text-gray-500">팀장님의 중요 공지사항과 주의사항</p>
        </div>
        
        <!-- 통계 정보 -->
        <div class="flex items-center space-x-4">
          <div class="text-center">
            <div class="text-sm font-semibold text-blue-600">{{ notices.length }}</div>
            <div class="text-xs text-gray-500">전체 공지</div>
          </div>
          <div class="text-center">
            <div class="text-sm font-semibold text-red-600">{{ notices.filter(n => !n.isRead).length }}</div>
            <div class="text-xs text-gray-500">미확인</div>
          </div>
          <div class="text-center">
            <div class="text-sm font-semibold text-orange-600">{{ notices.filter(n => n.type === 'important').length }}</div>
            <div class="text-xs text-gray-500">중요 공지</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 메인 컨텐츠 -->
    <div class="p-6 space-y-4">
      <!-- 로딩 상태 -->
      <div v-if="isLoading" class="flex items-center justify-center py-12">
        <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
        <span class="ml-2 text-xs text-gray-600">공지사항을 불러오는 중...</span>
      </div>

      <!-- 공지사항 목록 -->
      <div v-else class="space-y-3">
        <div 
          v-for="notice in notices" 
          :key="notice.id"
          :class="[
            'bg-white rounded-xl shadow-lg border-2 p-4 transition-all cursor-pointer hover:shadow-xl',
            getNoticeStyle(notice.type).borderColor,
            !notice.isRead ? 'ring-2 ring-offset-2 ring-blue-200' : ''
          ]"
          @click="markAsRead(notice.id)"
        >
          <div class="flex items-start justify-between mb-3">
            <div class="flex items-center space-x-3">
              <!-- 공지사항 타입 아이콘 -->
              <div :class="['w-8 h-8 rounded-lg flex items-center justify-center', getNoticeStyle(notice.type).bgColor]">
                <svg v-if="notice.type === 'important'" :class="['w-4 h-4', getNoticeStyle(notice.type).iconColor]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.464 0L4.35 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
                <svg v-else-if="notice.type === 'warning'" :class="['w-4 h-4', getNoticeStyle(notice.type).iconColor]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <svg v-else :class="['w-4 h-4', getNoticeStyle(notice.type).iconColor]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              
              <div>
                <h3 class="text-sm font-semibold text-gray-900 mb-1">{{ notice.title }}</h3>
                <div class="flex items-center space-x-2 text-xs text-gray-500">
                  <span>{{ notice.author }}</span>
                  <span>•</span>
                  <span>{{ notice.createdAt }}</span>
                </div>
              </div>
            </div>
            
            <div class="flex items-center space-x-2">
              <!-- 공지사항 타입 배지 -->
              <span :class="['px-2 py-1 rounded-full text-xs font-semibold', getNoticeStyle(notice.type).badgeColor]">
                {{ getTypeLabel(notice.type) }}
              </span>
              
              <!-- 읽음 상태 표시 -->
              <div v-if="!notice.isRead" class="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
            </div>
          </div>
          
          <!-- 공지 내용 -->
          <div class="text-xs text-gray-600 leading-relaxed pl-11">
            {{ notice.content }}
          </div>
          
          <!-- 읽음 처리 안내 -->
          <div v-if="!notice.isRead" class="mt-3 pt-3 border-t border-gray-100">
            <div class="flex items-center text-xs text-blue-600">
              <svg class="w-3 h-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              클릭하여 읽음 처리
            </div>
          </div>
        </div>
      </div>

      <!-- 빈 상태 -->
      <div v-if="!isLoading && notices.length === 0" class="text-center py-12">
        <svg class="w-12 h-12 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2M4 13h2m13-8V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v1M7 8h10l-1 8H8L7 8z" />
        </svg>
        <h3 class="text-sm font-semibold text-gray-900 mb-2">공지사항이 없습니다</h3>
        <p class="text-xs text-gray-600">새로운 공지사항이 등록되면 여기에 표시됩니다.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 추가 스타일이 필요한 경우 여기에 작성 */
</style> 