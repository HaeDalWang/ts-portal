<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <div
      v-for="customer in customers"
      :key="customer.id"
      class="bg-white rounded-xl shadow-lg border border-gray-200 p-4 hover:shadow-xl transition-shadow"
    >
      <div class="flex items-start justify-between mb-3">
        <div class="flex-1">
          <h3 class="text-sm font-semibold text-gray-900 mb-1">{{ customer.company_name }}</h3>
          <p v-if="customer.contact_email" class="text-xs text-gray-600">{{ customer.contact_email }}</p>
        </div>
        <div class="flex flex-col items-end space-y-1">
          <span :class="`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(customer.status)}`">
            {{ customer.status }}
          </span>
          <span v-if="customer.support_level" :class="`px-2 py-1 rounded-full text-xs font-medium ${getContractTypeColor(customer.support_level)}`">
            {{ customer.support_level }}
          </span>
        </div>
      </div>

      <div class="space-y-1 mb-3">
        <div v-if="customer.contact_email" class="flex items-center text-xs text-gray-600">
          <svg class="w-3 h-3 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
          </svg>
          {{ customer.contact_email }}
        </div>
        <div v-if="customer.contact_phone" class="flex items-center text-xs text-gray-600">
          <svg class="w-3 h-3 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
          </svg>
          {{ customer.contact_phone }}
        </div>
        <div class="flex items-center text-xs text-gray-600">
          <svg class="w-3 h-3 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          {{ formatDate.basic(customer.contract_start || '') }} ~ {{ formatDate.basic(customer.contract_end || '') }}
        </div>
      </div>

      <div v-if="customer.contract_days_remaining !== undefined" class="mb-3">
        <span :class="`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getDaysRemainingColor(customer.contract_days_remaining)}`">
          <svg class="w-3 h-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {{ customer.contract_days_remaining > 0 ? `${customer.contract_days_remaining}일 남음` : '만료됨' }}
        </span>
      </div>

      <div v-if="customer.notes" class="text-xs text-gray-600 bg-gray-50 rounded-lg p-2 mb-3">
        {{ customer.notes }}
      </div>

      <!-- 카드 액션 버튼들 -->
      <div class="flex items-center justify-between space-x-2">
        <div :class="`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${customer.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`">
          <div :class="`w-2 h-2 rounded-full mr-1 ${customer.is_active ? 'bg-green-400' : 'bg-gray-400'}`"></div>
          {{ customer.is_active ? '활성' : '비활성' }}
        </div>
        <div class="flex items-center space-x-1">
          <button 
            @click="$emit('customer-detail', customer)" 
            class="text-teal-600 hover:text-teal-800 text-xs font-medium px-2 py-1 rounded hover:bg-teal-50"
          >
            보기
          </button>
          <button 
            @click="$emit('edit-customer', customer)" 
            class="text-blue-600 hover:text-blue-800 text-xs font-medium px-2 py-1 rounded hover:bg-blue-50"
          >
            수정
          </button>
          <button 
            @click="$emit('assign-customer', customer)" 
            class="text-purple-600 hover:text-purple-800 text-xs font-medium px-2 py-1 rounded hover:bg-purple-50"
          >
            할당
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { formatDate } from '@/components/common'
import type { Customer } from '@/types'

// Props 정의
interface Props {
  customers: Customer[]
}

defineProps<Props>()

// Emits 정의
defineEmits<{
  'customer-detail': [customer: Customer]
  'edit-customer': [customer: Customer]
  'assign-customer': [customer: Customer]
}>()

// 유틸리티 함수들
const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    'Active': 'bg-green-100 text-green-800',
    'Inactive': 'bg-gray-100 text-gray-800',
    'Expired': 'bg-red-100 text-red-800'
  }
  return colors[status] || 'bg-gray-100 text-gray-800'
}

const getContractTypeColor = (type?: string) => {
  if (!type) return 'bg-gray-100 text-gray-800'
  
  const colors: Record<string, string> = {
    'Full MSP': 'bg-purple-100 text-purple-800',
    'Consulting': 'bg-blue-100 text-blue-800',
    'Support': 'bg-yellow-100 text-yellow-800',
    'Monitoring': 'bg-green-100 text-green-800'
  }
  
  return colors[type] || 'bg-gray-100 text-gray-800'
}

const getDaysRemainingColor = (days?: number) => {
  if (!days || days < 0) return 'bg-red-100 text-red-800'
  if (days <= 30) return 'bg-orange-100 text-orange-800'
  if (days <= 90) return 'bg-yellow-100 text-yellow-800'
  return 'bg-green-100 text-green-800'
}
</script> 