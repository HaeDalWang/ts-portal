<template>
  <div class="w-32 bg-white border-r border-gray-200 flex flex-col">
    <!-- 필터 및 컨트롤 -->
    <div class="p-2 border-b border-gray-100 flex-shrink-0">
      <div class="space-y-3">
        <!-- 뷰 타입 드롭다운 -->
        <div>
          <label class="block text-xs font-medium text-gray-700 mb-1">보기 방식</label>
          <div class="relative">
            <select 
              :value="currentView" 
              @change="$emit('view-change', ($event.target as HTMLSelectElement).value)"
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
                @change="$emit('toggle-all-members')"
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
                @change="$emit('toggle-member', member.id)"
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
                @change="$emit('toggle-all-parts')"
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
                @change="$emit('toggle-part', part)"
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
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { EVENT_TYPES } from '@/services/eventService'
import type { Member } from '@/types'

// Props 정의
interface Props {
  currentView: string
  members: Member[]
  isAllSelected: boolean
  selectedMembers: Set<number>
  isAllPartsSelected: boolean
  selectedParts: Set<string>
  getMemberColor: (memberId: number) => string
}

const props = defineProps<Props>()

// Emits 정의
defineEmits<{
  'view-change': [view: string]
  'toggle-all-members': []
  'toggle-member': [memberId: number]
  'toggle-all-parts': []
  'toggle-part': [part: string]
}>()

// 계산된 속성
const eventTypes = computed(() => EVENT_TYPES)

const availableParts = computed(() => {
  const parts = new Set<string>()
  props.members.forEach(member => {
    parts.add(member.team || '') // team이 없으면 빈 문자열
  })
  return Array.from(parts).sort()
})

const getPartMemberCount = (part: string) => {
  return props.members.filter(member => (member.team || '') === part).length
}
</script> 