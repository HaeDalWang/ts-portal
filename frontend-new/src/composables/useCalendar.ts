/**
 * 일정 관리 Composable
 * Vue 3 Composition API 기반
 */

import { ref, computed } from 'vue'
import { calendarService } from '@/services/calendar'
import { useAuth } from '@/composables/useAuth'
import { EventType } from '@/types/calendar'
import type { 
  EventResponse,
  EventCreate,
  EventUpdate,
  EventStats,
  CalendarEventResponse,
  SearchParams,
  PaginationParams,
  EventTypeInfo
} from '@/types/calendar'

// 글로벌 상태 (모든 컴포넌트에서 공유)
const events = ref<EventResponse[]>([])
const todayEvents = ref<EventResponse[]>([])
const upcomingEvents = ref<EventResponse[]>([])
const calendarEvents = ref<CalendarEventResponse[]>([])
const stats = ref<EventStats | null>(null)
const eventTypes = ref<EventTypeInfo[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const total = ref(0)
const selectedDate = ref<string | null>(null)
const currentView = ref<'month' | 'week' | 'day' | 'list'>('month')

export function useCalendar() {
  // 인증 정보
  const { user, hasRole } = useAuth()

  // 계산된 속성
  const hasEvents = computed(() => events.value.length > 0)
  const hasTodayEvents = computed(() => todayEvents.value.length > 0)
  const hasUpcomingEvents = computed(() => upcomingEvents.value.length > 0)
  const totalPages = computed(() => Math.ceil(total.value / 50)) // 일정은 50개씩

  /**
   * 이벤트 목록 로드
   */
  const loadEvents = async (skip: number = 0, limit: number = 50, searchParams?: SearchParams): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      const response = await calendarService.getEvents(skip, limit, searchParams)
      events.value = response.events
      total.value = response.total
      console.log('📅 이벤트 목록 로드 성공:', response.total, '개')
      return true
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '일정을 가져올 수 없습니다.'
      error.value = errorMessage
      console.error('📅 이벤트 목록 로드 실패:', errorMessage)
      return false
      
    } finally {
      loading.value = false
    }
  }

  /**
   * 달력용 이벤트 로드
   */
  const loadCalendarEvents = async (startDate: string, endDate: string, memberId?: number): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      calendarEvents.value = await calendarService.getCalendarEvents(startDate, endDate, memberId)
      console.log('📅 달력용 이벤트 로드 성공:', calendarEvents.value.length, '개')
      return true
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '달력 이벤트를 가져올 수 없습니다.'
      error.value = errorMessage
      console.error('📅 달력용 이벤트 로드 실패:', errorMessage)
      return false
      
    } finally {
      loading.value = false
    }
  }

  /**
   * 오늘 일정 로드
   */
  const loadTodayEvents = async (): Promise<boolean> => {
    try {
      todayEvents.value = await calendarService.getTodayEvents()
      console.log('📅 오늘 일정 로드 성공:', todayEvents.value.length, '개')
      return true
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '오늘 일정을 가져올 수 없습니다.'
      error.value = errorMessage
      console.error('📅 오늘 일정 로드 실패:', errorMessage)
      return false
    }
  }

  /**
   * 다가오는 일정 로드
   */
  const loadUpcomingEvents = async (days: number = 7): Promise<boolean> => {
    try {
      upcomingEvents.value = await calendarService.getUpcomingEvents(days)
      console.log('📅 다가오는 일정 로드 성공:', upcomingEvents.value.length, '개')
      return true
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '다가오는 일정을 가져올 수 없습니다.'
      error.value = errorMessage
      console.error('📅 다가오는 일정 로드 실패:', errorMessage)
      return false
    }
  }

  /**
   * 이벤트 검색
   */
  const searchEvents = async (
    searchParams: SearchParams, 
    pagination: PaginationParams
  ): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      const response = await calendarService.searchEvents(searchParams, pagination)
      events.value = response.events
      total.value = response.total
      console.log('🔍 이벤트 검색 성공:', response.total, '개 결과')
      return true
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '검색에 실패했습니다.'
      error.value = errorMessage
      console.error('🔍 이벤트 검색 실패:', errorMessage)
      return false
      
    } finally {
      loading.value = false
    }
  }

  /**
   * 이벤트 통계 로드
   */
  const loadStats = async (): Promise<boolean> => {
    try {
      stats.value = await calendarService.getEventStats()
      console.log('📊 이벤트 통계 로드 성공')
      return true
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '통계를 가져올 수 없습니다.'
      error.value = errorMessage
      console.error('📊 이벤트 통계 로드 실패:', errorMessage)
      return false
    }
  }

  /**
   * 이벤트 타입 목록 로드
   */
  const loadEventTypes = async (): Promise<boolean> => {
    try {
      eventTypes.value = await calendarService.getEventTypes()
      console.log('📊 이벤트 타입 목록 로드 성공:', eventTypes.value.length, '개')
      return true
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '이벤트 타입 정보를 가져올 수 없습니다.'
      error.value = errorMessage
      console.error('📊 이벤트 타입 목록 로드 실패:', errorMessage)
      return false
    }
  }

  /**
   * 이벤트 생성
   */
  const createEvent = async (eventData: EventCreate): Promise<EventResponse | null> => {
    loading.value = true
    error.value = null

    try {
      const newEvent = await calendarService.createEvent(eventData)
      // 목록에 새 이벤트 추가
      events.value.unshift(newEvent)
      total.value += 1
      console.log('📝 이벤트 생성 성공:', newEvent.id)
      return newEvent
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '이벤트 생성에 실패했습니다.'
      error.value = errorMessage
      console.error('📝 이벤트 생성 실패:', errorMessage)
      return null
      
    } finally {
      loading.value = false
    }
  }

  /**
   * 이벤트 수정
   */
  const updateEvent = async (eventId: number, eventData: EventUpdate): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      const updatedEvent = await calendarService.updateEvent(eventId, eventData)
      // 목록에서 해당 이벤트 업데이트
      const index = events.value.findIndex(event => event.id === eventId)
      if (index !== -1) {
        events.value[index] = updatedEvent
      }
      console.log('✏️ 이벤트 수정 성공:', eventId)
      return true
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '이벤트 수정에 실패했습니다.'
      error.value = errorMessage
      console.error('✏️ 이벤트 수정 실패:', errorMessage)
      return false
      
    } finally {
      loading.value = false
    }
  }

  /**
   * 이벤트 삭제
   */
  const deleteEvent = async (eventId: number): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      await calendarService.deleteEvent(eventId)
      // 목록에서 해당 이벤트 제거
      events.value = events.value.filter(event => event.id !== eventId)
      total.value -= 1
      console.log('🗑️ 이벤트 삭제 성공:', eventId)
      return true
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '이벤트 삭제에 실패했습니다.'
      error.value = errorMessage
      console.error('🗑️ 이벤트 삭제 실패:', errorMessage)
      return false
      
    } finally {
      loading.value = false
    }
  }

  /**
   * 이벤트 수정 권한 체크
   */
  const canEditEvent = (event: EventResponse): boolean => {
    if (!user.value) return false
    
    // 작성자 본인이거나 관리자인 경우
    return event.created_by === user.value.id || hasRole('admin')
  }

  /**
   * 이벤트 삭제 권한 체크
   */
  const canDeleteEvent = (event: EventResponse): boolean => {
    if (!user.value) return false
    
    // 작성자 본인이거나 관리자인 경우
    return event.created_by === user.value.id || hasRole('admin')
  }

  /**
   * 이벤트 타입별 정보 반환
   */
  const getEventTypeInfo = (eventType: EventType): EventTypeInfo | undefined => {
    return eventTypes.value.find(type => type.value === eventType)
  }

  /**
   * 날짜 포맷팅
   */
  const formatDate = (dateString: string): string => {
    return calendarService.formatDate(dateString)
  }

  /**
   * 시간 포맷팅
   */
  const formatTime = (dateString: string): string => {
    return calendarService.formatTime(dateString)
  }

  /**
   * 날짜+시간 포맷팅
   */
  const formatDateTime = (dateString: string): string => {
    return calendarService.formatDateTime(dateString)
  }

  /**
   * 에러 초기화
   */
  const clearError = (): void => {
    error.value = null
  }

  /**
   * 현재 보기 변경
   */
  const setCurrentView = (view: 'month' | 'week' | 'day' | 'list'): void => {
    currentView.value = view
  }

  /**
   * 선택된 날짜 설정
   */
  const setSelectedDate = (date: string | null): void => {
    selectedDate.value = date
  }

  /**
   * 전체 새로고침
   */
  const refresh = async (): Promise<void> => {
    console.log('📅 일정 전체 새로고침 시작')
    await Promise.all([
      loadEvents(),
      loadTodayEvents(),
      loadUpcomingEvents(),
      loadStats(),
      loadEventTypes()
    ])
    console.log('📅 일정 전체 새로고침 완료')
  }

  return {
    // 상태
    events: computed(() => events.value),
    todayEvents: computed(() => todayEvents.value),
    upcomingEvents: computed(() => upcomingEvents.value),
    calendarEvents: computed(() => calendarEvents.value),
    stats: computed(() => stats.value),
    eventTypes: computed(() => eventTypes.value),
    loading: computed(() => loading.value),
    error: computed(() => error.value),
    total: computed(() => total.value),
    selectedDate: computed(() => selectedDate.value),
    currentView: computed(() => currentView.value),
    hasEvents,
    hasTodayEvents,
    hasUpcomingEvents,
    totalPages,
    
    // 메서드
    loadEvents,
    loadCalendarEvents,
    loadTodayEvents,
    loadUpcomingEvents,
    searchEvents,
    loadStats,
    loadEventTypes,
    createEvent,
    updateEvent,
    deleteEvent,
    canEditEvent,
    canDeleteEvent,
    getEventTypeInfo,
    formatDate,
    formatTime,
    formatDateTime,
    clearError,
    setCurrentView,
    setSelectedDate,
    refresh
  }
} 