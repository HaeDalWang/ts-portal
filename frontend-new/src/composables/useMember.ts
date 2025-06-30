/**
 * Member Service 상태 관리 Composable
 * Vue 3 Composition API 기반
 */

import { ref, computed, reactive } from 'vue'
import { memberService } from '@/services/member'
import type { Member, MemberListResponse, MemberSearchParams, MemberState } from '@/types/member'

// 글로벌 상태
const state = reactive<MemberState>({
  members: [],
  currentMember: null,
  loading: false,
  error: null,
  totalCount: 0,
  currentPage: 1,
  pageSize: 20
})

export function useMember() {
  // 계산된 속성
  const totalPages = computed(() => Math.ceil(state.totalCount / state.pageSize))
  const hasMembers = computed(() => state.members.length > 0)
  const isEmpty = computed(() => !state.loading && state.members.length === 0)

  /**
   * 팀원 목록 조회
   */
  const fetchMembers = async (params?: MemberSearchParams): Promise<void> => {
    state.loading = true
    state.error = null

    try {
      console.log('👥 팀원 목록 조회 시작:', params)
      
      const searchParams = {
        page: state.currentPage,
        size: state.pageSize,
        ...params
      }

      const response: MemberListResponse = await memberService.getMembers(searchParams)
      
      state.members = response.items
      state.totalCount = response.total
      state.currentPage = response.page
      
      console.log('👥 팀원 목록 조회 성공:', {
        count: response.items.length,
        total: response.total,
        page: response.page
      })

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '팀원 목록을 가져올 수 없습니다.'
      state.error = errorMessage
      console.error('👥 팀원 목록 조회 실패:', errorMessage)
    } finally {
      state.loading = false
    }
  }

  /**
   * 팀원 상세 정보 조회
   */
  const fetchMember = async (id: number): Promise<void> => {
    state.loading = true
    state.error = null

    try {
      console.log('👤 팀원 상세 조회:', id)
      
      const member = await memberService.getMember(id)
      state.currentMember = member
      
      console.log('👤 팀원 상세 조회 성공:', member.name)

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '팀원 정보를 가져올 수 없습니다.'
      state.error = errorMessage
      console.error('👤 팀원 상세 조회 실패:', errorMessage)
    } finally {
      state.loading = false
    }
  }

  /**
   * 팀별 팀원 목록 조회
   */
  const fetchMembersByTeam = async (team: string): Promise<void> => {
    await fetchMembers({ team, is_active: true })
  }

  /**
   * 팀원 검색
   */
  const searchMembers = async (searchTerm: string): Promise<void> => {
    await fetchMembers({ search: searchTerm, is_active: true })
  }

  /**
   * 페이지 변경
   */
  const changePage = async (page: number): Promise<void> => {
    if (page < 1 || page > totalPages.value) return
    
    state.currentPage = page
    await fetchMembers()
  }

  /**
   * 페이지 크기 변경
   */
  const changePageSize = async (size: number): Promise<void> => {
    state.pageSize = size
    state.currentPage = 1
    await fetchMembers()
  }

  /**
   * 팀 목록 조회
   */
  const fetchTeams = async (): Promise<string[]> => {
    try {
      return await memberService.getTeams()
    } catch (err) {
      console.error('팀 목록 조회 실패:', err)
      return []
    }
  }

  /**
   * 직책 목록 조회
   */
  const fetchPositions = async (): Promise<string[]> => {
    try {
      return await memberService.getPositions()
    } catch (err) {
      console.error('직책 목록 조회 실패:', err)
      return []
    }
  }

  /**
   * 팀별 통계 조회
   */
  const fetchTeamStats = async (): Promise<Record<string, number>> => {
    try {
      return await memberService.getTeamStats()
    } catch (err) {
      console.error('팀별 통계 조회 실패:', err)
      return {}
    }
  }

  /**
   * 에러 초기화
   */
  const clearError = (): void => {
    state.error = null
  }

  /**
   * 상태 초기화
   */
  const reset = (): void => {
    state.members = []
    state.currentMember = null
    state.loading = false
    state.error = null
    state.totalCount = 0
    state.currentPage = 1
  }

  /**
   * 팀별 그룹핑
   */
  const membersByTeam = computed(() => {
    const grouped: Record<string, Member[]> = {}
    
    state.members.forEach(member => {
      if (!grouped[member.team]) {
        grouped[member.team] = []
      }
      grouped[member.team].push(member)
    })

    return grouped
  })

  /**
   * 활성 팀원만 필터링
   */
  const activeMembers = computed(() => {
    return state.members.filter(member => member.is_active)
  })

  return {
    // 상태
    members: computed(() => state.members),
    currentMember: computed(() => state.currentMember),
    loading: computed(() => state.loading),
    error: computed(() => state.error),
    totalCount: computed(() => state.totalCount),
    currentPage: computed(() => state.currentPage),
    pageSize: computed(() => state.pageSize),
    totalPages,
    hasMembers,
    isEmpty,
    membersByTeam,
    activeMembers,

    // 메서드
    fetchMembers,
    fetchMember,
    fetchMembersByTeam,
    searchMembers,
    changePage,
    changePageSize,
    fetchTeams,
    fetchPositions,
    fetchTeamStats,
    clearError,
    reset
  }
} 