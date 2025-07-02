/**
 * 공지사항 관리 Composable
 * Vue 3 Composition API 기반
 */

import { ref, computed } from 'vue'
import { noticesService } from '@/services/notices'
import { useAuth } from '@/composables/useAuth'
import { NoticePriority } from '@/types/notices'
import type { 
  NoticeResponse,
  NoticeCreate,
  NoticeUpdate,
  NoticeStats,
  SearchParams,
  PaginationParams,
  PriorityInfo
} from '@/types/notices'

// 글로벌 상태 (모든 컴포넌트에서 공유)
const notices = ref<NoticeResponse[]>([])
const pinnedNotices = ref<NoticeResponse[]>([])
const recentNotices = ref<NoticeResponse[]>([])
const stats = ref<NoticeStats | null>(null)
const priorities = ref<PriorityInfo[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const total = ref(0)

export function useNotices() {
  // 인증 정보
  const { user, hasRole } = useAuth()

  // 계산된 속성
  const hasNotices = computed(() => notices.value.length > 0)
  const hasPinnedNotices = computed(() => pinnedNotices.value.length > 0)
  const totalPages = computed(() => Math.ceil(total.value / 20))

  /**
   * 공지사항 목록 로드
   */
  const loadNotices = async (skip: number = 0, limit: number = 20): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      const response = await noticesService.getNotices(skip, limit)
      notices.value = response.notices
      total.value = response.total
      console.log('📋 공지사항 목록 로드 성공:', response.total, '개')
      return true
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '공지사항을 가져올 수 없습니다.'
      error.value = errorMessage
      console.error('📋 공지사항 목록 로드 실패:', errorMessage)
      return false
      
    } finally {
      loading.value = false
    }
  }

  /**
   * 공지사항 검색
   */
  const searchNotices = async (
    searchParams: SearchParams, 
    pagination: PaginationParams
  ): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      const response = await noticesService.searchNotices(searchParams, pagination)
      notices.value = response.notices
      total.value = response.total
      console.log('🔍 공지사항 검색 성공:', response.total, '개 결과')
      return true
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '검색에 실패했습니다.'
      error.value = errorMessage
      console.error('🔍 공지사항 검색 실패:', errorMessage)
      return false
      
    } finally {
      loading.value = false
    }
  }

  /**
   * 고정 공지사항 로드
   */
  const loadPinnedNotices = async (): Promise<boolean> => {
    try {
      pinnedNotices.value = await noticesService.getPinnedNotices()
      console.log('📌 고정 공지사항 로드 성공:', pinnedNotices.value.length, '개')
      return true
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '고정 공지사항을 가져올 수 없습니다.'
      error.value = errorMessage
      console.error('📌 고정 공지사항 로드 실패:', errorMessage)
      return false
    }
  }

  /**
   * 최근 공지사항 로드
   */
  const loadRecentNotices = async (days: number = 7, limit: number = 5): Promise<boolean> => {
    try {
      recentNotices.value = await noticesService.getRecentNotices(days, limit)
      console.log('📅 최근 공지사항 로드 성공:', recentNotices.value.length, '개')
      return true
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '최근 공지사항을 가져올 수 없습니다.'
      error.value = errorMessage
      console.error('📅 최근 공지사항 로드 실패:', errorMessage)
      return false
    }
  }

  /**
   * 공지사항 통계 로드
   */
  const loadStats = async (): Promise<boolean> => {
    try {
      stats.value = await noticesService.getNoticeStats()
      console.log('📊 공지사항 통계 로드 성공')
      return true
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '통계를 가져올 수 없습니다.'
      error.value = errorMessage
      console.error('📊 공지사항 통계 로드 실패:', errorMessage)
      return false
    }
  }

  /**
   * 우선순위 목록 로드
   */
  const loadPriorities = async (): Promise<boolean> => {
    try {
      priorities.value = await noticesService.getPriorities()
      console.log('📊 우선순위 목록 로드 성공:', priorities.value.length, '개')
      return true
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '우선순위 정보를 가져올 수 없습니다.'
      error.value = errorMessage
      console.error('📊 우선순위 목록 로드 실패:', errorMessage)
      return false
    }
  }

  /**
   * 공지사항 생성
   */
  const createNotice = async (noticeData: NoticeCreate): Promise<NoticeResponse | null> => {
    loading.value = true
    error.value = null

    try {
      const newNotice = await noticesService.createNotice(noticeData)
      // 목록에 새 공지사항 추가 (상단에)
      notices.value.unshift(newNotice)
      total.value += 1
      console.log('📝 공지사항 생성 성공:', newNotice.id)
      return newNotice
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '공지사항 생성에 실패했습니다.'
      error.value = errorMessage
      console.error('📝 공지사항 생성 실패:', errorMessage)
      return null
      
    } finally {
      loading.value = false
    }
  }

  /**
   * 공지사항 수정
   */
  const updateNotice = async (noticeId: number, noticeData: NoticeUpdate): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      const updatedNotice = await noticesService.updateNotice(noticeId, noticeData)
      // 목록에서 해당 공지사항 업데이트
      const index = notices.value.findIndex(notice => notice.id === noticeId)
      if (index !== -1) {
        notices.value[index] = updatedNotice
      }
      console.log('✏️ 공지사항 수정 성공:', noticeId)
      return true
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '공지사항 수정에 실패했습니다.'
      error.value = errorMessage
      console.error('✏️ 공지사항 수정 실패:', errorMessage)
      return false
      
    } finally {
      loading.value = false
    }
  }

  /**
   * 공지사항 삭제
   */
  const deleteNotice = async (noticeId: number): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      await noticesService.deleteNotice(noticeId)
      // 목록에서 해당 공지사항 제거
      notices.value = notices.value.filter(notice => notice.id !== noticeId)
      total.value -= 1
      console.log('🗑️ 공지사항 삭제 성공:', noticeId)
      return true
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '공지사항 삭제에 실패했습니다.'
      error.value = errorMessage
      console.error('🗑️ 공지사항 삭제 실패:', errorMessage)
      return false
      
    } finally {
      loading.value = false
    }
  }

  /**
   * 우선순위별 생성 권한 체크
   */
  const canCreatePriority = (priority: NoticePriority): boolean => {
    if (!user.value) return false
    
    switch (priority) {
      case NoticePriority.IMPORTANT:
        return hasRole('admin')
      case NoticePriority.CAUTION:
        return hasRole('power_user')
      case NoticePriority.NORMAL:
        return true
      default:
        return false
    }
  }

  /**
   * 우선순위별 삭제 권한 체크
   */
  const canDeleteNotice = (notice: NoticeResponse): boolean => {
    if (!user.value) return false
    
    // 작성자 본인은 항상 삭제 가능
    if (notice.author_id === user.value.id) return true
    
    // 관리자는 모든 공지사항 삭제 가능
    if (hasRole('admin')) return true
    
    // 우선순위별 권한 체크
    switch (notice.priority) {
      case NoticePriority.IMPORTANT:
        return hasRole('admin')
      case NoticePriority.CAUTION:
        return hasRole('power_user')
      case NoticePriority.NORMAL:
        return true // 일반 공지사항은 누구나 삭제 가능
      default:
        return true // 기본적으로 삭제 가능
    }
  }

  /**
   * 날짜 포맷팅
   */
  const formatDate = (dateString: string): string => {
    return noticesService.formatDate(dateString)
  }

  /**
   * 에러 초기화
   */
  const clearError = (): void => {
    error.value = null
  }

  /**
   * 전체 새로고침
   */
  const refresh = async (): Promise<void> => {
    console.log('📋 공지사항 전체 새로고침 시작')
    await Promise.all([
      loadNotices(),
      loadPinnedNotices(),
      loadRecentNotices(),
      loadStats(),
      loadPriorities()
    ])
    console.log('📋 공지사항 전체 새로고침 완료')
  }

  return {
    // 상태
    notices: computed(() => notices.value),
    pinnedNotices: computed(() => pinnedNotices.value),
    recentNotices: computed(() => recentNotices.value),
    stats: computed(() => stats.value),
    priorities: computed(() => priorities.value),
    loading: computed(() => loading.value),
    error: computed(() => error.value),
    total: computed(() => total.value),
    hasNotices,
    hasPinnedNotices,
    totalPages,
    
    // 메서드
    loadNotices,
    searchNotices,
    loadPinnedNotices,
    loadRecentNotices,
    loadStats,
    loadPriorities,
    createNotice,
    updateNotice,
    deleteNotice,
    canCreatePriority,
    canDeleteNotice,
    formatDate,
    clearError,
    refresh
  }
} 