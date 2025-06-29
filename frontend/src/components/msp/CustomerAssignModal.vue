<template>
  <BaseModal
    :show="show"
    :title="`담당자 할당 - ${customer?.company_name || ''}`"
    size="medium"
    @close="$emit('close')"
  >
    <div v-if="customer" class="space-y-4">
      <div class="bg-gray-50 rounded-lg p-4">
        <h4 class="font-semibold text-gray-900 mb-2">{{ customer.company_name }}</h4>
        <p class="text-sm text-gray-600">이 고객사의 담당자를 선택해주세요.</p>
      </div>
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">담당자 선택</label>
        <select
          :value="selectedAssigneeId"
          @change="$emit('update:selectedAssigneeId', parseInt(($event.target as HTMLSelectElement).value))"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          required
        >
          <option value="">담당자를 선택하세요</option>
          <option v-for="member in members" :key="member.id" :value="member.id">
            {{ member.name }} ({{ member.email }})
          </option>
        </select>
      </div>
      
      <div v-if="selectedAssigneeId" class="bg-blue-50 rounded-lg p-4">
        <div class="flex items-center">
          <div class="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold">
            {{ getSelectedMember()?.name.charAt(0) }}
          </div>
          <div class="ml-3">
            <p class="font-medium text-gray-900">{{ getSelectedMember()?.name }}</p>
            <p class="text-sm text-gray-600">{{ getSelectedMember()?.email }}</p>
            <p class="text-sm text-gray-600">{{ getSelectedMember()?.team }}</p>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-end space-x-3">
        <button
          type="button"
          @click="$emit('close')"
          class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
        >
          취소
        </button>
        <button
          @click="$emit('assign')"
          :disabled="!selectedAssigneeId || loading"
          class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <LoadingSpinner v-if="loading" size="small" color="white" class="mr-2" />
          할당하기
        </button>
      </div>
    </template>
  </BaseModal>
</template>

<script setup lang="ts">
import { BaseModal, LoadingSpinner } from '@/components/common'
import type { Customer, Member } from '@/types'

// Props 정의
interface Props {
  show: boolean
  customer: Customer | null
  members: Member[]
  selectedAssigneeId: number | null
  loading: boolean
}

const props = defineProps<Props>()

// Emits 정의
defineEmits<{
  'close': []
  'assign': []
  'update:selectedAssigneeId': [id: number]
}>()

// 선택된 멤버 정보 가져오기
const getSelectedMember = () => {
  return props.members.find(m => m.id === props.selectedAssigneeId)
}
</script> 