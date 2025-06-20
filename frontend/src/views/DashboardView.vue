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
      <!-- 좌측 사이드바 - 더욱 좁게 -->
      <div class="w-52 bg-white border-r border-gray-200 flex flex-col">
        <!-- 필터 및 컨트롤 -->
        <div class="p-3 border-b border-gray-100 flex-shrink-0">
          <div class="space-y-4">
            <!-- 팀원 선택 -->
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">팀원</label>
              <div class="space-y-1 max-h-96 overflow-y-auto">
                <label class="flex items-center space-x-2 text-xs">
                  <input
                    type="checkbox"
                    :checked="isAllSelected"
                    @change="toggleAllMembers"
                    class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span class="font-medium text-gray-600">전체 선택</span>
                </label>
                <hr class="my-1">
                <label 
                  v-for="member in members" 
                  :key="member.id" 
                  class="flex items-center space-x-2 text-xs cursor-pointer hover:bg-gray-50 p-1 rounded"
                >
                  <input
                    type="checkbox"
                    :checked="isAllSelected || selectedMembers.has(member.id)"
                    @change="toggleMember(member.id)"
                    class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <div 
                    class="w-3 h-3 rounded-full"
                    :style="{ backgroundColor: getMemberColor(member.id) }"
                  ></div>
                  <span class="text-gray-700">{{ member.name }}</span>
                </label>
              </div>
            </div>
            
            <!-- 뷰 타입 -->
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">보기 방식</label>
              <div class="flex rounded border border-gray-300">
                <button
                  @click="changeCalendarView('dayGridMonth')"
                  :class="[
                    'flex-1 px-2 py-1 text-xs font-medium',
                    currentView === 'dayGridMonth' 
                      ? 'bg-blue-500 text-white' 
                      : 'bg-white text-gray-700 hover:bg-gray-50'
                  ]"
                >
                  월
                </button>
                <button
                  @click="changeCalendarView('timeGridWeek')"
                  :class="[
                    'flex-1 px-2 py-1 text-xs font-medium border-l border-r border-gray-300',
                    currentView === 'timeGridWeek' 
                      ? 'bg-blue-500 text-white' 
                      : 'bg-white text-gray-700 hover:bg-gray-50'
                  ]"
                >
                  주
                </button>
                <button
                  @click="changeCalendarView('timeGridDay')"
                  :class="[
                    'flex-1 px-2 py-1 text-xs font-medium',
                    currentView === 'timeGridDay' 
                      ? 'bg-blue-500 text-white' 
                      : 'bg-white text-gray-700 hover:bg-gray-50'
                  ]"
                >
                  일
                </button>
              </div>
            </div>
          </div>
        </div>



        <!-- 오늘 일정 - 컴팩트 -->
        <div class="flex-1 overflow-y-auto min-h-0">
          <div class="p-3">
            <h3 class="text-sm font-semibold text-gray-900 mb-2">오늘 일정</h3>
            <div v-if="todayEvents.length === 0" class="text-xs text-gray-500 text-center py-4">
              일정 없음
            </div>
            <div v-else class="space-y-2">
              <div
                v-for="event in todayEvents"
                :key="event.id"
                class="flex items-start space-x-2 p-2 rounded border border-gray-100 hover:bg-gray-50"
              >
                <span class="text-sm">{{ event.event_type_icon }}</span>
                <div class="flex-1 min-w-0">
                  <p class="text-xs font-medium text-gray-900 truncate">{{ event.title }}</p>
                  <p class="text-xs text-gray-500">{{ formatTime(event.start_time) }}</p>
                  <p v-if="event.location" class="text-xs text-gray-400 truncate">📍 {{ event.location }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 범례 - 일정 유형만 -->
        <div class="border-t border-gray-100 p-3 flex-shrink-0">
          <!-- 일정 유형 -->
          <div>
            <h4 class="text-xs font-semibold text-gray-700 mb-2">일정 유형</h4>
            <div class="grid grid-cols-2 gap-1">
              <div v-for="type in eventTypes.slice(0, 6)" :key="type.value" class="flex items-center space-x-1">
                <span class="text-xs">{{ type.icon }}</span>
                <span class="text-xs text-gray-600 truncate">{{ type.label }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 메인 달력 영역 - 화면의 대부분을 차지 -->
      <div class="flex-1 bg-white">
        <div class="h-full p-6">
          <FullCalendar
            ref="fullCalendar"
            :options="calendarOptions"
          />
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

// 계산된 속성
const eventTypes = computed(() => EVENT_TYPES)

// 팀원 ID 기반 동적 색상 생성 (HSL 사용)
const generateMemberColor = (memberId: number): string => {
  // 팀원 ID를 시드로 사용하여 일관된 색상 생성
  const hue = (memberId * 137.508) % 360 // 황금각을 사용한 균등 분포
  const saturation = 45 + (memberId % 15) // 45-60% 채도로 부드러운 색상
  const lightness = 60 + (memberId % 15)  // 60-75% 명도로 옅은 색상
  
  return `hsl(${hue}, ${saturation}%, ${lightness}%)`
}

// FullCalendar 옵션 - 훨씬 크게 설정
const calendarOptions = ref({
  plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
  initialView: 'dayGridMonth',
  locale: koLocale,
  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: ''
  },
  height: 'calc(100vh - 80px)', // 헤더가 작아진 만큼 더 큰 높이
  events: loadEvents,
  eventDidMount: (info: any) => {
    // 툴크 추가
    info.el.title = `${info.event.title}\n${info.event.extendedProps.description || ''}`
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
  // 달력 셀 높이 증가
  aspectRatio: 1.2,
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

async function loadEvents(info: any): Promise<CalendarEventResponse[]> {
  try {
    const start = info.start.toISOString().split('T')[0]
    const end = info.end.toISOString().split('T')[0]
    
    // 전체 선택이거나 아무도 선택되지 않았으면 전체 표시
    if (isAllSelected.value || selectedMembers.value.size === 0) {
      return await EventService.getCalendarEvents(start, end)
    } else {
      // 선택된 팀원들의 이벤트를 병렬로 로드
      const eventPromises = Array.from(selectedMembers.value).map(memberId =>
        EventService.getCalendarEvents(start, end, memberId)
      )
      const eventsArrays = await Promise.all(eventPromises)
      // 모든 이벤트를 하나의 배열로 합치기
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
    
  } catch (error) {
    console.error('대시보드 데이터 로딩 실패:', error)
  } finally {
    loading.value = false
  }
}

// 컴포넌트 마운트 시 데이터 로딩
onMounted(() => {
  loadDashboardData()
})
</script>

<style scoped>
/* FullCalendar 대형 스타일 최적화 */
:deep(.fc) {
  font-family: 'Segoe UI', system-ui, sans-serif;
}

:deep(.fc-header-toolbar) {
  margin-bottom: 0.75rem !important; /* 하단 여백 축소 */
  padding: 0.5rem 1rem !important; /* 상하 패딩 축소 */
  min-height: 40px !important; /* 툴바 높이 제한 */
}

:deep(.fc-toolbar-title) {
  font-size: 1.1rem !important; /* 제목 폰트 크기 대폭 축소 */
  font-weight: 600 !important;
  color: #1f2937;
}

:deep(.fc-button) {
  padding: 0.25rem 0.5rem !important; /* 버튼 패딩 축소 */
  font-size: 0.75rem !important; /* 버튼 폰트 크기 축소 */
  border-radius: 4px !important;
  font-weight: 500 !important;
  min-height: 28px !important; /* 버튼 높이 제한 */
}

:deep(.fc-button-primary) {
  background-color: #3B82F6 !important;
  border-color: #3B82F6 !important;
}

:deep(.fc-button-primary:hover) {
  background-color: #2563EB !important;
  border-color: #2563EB !important;
}

:deep(.fc-today-button) {
  background-color: #10B981 !important;
  border-color: #10B981 !important;
}

/* 달력 셀 스타일 - 아웃룩 스타일로 확대 */
:deep(.fc-daygrid-day) {
  border: 1px solid #e5e7eb;
  min-height: 120px !important; /* 셀 높이 대폭 증가 */
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
}

:deep(.custom-day-number) {
  font-size: 0.75rem !important;
  font-weight: 400 !important;
  color: #6b7280 !important;
}

/* 달력 전체 높이 증가 */
:deep(.fc-daygrid-body) {
  min-height: 600px;
}

:deep(.fc-daygrid-day-frame) {
  min-height: 120px !important;
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
  padding: 0.25rem 0.5rem !important; /* 상하 패딩 더욱 축소 */
  background-color: #f9fafb;
  border-bottom: 1px solid #e5e7eb !important; /* 보더 두께도 축소 */
  min-height: 32px !important; /* 최소 높이 더욱 축소 */
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
</style> 