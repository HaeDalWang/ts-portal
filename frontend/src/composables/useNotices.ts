import { ref, computed, onMounted } from 'vue'
import { noticeService } from '@/services/noticeService'
import { memberService } from '@/services/memberService'
import type { Notice, NoticeStats, Member, NoticeCreate, NoticeUpdate } from '@/types'

export function useNotices() {
  // 반응형 상태
  const notices = ref<Notice[]>([])
  const pinnedNotices = ref<Notice[]>([])
  const stats = ref<NoticeStats | null>(null)
  const members = ref<Member[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  
  // 필터 상태
  const searchQuery = ref('')
  const selectedPriority = ref('all')
  const showPinnedOnly = ref(false)
  const viewMode = ref<'cards' | 'table'>('cards')

  // 모달 상태
  const selectedNotice = ref<Notice | null>(null)
  const showNoticeModal = ref(false)
  const showCreateModal = ref(false)
  const showEditModal = ref(false)

  // 폼 데이터
  const newNotice = ref<NoticeCreate>({
    title: '',
    content: '',
    priority: 'normal',
    author_id: 1, // 기본값
    is_pinned: false
  })

  const editNotice = ref<NoticeUpdate>({})

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
        throw new Error('제목과 내용을 입력해주세요.')
      }

      await noticeService.createNotice(newNotice.value)
      closeModals()
      await loadNotices()
      return { success: true, message: '공지사항이 생성되었습니다.' }
    } catch (err: any) {
      console.error('공지사항 생성 실패:', err)
      return { success: false, message: `공지사항 생성에 실패했습니다: ${err.message}` }
    }
  }

  // 공지사항 수정
  const updateNotice = async () => {
    try {
      if (!selectedNotice.value) return { success: false, message: '선택된 공지사항이 없습니다.' }
      
      await noticeService.updateNotice(selectedNotice.value.id, editNotice.value)
      closeModals()
      await loadNotices()
      return { success: true, message: '공지사항이 수정되었습니다.' }
    } catch (err: any) {
      console.error('공지사항 수정 실패:', err)
      return { success: false, message: `공지사항 수정에 실패했습니다: ${err.message}` }
    }
  }

  // 공지사항 삭제
  const deleteNotice = async (noticeId: number) => {
    try {
      await noticeService.deleteNotice(noticeId)
      await loadNotices()
      return { success: true, message: '공지사항이 삭제되었습니다.' }
    } catch (err: any) {
      console.error('공지사항 삭제 실패:', err)
      return { success: false, message: `공지사항 삭제에 실패했습니다: ${err.message}` }
    }
  }

  // 유틸리티 함수들
  const getAuthorName = (authorId: number) => {
    const author = members.value.find(m => m.id === authorId)
    return author?.name || '알 수 없음'
  }

  // 필터 초기화
  const resetFilters = () => {
    searchQuery.value = ''
    selectedPriority.value = 'all'
    showPinnedOnly.value = false
  }

  // 초기화
  onMounted(() => {
    loadNotices()
  })

  return {
    // 상태
    notices,
    pinnedNotices,
    stats,
    members,
    loading,
    error,
    searchQuery,
    selectedPriority,
    showPinnedOnly,
    viewMode,
    selectedNotice,
    showNoticeModal,
    showCreateModal,
    showEditModal,
    newNotice,
    editNotice,
    filteredNotices,
    
    // 메서드
    loadNotices,
    showNoticeDetail,
    editNoticeDetail,
    closeModals,
    createNotice,
    updateNotice,
    deleteNotice,
    getAuthorName,
    resetFilters
  }
}