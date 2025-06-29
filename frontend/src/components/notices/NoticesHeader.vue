<template>
  <div class="bg-white border-b border-gray-200 px-6 py-3">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-xl font-bold text-gray-900">TS 공지사항</h1>
        <p class="text-sm text-gray-500">팀 공지사항 관리</p>
      </div>
      
      <!-- 컴팩트 통계 및 컨트롤 -->
      <div class="flex items-center space-x-4">
        <!-- 통계 -->
        <div class="flex items-center space-x-3">
          <div class="text-center">
            <div class="text-sm font-semibold text-blue-600">{{ stats?.total_notices || 0 }}</div>
            <div class="text-xs text-gray-500">전체</div>
          </div>
          <div class="text-center">
            <div class="text-sm font-semibold text-yellow-600">{{ stats?.pinned_notices || 0 }}</div>
            <div class="text-xs text-gray-500">고정</div>
          </div>
          <div class="text-center">
            <div class="text-sm font-semibold text-red-600">{{ stats?.by_priority?.important || 0 }}</div>
            <div class="text-xs text-gray-500">중요</div>
          </div>
          <div class="text-center">
            <div class="text-sm font-semibold text-orange-600">{{ stats?.recent_notices || 0 }}</div>
            <div class="text-xs text-gray-500">최근</div>
          </div>
        </div>
        
        <!-- 구분선 -->
        <div class="h-8 w-px bg-gray-300"></div>
        
        <!-- 뷰 모드 전환 -->
        <div class="flex bg-gray-100 rounded-lg p-1">
          <button
            @click="$emit('view-mode-change', 'cards')"
            :class="`px-2 py-1 rounded-md text-xs font-medium transition-colors ${
              viewMode === 'cards' 
                ? 'bg-white text-gray-900 shadow-sm' 
                : 'text-gray-600 hover:text-gray-900'
            }`"
          >
            카드
          </button>
          <button
            @click="$emit('view-mode-change', 'table')"
            :class="`px-2 py-1 rounded-md text-xs font-medium transition-colors ${
              viewMode === 'table' 
                ? 'bg-white text-gray-900 shadow-sm' 
                : 'text-gray-600 hover:text-gray-900'
            }`"
          >
            테이블
          </button>
        </div>
        
        <button 
          @click="$emit('create-notice')"
          class="px-3 py-1.5 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors text-sm"
        >
          + 새 공지사항
        </button>
        
        <button 
          @click="$emit('refresh')"
          :disabled="loading"
          class="px-3 py-1.5 bg-gray-600 text-white rounded-md hover:bg-gray-700 disabled:opacity-50 transition-colors text-sm"
        >
          <LoadingSpinner v-if="loading" size="small" color="white" />
          새로고침
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { LoadingSpinner } from '@/components/common'
import type { NoticeStats } from '@/types'

// Props 정의
interface Props {
  stats: NoticeStats | null
  viewMode: 'cards' | 'table'
  loading: boolean
}

defineProps<Props>()

// Emits 정의
defineEmits<{
  'view-mode-change': [mode: 'cards' | 'table']
  'create-notice': []
  'refresh': []
}>()
</script> 