<template>
  <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">고객사</th>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">연락처</th>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">지원 레벨</th>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">계약 기간</th>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">남은 일수</th>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">상태</th>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">액션</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="customer in customers" :key="customer.id" class="hover:bg-gray-50">
            <td class="px-4 py-3 whitespace-nowrap">
              <div class="text-xs font-medium text-gray-900">{{ customer.company_name }}</div>
              <div v-if="customer.contact_email" class="text-xs text-gray-500">{{ customer.contact_email }}</div>
            </td>
            <td class="px-4 py-3 whitespace-nowrap">
              <div v-if="customer.contact_email" class="text-xs text-gray-900">{{ customer.contact_email }}</div>
              <div v-if="customer.contact_phone" class="text-xs text-gray-500">{{ customer.contact_phone }}</div>
            </td>
            <td class="px-4 py-3 whitespace-nowrap">
              <span v-if="customer.support_level" :class="`px-2 py-1 rounded-full text-xs font-medium ${getContractTypeColor(customer.support_level)}`">
                {{ customer.support_level }}
              </span>
              <span v-else class="text-xs text-gray-500">-</span>
            </td>
            <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-900">
              <div>{{ formatDate.basic(customer.contract_start || '') }}</div>
              <div class="text-gray-500">{{ formatDate.basic(customer.contract_end || '') }}</div>
            </td>
            <td class="px-4 py-3 whitespace-nowrap">
              <span v-if="customer.contract_days_remaining !== undefined" :class="`px-2 py-1 rounded-full text-xs font-medium ${getDaysRemainingColor(customer.contract_days_remaining)}`">
                {{ customer.contract_days_remaining > 0 ? `${customer.contract_days_remaining}일` : '만료' }}
              </span>
              <span v-else class="text-xs text-gray-500">-</span>
            </td>
            <td class="px-4 py-3 whitespace-nowrap">
              <span :class="`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(customer.status)}`">
                {{ customer.status }}
              </span>
            </td>
            <td class="px-4 py-3 whitespace-nowrap text-xs font-medium">
              <div class="flex items-center space-x-2">
                <button @click="$emit('customer-detail', customer)" class="text-teal-600 hover:text-teal-900">
                  보기
                </button>
                <button @click="$emit('edit-customer', customer)" class="text-blue-600 hover:text-blue-900">
                  수정
                </button>
                <button @click="$emit('assign-customer', customer)" class="text-purple-600 hover:text-purple-900">
                  할당
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
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