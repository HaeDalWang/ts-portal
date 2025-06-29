<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="$emit('close')">
    <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[80vh] overflow-hidden" @click.stop>
      <!-- 모달 헤더 -->
      <div class="px-6 py-4 border-b border-gray-200 bg-gray-50">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-lg font-semibold text-gray-900">{{ formatSelectedDate(selectedDate) }}</h3>
            <p class="text-sm text-gray-500">{{ events.length }}개의 일정</p>
          </div>
          <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- 모달 내용 -->
      <div class="px-6 py-4 overflow-y-auto max-h-[60vh]">
        <div v-if="events.length === 0" class="text-center py-8">
          <div class="text-gray-400 mb-2">
            <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <p class="text-gray-500">이 날에는 일정이 없습니다.</p>
        </div>

        <div v-else class="space-y-3">
          <div 
            v-for="event in events" 
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
            @click="$emit('close')"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            닫기
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { EventResponse } from '@/services/eventService'

// Props 정의
interface Props {
  show: boolean
  selectedDate: string
  events: EventResponse[]
  getEventTypeIcon: (eventType: string) => string
  getStatusBadgeClass: (status: string) => string
  getStatusText: (status: string) => string
  formatEventTime: (event: EventResponse) => string
  getMemberColor: (memberId: number) => string
}

defineProps<Props>()

// Emits 정의
defineEmits<{
  'close': []
}>()

// 유틸리티 함수들
const formatSelectedDate = (dateStr: string): string => {
  if (!dateStr) return ''
  
  const date = new Date(dateStr)
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const weekday = ['일', '월', '화', '수', '목', '금', '토'][date.getDay()]
  
  return `${year}년 ${month}월 ${day}일 (${weekday})`
}
</script> 