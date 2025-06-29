<template>
  <div class="bg-white border-b border-gray-200 px-6 py-3">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-xl font-bold text-gray-900">MSP 관리</h1>
        <p class="text-sm text-gray-500">고객사 계약 관리</p>
      </div>
      
      <!-- 컴팩트 통계 -->
      <div class="flex items-center space-x-6">
        <div class="text-center">
          <div class="text-lg font-semibold text-blue-600">{{ stats?.total_customers || 0 }}</div>
          <div class="text-xs text-gray-500">전체</div>
        </div>
        <div class="text-center">
          <div class="text-lg font-semibold text-green-600">{{ stats?.active_customers || 0 }}</div>
          <div class="text-xs text-gray-500">활성</div>
        </div>
        <div class="text-center">
          <div class="text-lg font-semibold text-red-600">{{ stats?.expired_customers || 0 }}</div>
          <div class="text-xs text-gray-500">만료</div>
        </div>
        <div class="text-center">
          <div class="text-lg font-semibold text-yellow-600">{{ stats?.expiring_soon || 0 }}</div>
          <div class="text-xs text-gray-500">만료예정</div>
        </div>
        
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
        
        <!-- 액션 버튼들 -->
        <div class="flex items-center space-x-2">
          <button 
            @click="$emit('create-customer')"
            class="px-3 py-1.5 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors text-sm font-medium flex items-center space-x-1"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            <span>새 고객사</span>
          </button>
          
          <button 
            @click="$emit('refresh')"
            :disabled="loading"
            class="px-3 py-1.5 bg-teal-600 text-white rounded-md hover:bg-teal-700 disabled:opacity-50 transition-colors text-sm"
          >
            <LoadingSpinner v-if="loading" size="small" color="white" />
            새로고침
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { LoadingSpinner } from '@/components/common'
import type { CustomerStats } from '@/types'

// Props 정의
interface Props {
  stats: CustomerStats | null
  viewMode: 'cards' | 'table'
  loading: boolean
}

defineProps<Props>()

// Emits 정의
defineEmits<{
  'view-mode-change': [mode: 'cards' | 'table']
  'create-customer': []
  'refresh': []
}>()
</script> 