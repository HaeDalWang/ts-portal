<template>
  <BaseModal
    :show="show"
    :title="customer?.company_name || ''"
    size="large"
    @close="$emit('close')"
  >
    <div v-if="customer" class="space-y-6">
      <!-- 기본 정보 -->
      <div class="flex items-center space-x-6">
        <div class="w-20 h-20 bg-gradient-to-br from-teal-400 to-teal-600 rounded-full flex items-center justify-center text-white font-bold text-2xl">
          {{ customer.company_name.charAt(0) }}
        </div>
        <div class="flex-1">
          <h3 class="text-2xl font-bold text-gray-900 mb-1">{{ customer.company_name }}</h3>
          <div class="flex items-center space-x-3 mb-2">
            <span v-if="customer.support_level" :class="`px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800`">
              {{ customer.support_level }}
            </span>
            <span :class="`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${customer.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`">
              {{ customer.status }}
            </span>
          </div>
        </div>
      </div>

      <!-- 연락처 정보 -->
      <div class="bg-gray-50 rounded-lg p-4">
        <h4 class="font-semibold text-gray-900 mb-3">연락처 정보</h4>
        <div class="space-y-2">
          <div v-if="customer.contact_email" class="flex items-center text-sm">
            <span class="text-gray-600">이메일:</span>
            <span class="ml-2 font-medium">{{ customer.contact_email }}</span>
          </div>
          <div v-if="customer.contact_phone" class="flex items-center text-sm">
            <span class="text-gray-600">전화번호:</span>
            <span class="ml-2 font-medium">{{ customer.contact_phone }}</span>
          </div>
        </div>
      </div>

      <!-- 계약 정보 -->
      <div class="bg-gray-50 rounded-lg p-4">
        <h4 class="font-semibold text-gray-900 mb-3">계약 정보</h4>
        <div class="space-y-2">
          <div class="flex items-center text-sm">
            <span class="text-gray-600">계약 시작:</span>
            <span class="ml-2 font-medium">{{ formatDate.basic(customer.contract_start || '') }}</span>
          </div>
          <div class="flex items-center text-sm">
            <span class="text-gray-600">계약 종료:</span>
            <span class="ml-2 font-medium">{{ formatDate.basic(customer.contract_end || '') }}</span>
          </div>
          <div v-if="customer.contract_days_remaining !== undefined" class="flex items-center text-sm">
            <span class="text-gray-600">남은 일수:</span>
            <span class="ml-2 font-medium">{{ customer.contract_days_remaining > 0 ? `${customer.contract_days_remaining}일` : '만료됨' }}</span>
          </div>
        </div>
      </div>

      <!-- 메모 -->
      <div v-if="customer.notes">
        <h4 class="font-semibold text-gray-900 mb-3">메모</h4>
        <div class="bg-gray-50 rounded-lg p-4">
          <p class="text-sm text-gray-700">{{ customer.notes }}</p>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-end">
        <button
          @click="$emit('close')"
          class="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
        >
          닫기
        </button>
      </div>
    </template>
  </BaseModal>
</template>

<script setup lang="ts">
import { BaseModal, formatDate } from '@/components/common'
import type { Customer } from '@/types'

// Props 정의
interface Props {
  show: boolean
  customer: Customer | null
}

defineProps<Props>()

// Emits 정의
defineEmits<{
  'close': []
}>()
</script> 