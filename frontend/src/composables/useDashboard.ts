import { ref, computed } from 'vue'
import { EventService, EVENT_TYPES, type EventResponse, type EventStats, type CalendarEventResponse } from '@/services/eventService'
import { memberService } from '@/services/memberService'
import type { Member } from '@/types'

export function useDashboard() {
  // 반응형 데이터
  const loading = ref(true)
  const stats = ref<EventStats>({
    total_events: 0,
    today_events: 0,
    upcoming_events: 0,
    ongoing_events: 0,
    completed_events: 0,
    events_by_type: {},
    events_by_member: {}
  })
  const members = ref<Member[]>([])
  const todayEvents = ref<EventResponse[]>([])
  const selectedMembers = ref<Set<number>>(new Set())
  const isAllSelected = ref(true)
  const currentView = ref('dayGridMonth')
  
  // 모달 관련 데이터
  const showEventModal = ref(false)
  const selectedDate = ref<string>('')
  const selectedDateEvents = ref<EventResponse[]>([])
  
  // 파트별 보기 관련 데이터
  const selectedParts = ref<Set<string>>(new Set())
  const isAllPartsSelected = ref(true)
  
  // 계산된 속성
  const eventTypes = computed(() => EVENT_TYPES)
  
  const availableParts = computed(() => {
    const parts = new Set<string>()
    members.value.forEach(member => {
      parts.add(member.team || '') // team이 없으면 빈 문자열
    })
    return Array.from(parts).sort()
  })
  
  // 팀원 ID 기반 동적 색상 생성 (HSL 사용)
  const getMemberColor = (memberId: number): string => {
    // 팀원 ID를 시드로 사용하여 일관된 색상 생성
    const hue = (memberId * 137.508) % 360 // 황금각을 사용한 균등 분포
    const saturation = 45 + (memberId % 15) // 45-60% 채도로 부드러운 색상
    const lightness = 60 + (memberId % 15)  // 60-75% 명도로 옅은 색상
    
    return `hsl(${hue}, ${saturation}%, ${lightness}%)`
  }
  
  // 팀원 필터 관련 함수들
  const toggleMember = (memberId: number) => {
    if (isAllSelected.value) {
      // 전체 선택 상태에서 개별 멤버 클릭 시 -> 해당 멤버만 제외하고 나머지 모두 선택
      isAllSelected.value = false
      selectedMembers.value.clear()
      // 클릭한 멤버를 제외한 모든 멤버를 선택
      members.value.forEach(member => {
        if (member.id !== memberId) {
          selectedMembers.value.add(member.id)
        }
      })
    } else {
      // 개별 선택 모드에서 토글
      if (selectedMembers.value.has(memberId)) {
        selectedMembers.value.delete(memberId)
        // 모든 멤버가 해제되면 전체 선택으로 변경
        if (selectedMembers.value.size === 0) {
          isAllSelected.value = true
        }
      } else {
        selectedMembers.value.add(memberId)
        // 모든 멤버가 선택되면 전체 선택으로 변경
        if (selectedMembers.value.size === members.value.length) {
          isAllSelected.value = true
          selectedMembers.value.clear()
        }
      }
    }
  }
  
  const toggleAllMembers = () => {
    if (isAllSelected.value) {
      // 전체 선택 해제 -> 아무도 선택 안함
      isAllSelected.value = false
      selectedMembers.value.clear()
    } else {
      // 전체 선택
      isAllSelected.value = true
      selectedMembers.value.clear()
    }
  }
  
  // 파트 필터 관련 함수들
  const togglePart = (part: string) => {
    if (isAllPartsSelected.value) {
      // 전체 선택 상태에서 개별 파트 클릭 시 -> 해당 파트만 제외하고 나머지 모두 선택
      isAllPartsSelected.value = false
      selectedParts.value.clear()
      // 클릭한 파트를 제외한 모든 파트를 선택
      availableParts.value.forEach(p => {
        if (p !== part) {
          selectedParts.value.add(p)
        }
      })
    } else {
      // 개별 선택 모드에서 토글
      if (selectedParts.value.has(part)) {
        selectedParts.value.delete(part)
        // 모든 파트가 해제되면 전체 선택으로 변경
        if (selectedParts.value.size === 0) {
          isAllPartsSelected.value = true
        }
      } else {
        selectedParts.value.add(part)
        // 모든 파트가 선택되면 전체 선택으로 변경
        if (selectedParts.value.size === availableParts.value.length) {
          isAllPartsSelected.value = true
          selectedParts.value.clear()
        }
      }
    }
  }
  
  const toggleAllParts = () => {
    if (isAllPartsSelected.value) {
      // 전체 선택 해제 -> 아무 파트도 선택 안함
      isAllPartsSelected.value = false
      selectedParts.value.clear()
    } else {
      // 전체 선택
      isAllPartsSelected.value = true
      selectedParts.value.clear()
    }
  }
  
  // 이벤트 로딩 함수
  async function loadEvents(info: any): Promise<CalendarEventResponse[]> {
    try {
      const start = info.start.toISOString().split('T')[0]
      const end = info.end.toISOString().split('T')[0]
      
      // 팀원 필터 적용
      let targetMemberIds: number[] = []
      
      if (isAllSelected.value || selectedMembers.value.size === 0) {
        // 전체 팀원 선택 시 모든 팀원
        targetMemberIds = members.value.map(m => m.id)
      } else {
        // 선택된 팀원들만
        targetMemberIds = Array.from(selectedMembers.value)
      }
      
      // 파트 필터 추가 적용
      if (!isAllPartsSelected.value && selectedParts.value.size > 0) {
        // 선택된 파트에 속한 팀원들만 필터링
        const partFilteredMemberIds = members.value
          .filter(member => selectedParts.value.has(member.team || ''))
          .map(m => m.id)
        
        // 팀원 필터와 파트 필터의 교집합
        targetMemberIds = targetMemberIds.filter(id => partFilteredMemberIds.includes(id))
      }
      
      // 선택된 팀원들의 이벤트를 병렬로 로드
      if (targetMemberIds.length === 0) {
        return []
      }
      
      if (targetMemberIds.length === members.value.length && (isAllSelected.value || selectedMembers.value.size === 0) && isAllPartsSelected.value) {
        // 모든 필터가 전체 선택된 경우 전체 이벤트 로드
        return await EventService.getCalendarEvents(start, end)
      } else {
        // 선택된 팀원들의 이벤트를 병렬로 로드
        const eventPromises = targetMemberIds.map(memberId =>
          EventService.getCalendarEvents(start, end, memberId)
        )
        const eventsArrays = await Promise.all(eventPromises)
        return eventsArrays.flat()
      }
    } catch (error) {
      console.error('이벤트 로딩 실패:', error)
      return []
    }
  }
  
  // 대시보드 데이터 로딩
  const loadDashboardData = async () => {
    try {
      loading.value = true
      
      // 병렬로 데이터 로딩
      const [statsData, membersData, todayEventsData] = await Promise.all([
        EventService.getEventStats(),
        memberService.getMembers(),
        EventService.getTodayEvents()
      ])
      
      stats.value = statsData
      members.value = membersData.members
      todayEvents.value = todayEventsData
      
    } catch (error) {
      console.error('대시보드 데이터 로딩 실패:', error)
    } finally {
      loading.value = false
    }
  }
  
  // 모달 관련 함수들
  const openEventModal = async (dateStr: string) => {
    selectedDate.value = dateStr
    showEventModal.value = true
    
    try {
      // 선택된 날짜의 이벤트들을 가져오기
      const response = await EventService.getEvents({
        start_date: dateStr,
        end_date: dateStr
      })
      selectedDateEvents.value = response.events
    } catch (error) {
      console.error('이벤트 로딩 실패:', error)
      selectedDateEvents.value = []
    }
  }
  
  const closeEventModal = () => {
    showEventModal.value = false
    selectedDate.value = ''
    selectedDateEvents.value = []
  }
  
  // 유틸리티 함수들
  const formatTime = (timeString: string): string => {
    const date = new Date(timeString)
    return date.toLocaleTimeString('ko-KR', { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: false 
    })
  }
  
  const getEventTypeIcon = (eventType: string): string => {
    const type = EVENT_TYPES.find(t => t.value === eventType)
    return type?.icon || '📅'
  }
  
  const getStatusText = (status: string): string => {
    const statusMap: { [key: string]: string } = {
      'scheduled': '예정',
      'in_progress': '진행중',
      'completed': '완료',
      'cancelled': '취소'
    }
    return statusMap[status] || status
  }
  
  const getStatusBadgeClass = (status: string): string => {
    const classMap: { [key: string]: string } = {
      'scheduled': 'bg-blue-100 text-blue-800',
      'in_progress': 'bg-yellow-100 text-yellow-800',
      'completed': 'bg-green-100 text-green-800',
      'cancelled': 'bg-red-100 text-red-800'
    }
    return classMap[status] || 'bg-gray-100 text-gray-800'
  }
  
  const formatEventTime = (event: EventResponse): string => {
    if (event.all_day) {
      return '종일'
    }
    
    const startTime = formatTime(event.start_time)
    const endTime = event.end_time ? formatTime(event.end_time) : ''
    return endTime ? `${startTime} - ${endTime}` : startTime
  }
  
  const refreshCalendar = () => {
    // 달력 새로고침 로직은 컴포넌트에서 처리
  }
  
  // 초기화
  loadDashboardData()
  
  return {
    // 상태
    loading,
    stats,
    members,
    todayEvents,
    selectedMembers,
    isAllSelected,
    currentView,
    showEventModal,
    selectedDate,
    selectedDateEvents,
    selectedParts,
    isAllPartsSelected,
    eventTypes,
    availableParts,
    
    // 메서드
    loadEvents,
    getMemberColor,
    toggleMember,
    toggleAllMembers,
    togglePart,
    toggleAllParts,
    openEventModal,
    closeEventModal,
    getEventTypeIcon,
    getStatusBadgeClass,
    getStatusText,
    formatEventTime,
    refreshCalendar,
    loadDashboardData
  }
} 