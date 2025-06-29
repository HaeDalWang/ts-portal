<template>
  <div class="flex items-center space-x-4">
    <!-- 전체 이벤트 -->
    <div class="text-center">
      <div class="text-lg font-bold text-blue-600">{{ stats.total_events }}</div>
      <div class="text-xs text-gray-500">전체</div>
    </div>
    
    <div class="h-8 w-px bg-gray-300"></div>
    
    <!-- 오늘 이벤트 -->
    <div class="text-center">
      <div class="text-lg font-bold text-green-600">{{ stats.today_events }}</div>
      <div class="text-xs text-gray-500">오늘</div>
    </div>
    
    <div class="h-8 w-px bg-gray-300"></div>
    
    <!-- 예정 이벤트 -->
    <div class="text-center">
      <div class="text-lg font-bold text-orange-600">{{ stats.upcoming_events }}</div>
      <div class="text-xs text-gray-500">예정</div>
    </div>
    
    <div class="h-8 w-px bg-gray-300"></div>
    
    <!-- 진행중 이벤트 -->
    <div class="text-center">
      <div class="text-lg font-bold text-yellow-600">{{ stats.ongoing_events }}</div>
      <div class="text-xs text-gray-500">진행중</div>
    </div>
    
    <div class="h-8 w-px bg-gray-300"></div>
    
    <!-- 완료 이벤트 -->
    <div class="text-center">
      <div class="text-lg font-bold text-purple-600">{{ stats.completed_events }}</div>
      <div class="text-xs text-gray-500">완료</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { EventStats } from '@/services/eventService'

// Props 정의
interface Props {
  stats: EventStats
}

defineProps<Props>()
</script> 