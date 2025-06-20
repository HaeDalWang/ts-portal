<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 컴팩트 헤더 -->
    <div class="bg-white border-b border-gray-200 px-6 py-3">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-xl font-bold text-gray-900">팀 대시보드</h1>
          <p class="text-sm text-gray-500">TS팀 일정 관리</p>
        </div>
        
        <!-- 컴팩트 통계 -->
        <div class="flex items-center space-x-6">
          <div class="text-center">
            <div class="text-lg font-semibold text-blue-600">{{ stats.total_events }}</div>
            <div class="text-xs text-gray-500">전체</div>
          </div>
          <div class="text-center">
            <div class="text-lg font-semibold text-green-600">{{ stats.today_events }}</div>
            <div class="text-xs text-gray-500">오늘</div>
          </div>
          <div class="text-center">
            <div class="text-lg font-semibold text-yellow-600">{{ stats.upcoming_events }}</div>
            <div class="text-xs text-gray-500">예정</div>
          </div>
          <div class="text-center">
            <div class="text-lg font-semibold text-red-600">{{ stats.ongoing_events }}</div>
            <div class="text-xs text-gray-500">진행중</div>
          </div>
        </div>
      </div>
    </div>

    <div class="flex h-screen">
      <!-- 좌측 사이드바 - 최대한 좁게 -->
      <div class="w-32 bg-white border-r border-gray-200 flex flex-col">
        <!-- 필터 및 컨트롤 -->
        <div class="p-2 border-b border-gray-100 flex-shrink-0">
          <div class="space-y-3">
            <!-- 뷰 타입 드롭다운 -->
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">보기 방식</label>
              <div class="relative">
                <select 
                  v-model="currentView" 
                  @change="changeCalendarView(currentView)"
                  class="w-full px-2 py-1 text-xs border border-gray-300 rounded bg-white text-gray-700 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="dayGridMonth">📅 월간 보기</option>
                  <option value="timeGridWeek">📊 주간 보기</option>
                  <option value="timeGridDay">📋 일간 보기</option>
                </select>
              </div>
            </div>

            <!-- 팀원 선택 -->
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">팀원</label>
              <div class="space-y-1 max-h-80 overflow-y-auto">
                <label class="flex items-center space-x-1 text-xs">
                  <input
                    type="checkbox"
                    :checked="isAllSelected"
                    @change="toggleAllMembers"
                    class="rounded border-gray-300 text-blue-600 focus:ring-blue-500 w-3 h-3"
                  />
                  <span class="font-medium text-gray-600 text-xs">전체</span>
                </label>
                <hr class="my-1">
                <label 
                  v-for="member in members" 
                  :key="member.id" 
                  class="flex items-center space-x-1 text-xs cursor-pointer hover:bg-gray-50 p-1 rounded"
                >
                  <input
                    type="checkbox"
                    :checked="isAllSelected || selectedMembers.has(member.id)"
                    @change="toggleMember(member.id)"
                    class="rounded border-gray-300 text-blue-600 focus:ring-blue-500 w-3 h-3"
                  />
                  <div 
                    class="w-2 h-2 rounded-full flex-shrink-0"
                    :style="{ backgroundColor: getMemberColor(member.id) }"
                  ></div>
                  <span class="text-gray-700 truncate text-xs">{{ member.name }}</span>
                </label>
              </div>
            </div>
            
            <!-- 파트 필터 -->
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">파트 필터</label>
              <div class="space-y-1 max-h-40 overflow-y-auto">
                <label class="flex items-center space-x-1 text-xs">
                  <input
                    type="checkbox"
                    :checked="isAllPartsSelected"
                    @change="toggleAllParts"
                    class="rounded border-gray-300 text-blue-600 focus:ring-blue-500 w-3 h-3"
                  />
                  <span class="font-medium text-gray-600 text-xs">전체 파트</span>
                </label>
                <hr class="my-1">
                <label 
                  v-for="part in availableParts" 
                  :key="part" 
                  class="flex items-center space-x-1 text-xs cursor-pointer hover:bg-gray-50 p-1 rounded"
                >
                  <input
                    type="checkbox"
                    :checked="isAllPartsSelected || selectedParts.has(part)"
                    @change="togglePart(part)"
                    class="rounded border-gray-300 text-blue-600 focus:ring-blue-500 w-3 h-3"
                  />
                  <span class="text-gray-700 truncate text-xs">{{ part || '파트 미지정' }}</span>
                  <span class="text-xs text-gray-400">({{ getPartMemberCount(part) }}명)</span>
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- 일정 유형 -->
        <div class="flex-1 overflow-y-auto min-h-0">
          <div class="p-2">
            <h4 class="text-xs font-semibold text-gray-700 mb-1">일정 유형</h4>
            <div class="space-y-1">
              <div v-for="type in eventTypes.slice(0, 6)" :key="type.value" class="flex items-center space-x-1">
                <span class="text-xs">{{ type.icon }}</span>
                <span class="text-xs text-gray-600 truncate">{{ type.label }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 메인 달력 영역 - 완전 일체화 -->
      <div class="flex-1 bg-white">
        <!-- 달력 헤더를 FullCalendar 내부로 완전 통합 -->
        <div class="h-full relative">
          <!-- 커스텀 헤더 - 절대 위치로 달력 위에 오버레이 -->
          <div class="absolute top-0 left-0 right-0 z-10 flex items-center justify-between px-4 py-1 bg-white/95 backdrop-blur-sm">
            <!-- 네비게이션 버튼들 - 더 작게 -->
            <div class="flex items-center space-x-1">
              <button @click="goToPrev" class="p-1 hover:bg-gray-200 rounded text-gray-600 hover:text-gray-900">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <button @click="goToNext" class="p-1 hover:bg-gray-200 rounded text-gray-600 hover:text-gray-900">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
              <button @click="goToToday" class="px-2 py-1 text-xs bg-blue-500 text-white rounded hover:bg-blue-600 ml-2">
                오늘
              </button>
            </div>
            
            <!-- 현재 날짜 표시 - 더 작게 -->
            <div class="text-lg font-semibold text-gray-900">
              {{ currentTitle }}
            </div>
            
            <div class="w-16"></div> <!-- 균형을 위한 빈 공간 -->
          </div>
          
          <!-- 달력 본체 - 전체 영역 사용 -->
          <div class="h-full pt-8">
            <FullCalendar
              ref="fullCalendar"
              :options="calendarOptions"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- 날짜별 이벤트 모달 -->
    <div v-if="showEventModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="closeEventModal">
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[80vh] overflow-hidden" @click.stop>
        <!-- 모달 헤더 -->
        <div class="px-6 py-4 border-b border-gray-200 bg-gray-50">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-semibold text-gray-900">{{ formatSelectedDate(selectedDate) }}</h3>
              <p class="text-sm text-gray-500">{{ selectedDateEvents.length }}개의 일정</p>
            </div>
            <button @click="closeEventModal" class="text-gray-400 hover:text-gray-600 transition-colors">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <!-- 모달 내용 -->
        <div class="px-6 py-4 overflow-y-auto max-h-[60vh]">
          <div v-if="selectedDateEvents.length === 0" class="text-center py-8">
            <div class="text-gray-400 mb-2">
              <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <p class="text-gray-500">이 날에는 일정이 없습니다.</p>
          </div>

          <div v-else class="space-y-3">
            <div 
              v-for="event in selectedDateEvents" 
              :key="event.id"
              class="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors"
            >
              <div class="flex items-start space-x-3">
                <!-- 이벤트 타입 아이콘 -->
                <div class="flex-shrink-0">
                  <span class="text-2xl">{{ getEventTypeIcon(event.event_type) }}</span>
                </div>
                
                <!-- 이벤트 정보 -->
                <div class="flex-1 min-w-0">
                  <div class="flex items-center space-x-2 mb-1">
                    <h4 class="text-base font-medium text-gray-900 truncate">{{ event.title }}</h4>
                    <span 
                      class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
                      :class="getStatusBadgeClass(event.status)"
                    >
                      {{ getStatusText(event.status) }}
                    </span>
                  </div>
                  
                  <div class="text-sm text-gray-600 mb-2">
                    <div class="flex items-center space-x-4">
                      <span class="flex items-center">
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        {{ formatEventTime(event) }}
                      </span>
                      <span v-if="event.creator?.name" class="flex items-center">
                        <div 
                          class="w-3 h-3 rounded-full mr-1"
                          :style="{ backgroundColor: getMemberColor(event.created_by) }"
                        ></div>
                        {{ event.creator.name }}
                      </span>
                    </div>
                  </div>
                  
                  <p v-if="event.description" class="text-sm text-gray-600 line-clamp-2">
                    {{ event.description }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 모달 푸터 -->
        <div class="px-6 py-4 border-t border-gray-200 bg-gray-50">
          <div class="flex justify-end">
            <button 
              @click="closeEventModal"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              닫기
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import koLocale from '@fullcalendar/core/locales/ko'

import { EventService, EVENT_TYPES, type EventResponse, type EventStats, type CalendarEventResponse } from '@/services/eventService'
import { memberService } from '@/services/memberService'
import type { Member } from '@/types'

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
const selectedMembers = ref<Set<number>>(new Set()) // 다중 선택을 위한 Set
const isAllSelected = ref(true) // 전체 선택 상태
const currentView = ref('dayGridMonth')
const fullCalendar = ref()
const currentTitle = ref('')

// 모달 관련 데이터
const showEventModal = ref(false)
const selectedDate = ref<string>('')
const selectedDateEvents = ref<EventResponse[]>([])

// 파트별 보기 관련 데이터
const selectedParts = ref<Set<string>>(new Set())
const isAllPartsSelected = ref(true)

// 계산된 속성
const eventTypes = computed(() => EVENT_TYPES)

// 파트 관련 계산된 속성
const availableParts = computed(() => {
  const parts = new Set<string>()
  members.value.forEach(member => {
    parts.add(member.team || '') // team이 없으면 빈 문자열
  })
  return Array.from(parts).sort()
})

const getPartMemberCount = (part: string) => {
  return members.value.filter(member => (member.team || '') === part).length
}

// 팀원 ID 기반 동적 색상 생성 (HSL 사용)
const generateMemberColor = (memberId: number): string => {
  // 팀원 ID를 시드로 사용하여 일관된 색상 생성
  const hue = (memberId * 137.508) % 360 // 황금각을 사용한 균등 분포
  const saturation = 45 + (memberId % 15) // 45-60% 채도로 부드러운 색상
  const lightness = 60 + (memberId % 15)  // 60-75% 명도로 옅은 색상
  
  return `hsl(${hue}, ${saturation}%, ${lightness}%)`
}

// FullCalendar 옵션 - 최대한 크게 설정
const calendarOptions = ref({
  plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
  initialView: 'dayGridMonth',
  locale: koLocale,
  headerToolbar: {
    left: '',
    center: '',
    right: ''
  }, // 기본 헤더 툴바 제거
  height: '100%', // 전체 높이 사용
  events: loadEvents,
  eventDidMount: (info: any) => {
    // 툴크 추가
    info.el.title = `${info.event.title}\n${info.event.extendedProps.description || ''}`
  },
  datesSet: (dateInfo: any) => {
    // 날짜가 변경될 때마다 타이틀 업데이트
    updateCurrentTitle()
  },
  dateClick: (info: any) => {
    // 날짜 클릭 시 해당 날짜의 이벤트 모달 표시
    openEventModal(info.dateStr)
  },
  // 달력 셀 크기 최적화
  dayMaxEvents: false,
  moreLinkClick: 'popover',
  eventDisplay: 'block',
  // 폰트 크기 조정
  eventTextColor: '#ffffff',
  // 주간/일간 뷰에서 시간 슬롯 조정
  slotMinTime: '07:00:00',
  slotMaxTime: '22:00:00',
  allDaySlot: true,
  // 더 나은 시각적 효과
  nowIndicator: true,
  selectMirror: true,
  // 달력 셀 높이 최대화
  aspectRatio: 1.0,
  // 이벤트 간격 조정
  eventMinHeight: 20,
  // 달력 셀 패딩 증가
  dayCellContent: (arg: any) => {
    return { html: `<div class="custom-day-number">${arg.dayNumberText}</div>` }
  }
})

// 메서드들
const getMemberColor = (memberId: number): string => {
  return generateMemberColor(memberId)
}

const formatTime = (timeString: string): string => {
  const date = new Date(timeString)
  return date.toLocaleTimeString('ko-KR', { 
    hour: '2-digit', 
    minute: '2-digit',
    hour12: false 
  })
}

const changeCalendarView = (viewName: string) => {
  currentView.value = viewName
  const calendarApi = fullCalendar.value?.getApi()
  if (calendarApi) {
    calendarApi.changeView(viewName)
  }
}

// 달력 네비게이션 메서드들
const goToPrev = () => {
  const calendarApi = fullCalendar.value?.getApi()
  if (calendarApi) {
    calendarApi.prev()
    updateCurrentTitle()
  }
}

const goToNext = () => {
  const calendarApi = fullCalendar.value?.getApi()
  if (calendarApi) {
    calendarApi.next()
    updateCurrentTitle()
  }
}

const goToToday = () => {
  const calendarApi = fullCalendar.value?.getApi()
  if (calendarApi) {
    calendarApi.today()
    updateCurrentTitle()
  }
}

const updateCurrentTitle = () => {
  const calendarApi = fullCalendar.value?.getApi()
  if (calendarApi) {
    currentTitle.value = calendarApi.view.title
  }
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
  
  // 달력 이벤트 새로고침
  const calendarApi = fullCalendar.value?.getApi()
  if (calendarApi) {
    calendarApi.refetchEvents()
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
  
  // 달력 이벤트 새로고침
  const calendarApi = fullCalendar.value?.getApi()
  if (calendarApi) {
    calendarApi.refetchEvents()
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
  
  // 달력 이벤트 새로고침
  const calendarApi = fullCalendar.value?.getApi()
  if (calendarApi) {
    calendarApi.refetchEvents()
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
  
  // 달력 이벤트 새로고침
  const calendarApi = fullCalendar.value?.getApi()
  if (calendarApi) {
    calendarApi.refetchEvents()
  }
}

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
    
    // 팀원 데이터 로드 후 달력 새로고침
    setTimeout(() => {
      const calendarApi = fullCalendar.value?.getApi()
      if (calendarApi) {
        calendarApi.refetchEvents()
      }
    }, 100)
    
  } catch (error) {
    console.error('대시보드 데이터 로딩 실패:', error)
  } finally {
    loading.value = false
  }
}

// 컴포넌트 마운트 시 데이터 로딩
onMounted(() => {
  loadDashboardData()
  // 초기 타이틀 설정 (약간의 지연 후)
  setTimeout(() => {
    updateCurrentTitle()
  }, 100)
})

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

const formatSelectedDate = (dateStr: string): string => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
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
</script>

<style scoped>
/* FullCalendar 완전 일체화 스타일 */
:deep(.fc) {
  font-family: 'Segoe UI', system-ui, sans-serif;
  margin: 0 !important;
  padding: 0 !important;
  border: none !important;
}

:deep(.fc-view-harness) {
  margin: 0 !important;
  padding: 0 !important;
  border: none !important;
}

:deep(.fc-daygrid) {
  margin: 0 !important;
  padding: 0 !important;
  border: none !important;
}

:deep(.fc-scrollgrid) {
  border: none !important;
}

:deep(.fc-theme-standard .fc-scrollgrid) {
  border: none !important;
}

:deep(.fc-scrollgrid-section) {
  border: none !important;
}

:deep(.fc-scrollgrid-section-header) {
  border-top: none !important;
}

:deep(.fc-col-header) {
  border-top: none !important;
}

/* FullCalendar 툴바 완전 제거 */
:deep(.fc-header-toolbar) {
  display: none !important;
}

:deep(.fc-toolbar) {
  display: none !important;
}

:deep(.fc-toolbar-chunk) {
  display: none !important;
}

/* 툴바 관련 스타일들은 더 이상 필요 없음 */

/* 달력 셀 스타일 - 최대한 크게 */
:deep(.fc-daygrid-day) {
  border: 1px solid #e5e7eb;
  min-height: 140px !important; /* 셀 높이 더욱 증가 */
  cursor: pointer; /* 클릭 가능함을 표시 */
  transition: background-color 0.2s ease; /* 부드러운 전환 효과 */
}

/* 날짜 셀 호버 효과 */
:deep(.fc-daygrid-day:hover) {
  background-color: #f8fafc !important; /* 연한 회색 배경 */
}

/* 오늘 날짜 호버 효과 */
:deep(.fc-day-today:hover) {
  background-color: #e0f2fe !important; /* 연한 파란색 배경 */
}

:deep(.fc-daygrid-day-top) {
  padding: 0.5rem 0.75rem;
  justify-content: flex-start;
}

:deep(.fc-daygrid-day-number) {
  font-size: 0.75rem !important; /* 날짜 폰트 크기 축소 */
  font-weight: 400 !important; /* 폰트 두께 감소 */
  color: #6b7280 !important; /* 더 연한 색상 */
  padding: 2px 4px;
  transition: color 0.2s ease; /* 색상 전환 효과 */
}

/* 날짜 숫자 호버 효과 */
:deep(.fc-daygrid-day:hover .fc-daygrid-day-number) {
  color: #374151 !important; /* 호버 시 더 진한 색상 */
  font-weight: 500 !important; /* 호버 시 폰트 두께 증가 */
}

/* 달력 전체 높이 최대화 */
:deep(.fc-daygrid-body) {
  min-height: 700px;
}

:deep(.fc-daygrid-day-frame) {
  min-height: 140px !important;
  padding: 0;
}

/* 주말 스타일 */
:deep(.fc-day-sat .fc-daygrid-day-number) {
  color: #2563eb !important;
}

:deep(.fc-day-sun .fc-daygrid-day-number) {
  color: #dc2626 !important;
}

:deep(.fc-day-today) {
  background-color: #f0f9ff !important;
}

:deep(.fc-day-today .fc-daygrid-day-number) {
  color: #1d4ed8 !important;
  font-weight: 600 !important;
  font-size: 0.75rem !important; /* 오늘 날짜도 작은 폰트 유지 */
}

/* 이벤트 스타일 개선 - 더 컴팩트하게 */
:deep(.fc-event) {
  border: none !important;
  border-radius: 3px !important;
  font-size: 0.7rem !important; /* 이벤트 폰트 더 작게 */
  font-weight: 500 !important;
  padding: 1px 4px !important; /* 패딩 축소 */
  margin: 1px 2px !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  min-height: 18px !important; /* 최소 높이 설정 */
}

:deep(.fc-event-title) {
  font-weight: 500 !important;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.2;
}

:deep(.fc-daygrid-event) {
  border-radius: 3px !important;
  margin: 1px 2px !important;
  height: 18px !important; /* 이벤트 높이 고정 */
}

:deep(.fc-timegrid-event) {
  border-radius: 3px !important;
  padding: 1px 3px !important;
}

/* 이벤트가 많을 때 더 보기 링크 스타일 */
:deep(.fc-daygrid-more-link) {
  font-size: 0.65rem !important;
  color: #6b7280 !important;
  font-weight: 400 !important;
  margin: 1px 2px;
}

/* 주간/일간 뷰 스타일 */
:deep(.fc-timegrid-slot) {
  height: 3rem;
}

:deep(.fc-timegrid-axis) {
  font-size: 0.8rem;
  color: #6b7280;
}

:deep(.fc-col-header-cell) {
  padding: 0.25rem 0.5rem !important; /* 적당한 패딩 */
  background-color: transparent !important; /* 배경 투명하게 */
  border-bottom: 1px solid #e5e7eb !important;
  border-top: none !important;
  border-left: none !important;
  border-right: none !important;
  min-height: 32px !important;
}

:deep(.fc-col-header-cell-cushion) {
  font-size: 0.8rem !important; /* 폰트 크기 축소 */
  font-weight: 500 !important; /* 폰트 두께 감소 */
  color: #374151;
  padding: 0 !important; /* 내부 패딩 제거 */
  line-height: 1.2 !important; /* 줄 높이 축소 */
}

/* 현재 시간 인디케이터 */
:deep(.fc-timegrid-now-indicator-line) {
  border-color: #ef4444 !important;
  border-width: 2px !important;
}

:deep(.fc-timegrid-now-indicator-arrow) {
  border-color: #ef4444 !important;
}

/* 스크롤바 스타일 */
:deep(.fc-scroller) {
  scrollbar-width: thin;
  scrollbar-color: #d1d5db #f3f4f6;
}

:deep(.fc-scroller::-webkit-scrollbar) {
  width: 8px;
}

:deep(.fc-scroller::-webkit-scrollbar-track) {
  background: #f3f4f6;
}

:deep(.fc-scroller::-webkit-scrollbar-thumb) {
  background: #d1d5db;
  border-radius: 4px;
}

:deep(.fc-scroller::-webkit-scrollbar-thumb:hover) {
  background: #9ca3af;
}

/* 텍스트 줄 제한 */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 