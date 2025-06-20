<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { noticeService } from '../services/noticeService'
import { memberService } from '../services/memberService'
import type { Notice, NoticeStats, Member, NoticeCreate, NoticeUpdate } from '../types'

// 반응형 상태
const notices = ref<Notice[]>([])
const pinnedNotices = ref<Notice[]>([])
const stats = ref<NoticeStats | null>(null)
const members = ref<Member[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const searchQuery = ref('')
const selectedPriority = ref('all')
const showPinnedOnly = ref(false)
const viewMode = ref<'cards' | 'table'>('cards')

// 모달 상태
const selectedNotice = ref<Notice | null>(null)
const showNoticeModal = ref(false)
const showCreateModal = ref(false)
const showEditModal = ref(false)

// 새 공지사항 폼
const newNotice = ref<NoticeCreate>({
  title: '',
  content: '',
  priority: 'normal',
  author_id: 1, // 기본값
  is_pinned: false
})

const editNotice = ref<NoticeUpdate>({})

// 중요도 옵션
const priorityOptions = [
  { value: 'all', label: '전체', color: 'bg-gray-100 text-gray-800', icon: '📋' },
  { value: 'important', label: '중요', color: 'bg-red-100 text-red-800', icon: '🚨' },
  { value: 'caution', label: '주의', color: 'bg-yellow-100 text-yellow-800', icon: '⚠️' },
  { value: 'normal', label: '일반', color: 'bg-blue-100 text-blue-800', icon: '📢' }
]

// 계산된 속성
const filteredNotices = computed(() => {
  let filtered = showPinnedOnly.value ? pinnedNotices.value : notices.value

  // 중요도 필터
  if (selectedPriority.value !== 'all') {
    filtered = filtered.filter(notice => notice.priority === selectedPriority.value)
  }

  // 검색 필터
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(notice =>
      notice.title.toLowerCase().includes(query) ||
      notice.content.toLowerCase().includes(query) ||
      getAuthorName(notice.author_id).toLowerCase().includes(query)
    )
  }

  return filtered.sort((a, b) => {
    // 고정 공지사항을 먼저 표시
    if (a.is_pinned && !b.is_pinned) return -1
    if (!a.is_pinned && b.is_pinned) return 1
    
    // 중요도 순서
    const priorityOrder = { important: 3, caution: 2, normal: 1 }
    const aPriority = priorityOrder[a.priority]
    const bPriority = priorityOrder[b.priority]
    
    if (aPriority !== bPriority) return bPriority - aPriority
    
    // 생성일 순서 (최신순)
    return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  })
})

// 공지사항별 그룹화
const noticesByPriority = computed(() => {
  const grouped: Record<string, Notice[]> = {}
  
  filteredNotices.value.forEach(notice => {
    const priority = notice.priority
    if (!grouped[priority]) {
      grouped[priority] = []
    }
    grouped[priority].push(notice)
  })
  
  return grouped
})

// 데이터 로딩 함수
const loadNotices = async () => {
  try {
    loading.value = true
    error.value = null
    
    const [noticesRes, pinnedRes, statsRes, membersRes] = await Promise.all([
      noticeService.getNotices({ limit: 100 }),
      noticeService.getPinnedNotices(),
      noticeService.getNoticeStats(),
      memberService.getActiveMembers()
    ])
    
    notices.value = noticesRes.notices
    pinnedNotices.value = pinnedRes
    stats.value = statsRes
    members.value = membersRes
    
  } catch (err: any) {
    error.value = err.message || '데이터를 불러오는 중 오류가 발생했습니다.'
    console.error('공지사항 데이터 로딩 오류:', err)
  } finally {
    loading.value = false
  }
}

// 공지사항 상세 보기
const showNoticeDetail = (notice: Notice) => {
  selectedNotice.value = notice
  showNoticeModal.value = true
}

// 공지사항 편집
const editNoticeDetail = (notice: Notice) => {
  selectedNotice.value = notice
  editNotice.value = {
    title: notice.title,
    content: notice.content,
    priority: notice.priority,
    is_pinned: notice.is_pinned
  }
  showEditModal.value = true
}

// 모달 닫기
const closeModals = () => {
  showNoticeModal.value = false
  showCreateModal.value = false
  showEditModal.value = false
  selectedNotice.value = null
  newNotice.value = {
    title: '',
    content: '',
    priority: 'normal',
    author_id: 1,
    is_pinned: false
  }
  editNotice.value = {}
}

// 공지사항 생성
const createNotice = async () => {
  try {
    if (!newNotice.value.title.trim() || !newNotice.value.content.trim()) {
      alert('제목과 내용을 입력해주세요.')
      return
    }

    await noticeService.createNotice(newNotice.value)
    closeModals()
    await loadNotices()
    alert('공지사항이 생성되었습니다.')
  } catch (err: any) {
    console.error('공지사항 생성 실패:', err)
    alert(`공지사항 생성에 실패했습니다: ${err.message}`)
  }
}

// 공지사항 수정
const updateNotice = async () => {
  try {
    if (!selectedNotice.value) return
    
    await noticeService.updateNotice(selectedNotice.value.id, editNotice.value)
    closeModals()
    await loadNotices()
    alert('공지사항이 수정되었습니다.')
  } catch (err: any) {
    console.error('공지사항 수정 실패:', err)
    alert(`공지사항 수정에 실패했습니다: ${err.message}`)
  }
}

// 공지사항 삭제
const deleteNotice = async (noticeId: number) => {
  if (!confirm('정말로 이 공지사항을 삭제하시겠습니까?')) return
  
  try {
    await noticeService.deleteNotice(noticeId)
    await loadNotices()
    alert('공지사항이 삭제되었습니다.')
  } catch (err: any) {
    console.error('공지사항 삭제 실패:', err)
    alert(`공지사항 삭제에 실패했습니다: ${err.message}`)
  }
}

// 유틸리티 함수들
const getPriorityColor = (priority: Notice['priority']) => {
  const colors: Record<string, string> = {
    'important': 'bg-red-100 text-red-800',
    'caution': 'bg-yellow-100 text-yellow-800',
    'normal': 'bg-blue-100 text-blue-800'
  }
  return colors[priority] || 'bg-gray-100 text-gray-800'
}

const getPriorityIcon = (priority: Notice['priority']) => {
  const icons: Record<string, string> = {
    'important': '🚨',
    'caution': '⚠️',
    'normal': '📢'
  }
  return icons[priority] || '📢'
}

const getPriorityLabel = (priority: Notice['priority']) => {
  const labels: Record<string, string> = {
    'important': '중요',
    'caution': '주의',
    'normal': '일반'
  }
  return labels[priority] || '일반'
}

const getAuthorName = (authorId: number) => {
  const author = members.value.find(m => m.id === authorId)
  return author?.name || '알 수 없음'
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatRelativeDate = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = now.getTime() - date.getTime()
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) return '오늘'
  if (diffDays === 1) return '어제'
  if (diffDays < 7) return `${diffDays}일 전`
  return date.toLocaleDateString('ko-KR', { month: 'short', day: 'numeric' })
}

// 컴포넌트 마운트 시 데이터 로딩
onMounted(() => {
  loadNotices()
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 컴팩트 헤더 -->
    <div class="bg-white border-b border-gray-200 px-6 py-3">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-xl font-bold text-gray-900">TS 공지사항</h1>
          <p class="text-sm text-gray-500">팀 공지사항 관리</p>
        </div>
        
        <!-- 컴팩트 통계 및 컨트롤 -->
        <div class="flex items-center space-x-4">
          <!-- 통계 -->
          <div class="flex items-center space-x-3">
            <div class="text-center">
              <div class="text-sm font-semibold text-blue-600">{{ stats?.total_notices || 0 }}</div>
              <div class="text-xs text-gray-500">전체</div>
            </div>
            <div class="text-center">
              <div class="text-sm font-semibold text-yellow-600">{{ stats?.pinned_notices || 0 }}</div>
              <div class="text-xs text-gray-500">고정</div>
            </div>
            <div class="text-center">
              <div class="text-sm font-semibold text-red-600">{{ stats?.by_priority?.important || 0 }}</div>
              <div class="text-xs text-gray-500">중요</div>
            </div>
            <div class="text-center">
              <div class="text-sm font-semibold text-orange-600">{{ stats?.recent_notices || 0 }}</div>
              <div class="text-xs text-gray-500">최근</div>
            </div>
          </div>
          
          <!-- 구분선 -->
          <div class="h-8 w-px bg-gray-300"></div>
          
          <!-- 뷰 모드 전환 -->
          <div class="flex bg-gray-100 rounded-lg p-1">
            <button
              @click="viewMode = 'cards'"
              :class="`px-2 py-1 rounded-md text-xs font-medium transition-colors ${
                viewMode === 'cards' 
                  ? 'bg-white text-gray-900 shadow-sm' 
                  : 'text-gray-600 hover:text-gray-900'
              }`"
            >
              카드
            </button>
            <button
              @click="viewMode = 'table'"
              :class="`px-2 py-1 rounded-md text-xs font-medium transition-colors ${
                viewMode === 'table' 
                  ? 'bg-white text-gray-900 shadow-sm' 
                  : 'text-gray-600 hover:text-gray-900'
              }`"
            >
              테이블
            </button>
          </div>
          
          <button 
            @click="showCreateModal = true"
            class="px-3 py-1.5 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors text-sm"
          >
            + 새 공지사항
          </button>
          
          <button 
            @click="loadNotices"
            :disabled="loading"
            class="px-3 py-1.5 bg-gray-600 text-white rounded-md hover:bg-gray-700 disabled:opacity-50 transition-colors text-sm"
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
      <!-- 검색 및 필터 -->
      <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-4">
        <div class="flex flex-col md:flex-row gap-3">
          <div class="flex-1">
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <input
                v-model="searchQuery"
                type="text"
                class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 text-sm"
                placeholder="공지사항 검색..."
              />
            </div>
          </div>
          
          <div class="flex flex-col sm:flex-row gap-2">
            <select
              v-model="selectedPriority"
              class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 text-sm"
            >
              <option v-for="option in priorityOptions" :key="option.value" :value="option.value">
                {{ option.label }}
              </option>
            </select>
            
            <label class="inline-flex items-center px-3 py-2 border border-gray-300 rounded-md cursor-pointer hover:bg-gray-50">
              <input
                v-model="showPinnedOnly"
                type="checkbox"
                class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
              />
              <span class="ml-2 text-sm text-gray-700">고정 공지만</span>
            </label>
          </div>
        </div>
      </div>

      <!-- 로딩 상태 -->
      <div v-if="loading" class="flex items-center justify-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-gray-600">공지사항을 불러오는 중...</span>
      </div>

      <!-- 에러 상태 -->
      <div v-else-if="error" class="bg-white rounded-xl shadow-lg border border-gray-200 p-8 text-center">
        <div class="text-red-600 mb-4">{{ error }}</div>
        <button
          @click="loadNotices"
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
        >
          다시 시도
        </button>
      </div>

      <!-- 카드 뷰 -->
      <div v-else-if="viewMode === 'cards'" class="space-y-4">
        <div 
          v-for="notice in filteredNotices" 
          :key="notice.id"
          :class="[
            'bg-white rounded-xl shadow-lg border border-gray-200 p-6 hover:shadow-xl transition-all duration-200 cursor-pointer',
            notice.is_pinned ? 'ring-2 ring-yellow-200 bg-yellow-50' : ''
          ]"
          @click="showNoticeDetail(notice)"
        >
          <div class="flex items-start justify-between mb-4">
            <div class="flex items-start space-x-4 flex-1">
              <!-- 아이콘 -->
              <div :class="['w-10 h-10 rounded-lg flex items-center justify-center text-lg', getPriorityColor(notice.priority)]">
                {{ getPriorityIcon(notice.priority) }}
              </div>
              
              <div class="flex-1 min-w-0">
                <div class="flex items-center space-x-2 mb-2">
                  <h3 class="text-lg font-semibold text-gray-900 truncate">{{ notice.title }}</h3>
                  <span v-if="notice.is_pinned" class="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs font-medium rounded-full">
                    📌 고정
                  </span>
                </div>
                <div class="flex items-center space-x-3 text-sm text-gray-500 mb-3">
                  <span>{{ getAuthorName(notice.author_id) }}</span>
                  <span>•</span>
                  <span>{{ formatRelativeDate(notice.created_at) }}</span>
                  <span>•</span>
                  <span>조회 {{ notice.views }}회</span>
                </div>
                <p class="text-gray-600 leading-relaxed line-clamp-2">
                  {{ notice.content.length > 120 ? notice.content.substring(0, 120) + '...' : notice.content }}
                </p>
              </div>
            </div>
            
            <div class="flex items-center space-x-3 ml-4">
              <!-- 중요도 배지 -->
              <span :class="['px-3 py-1 rounded-full text-sm font-medium', getPriorityColor(notice.priority)]">
                {{ getPriorityLabel(notice.priority) }}
              </span>
              
              <!-- 액션 버튼들 -->
              <div class="flex items-center space-x-1">
                <button
                  @click.stop="editNoticeDetail(notice)"
                  class="text-gray-400 hover:text-blue-600 transition-colors p-1"
                  title="편집"
                >
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
                <button
                  @click.stop="deleteNotice(notice.id)"
                  class="text-gray-400 hover:text-red-600 transition-colors p-1"
                  title="삭제"
                >
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 테이블 뷰 -->
      <div v-else class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">제목</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">중요도</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">작성자</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">작성일</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">조회수</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">상태</th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">액션</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr
                v-for="notice in filteredNotices"
                :key="notice.id"
                :class="[
                  'hover:bg-gray-50 cursor-pointer transition-colors',
                  notice.is_pinned ? 'bg-yellow-50' : ''
                ]"
                @click="showNoticeDetail(notice)"
              >
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="text-sm font-medium text-gray-900 truncate max-w-xs">
                      {{ notice.title }}
                    </div>
                    <span v-if="notice.is_pinned" class="ml-2 text-xs">📌</span>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="['inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium', getPriorityColor(notice.priority)]">
                    {{ getPriorityIcon(notice.priority) }} {{ getPriorityLabel(notice.priority) }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ getAuthorName(notice.author_id) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ formatDate(notice.created_at) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ notice.views }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="['inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium', notice.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800']">
                    {{ notice.is_active ? '활성' : '비활성' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div class="flex items-center justify-end space-x-2">
                    <button
                      @click.stop="editNoticeDetail(notice)"
                      class="text-blue-600 hover:text-blue-900 transition-colors"
                      title="편집"
                    >
                      편집
                    </button>
                    <button
                      @click.stop="deleteNotice(notice.id)"
                      class="text-red-600 hover:text-red-900 transition-colors"
                      title="삭제"
                    >
                      삭제
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 빈 상태 -->
      <div v-if="!loading && !error && filteredNotices.length === 0" class="bg-white rounded-xl shadow-lg border border-gray-200 p-12 text-center">
        <div class="text-6xl mb-4">📭</div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">공지사항이 없습니다</h3>
        <p class="text-gray-600 mb-4">
          {{ searchQuery || selectedPriority !== 'all' || showPinnedOnly ? '검색 조건에 맞는 공지사항이 없습니다.' : '새로운 공지사항을 작성해보세요.' }}
        </p>
        <div class="space-x-3">
          <button
            v-if="searchQuery || selectedPriority !== 'all' || showPinnedOnly"
            @click="searchQuery = ''; selectedPriority = 'all'; showPinnedOnly = false"
            class="text-blue-600 hover:text-blue-700 transition-colors"
          >
            필터 초기화
          </button>
          <button
            @click="showCreateModal = true"
            class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            새 공지사항 작성
          </button>
        </div>
      </div>
    </div>

    <!-- 공지사항 상세 모달 -->
    <div v-if="showNoticeModal && selectedNotice" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex items-start justify-between mb-6">
            <div class="flex items-center space-x-4">
              <div :class="['w-12 h-12 rounded-lg flex items-center justify-center text-xl', getPriorityColor(selectedNotice.priority)]">
                {{ getPriorityIcon(selectedNotice.priority) }}
              </div>
              <div>
                <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ selectedNotice.title }}</h2>
                <div class="flex items-center space-x-3">
                  <span :class="['px-3 py-1 rounded-full text-sm font-medium', getPriorityColor(selectedNotice.priority)]">
                    {{ getPriorityLabel(selectedNotice.priority) }}
                  </span>
                  <span v-if="selectedNotice.is_pinned" class="px-3 py-1 bg-yellow-100 text-yellow-800 text-sm font-medium rounded-full">
                    📌 고정 공지
                  </span>
                </div>
              </div>
            </div>
            <button
              @click="closeModals"
              class="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <div class="flex items-center space-x-4 text-sm text-gray-500 mb-6 pb-6 border-b border-gray-200">
            <span class="font-medium">{{ getAuthorName(selectedNotice.author_id) }}</span>
            <span>•</span>
            <span>{{ formatDate(selectedNotice.created_at) }}</span>
            <span>•</span>
            <span>조회 {{ selectedNotice.views }}회</span>
          </div>
          
          <div class="prose max-w-none">
            <div class="whitespace-pre-wrap text-gray-700 leading-relaxed text-base">{{ selectedNotice.content }}</div>
          </div>
          
          <div class="flex justify-end space-x-3 mt-8 pt-6 border-t border-gray-200">
            <button
              @click="editNoticeDetail(selectedNotice)"
              class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
            >
              편집
            </button>
            <button
              @click="deleteNotice(selectedNotice.id); closeModals()"
              class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              삭제
            </button>
            <button
              @click="closeModals"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              닫기
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 새 공지사항 생성 모달 -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-xl font-bold text-gray-900">새 공지사항 작성</h2>
            <button
              @click="closeModals"
              class="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <form @submit.prevent="createNotice" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">제목</label>
              <input
                v-model="newNotice.title"
                type="text"
                required
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="공지사항 제목을 입력하세요"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">내용</label>
              <textarea
                v-model="newNotice.content"
                required
                rows="8"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="공지사항 내용을 입력하세요"
              ></textarea>
            </div>
            
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">중요도</label>
                <select
                  v-model="newNotice.priority"
                  class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="normal">📢 일반</option>
                  <option value="caution">⚠️ 주의</option>
                  <option value="important">🚨 중요</option>
                </select>
              </div>
              
              <div class="flex items-end">
                <label class="flex items-center">
                  <input
                    v-model="newNotice.is_pinned"
                    type="checkbox"
                    class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
                  >
                  <span class="ml-2 text-sm text-gray-700">📌 상단 고정</span>
                </label>
              </div>
            </div>
            
            <div class="flex justify-end space-x-3 pt-6">
              <button
                type="button"
                @click="closeModals"
                class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
              >
                취소
              </button>
              <button
                type="submit"
                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                작성하기
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- 공지사항 편집 모달 -->
    <div v-if="showEditModal && selectedNotice" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-xl font-bold text-gray-900">공지사항 편집</h2>
            <button
              @click="closeModals"
              class="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <form @submit.prevent="updateNotice" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">제목</label>
              <input
                v-model="editNotice.title"
                type="text"
                required
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="공지사항 제목을 입력하세요"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">내용</label>
              <textarea
                v-model="editNotice.content"
                required
                rows="8"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="공지사항 내용을 입력하세요"
              ></textarea>
            </div>
            
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">중요도</label>
                <select
                  v-model="editNotice.priority"
                  class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="normal">📢 일반</option>
                  <option value="caution">⚠️ 주의</option>
                  <option value="important">🚨 중요</option>
                </select>
              </div>
              
              <div class="flex items-end">
                <label class="flex items-center">
                  <input
                    v-model="editNotice.is_pinned"
                    type="checkbox"
                    class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
                  >
                  <span class="ml-2 text-sm text-gray-700">📌 상단 고정</span>
                </label>
              </div>
            </div>
            
            <div class="flex justify-end space-x-3 pt-6">
              <button
                type="button"
                @click="closeModals"
                class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
              >
                취소
              </button>
              <button
                type="submit"
                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                수정하기
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 