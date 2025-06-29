<template>
  <div class="flex-1 bg-white">
    <div class="h-full relative">
      <!-- 커스텀 헤더 - 절대 위치로 달력 위에 오버레이 -->
      <div class="absolute top-0 left-0 right-0 z-10 flex items-center justify-between px-4 py-1 bg-white/95 backdrop-blur-sm">
        <!-- 네비게이션 버튼들 -->
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
        
        <!-- 현재 날짜 표시 -->
        <div class="text-lg font-semibold text-gray-900">
          {{ currentTitle }}
        </div>
        
        <div class="w-16"></div> <!-- 균형을 위한 빈 공간 -->
      </div>
      
      <!-- 달력 본체 -->
      <div class="h-full pt-8">
        <FullCalendar
          ref="fullCalendar"
          :options="calendarOptions"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import koLocale from '@fullcalendar/core/locales/ko'
import type { Member } from '@/types'

// Props 정의
interface Props {
  currentView: string
  loadEvents: (info: any) => Promise<any[]>
  members: Member[]
  selectedMembers: Set<number>
  isAllSelected: boolean
  getMemberColor: (memberId: number) => string
}

const props = defineProps<Props>()

// Emits 정의
const $emit = defineEmits<{
  'date-click': [dateStr: string]
}>()

// 반응형 데이터
const fullCalendar = ref()
const currentTitle = ref('')

// FullCalendar 옵션
const calendarOptions = computed(() => ({
  plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
  initialView: 'dayGridMonth',
  locale: koLocale,
  headerToolbar: {
    left: '',
    center: '',
    right: ''
  }, // 기본 헤더 툴바 제거
  height: '100%',
  events: props.loadEvents,
  eventDidMount: (info: any) => {
    // 툴크 추가
    info.el.title = `${info.event.title}\n${info.event.extendedProps.description || ''}`
  },
  datesSet: (dateInfo: any) => {
    // 날짜가 변경될 때마다 타이틀 업데이트
    updateCurrentTitle()
  },
  dateClick: (info: any) => {
    // 날짜 클릭 시 이벤트 발생
    $emit('date-click', info.dateStr)
  },
  dayMaxEvents: false,
  moreLinkClick: 'popover',
  eventDisplay: 'block',
  eventTextColor: '#ffffff',
  slotMinTime: '07:00:00',
  slotMaxTime: '22:00:00',
  allDaySlot: true,
  nowIndicator: true,
  selectMirror: true,
  aspectRatio: 1.0,
  eventMinHeight: 20,
  dayCellContent: (arg: any) => {
    return { html: `<div class="custom-day-number">${arg.dayNumberText}</div>` }
  }
}))

// 뷰 변경 감지
watch(() => props.currentView, (newView) => {
  const calendarApi = fullCalendar.value?.getApi()
  if (calendarApi) {
    calendarApi.changeView(newView)
  }
})

// 메서드들
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

// 달력 이벤트 새로고침 메서드 노출
const refreshEvents = () => {
  const calendarApi = fullCalendar.value?.getApi()
  if (calendarApi) {
    calendarApi.refetchEvents()
  }
}

// 외부에서 접근 가능하도록 expose
defineExpose({
  refreshEvents
})
</script> 