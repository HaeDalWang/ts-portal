<template>
  <BaseModal
    :show="show"
    :title="isEdit ? '고객사 편집' : '새 고객사 등록'"
    size="large"
    @close="$emit('close')"
  >
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">회사명</label>
        <input
          v-model="formData.company_name"
          type="text"
          required
          class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-teal-500 focus:border-transparent"
          placeholder="회사명을 입력하세요"
        >
      </div>
      
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">이메일</label>
          <input
            v-model="formData.contact_email"
            type="email"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-teal-500 focus:border-transparent"
            placeholder="contact@company.com"
          >
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">전화번호</label>
          <input
            v-model="formData.contact_phone"
            type="tel"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-teal-500 focus:border-transparent"
            placeholder="010-1234-5678"
          >
        </div>
      </div>
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">지원 레벨</label>
        <select
          v-model="formData.support_level"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-teal-500 focus:border-transparent"
        >
          <option value="">지원 레벨 선택</option>
          <option value="Basic">Basic</option>
          <option value="Standard">Standard</option>
          <option value="Premium">Premium</option>
          <option value="Enterprise">Enterprise</option>
        </select>
      </div>
      
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">계약 시작일</label>
          <input
            v-model="formData.contract_start"
            type="date"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-teal-500 focus:border-transparent"
          >
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">계약 종료일</label>
          <input
            v-model="formData.contract_end"
            type="date"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-teal-500 focus:border-transparent"
          >
        </div>
      </div>
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">상태</label>
        <select
          v-model="formData.status"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-teal-500 focus:border-transparent"
        >
          <option value="Active">활성</option>
          <option value="Inactive">비활성</option>
          <option value="Expired">만료</option>
        </select>
      </div>
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">메모</label>
        <textarea
          v-model="formData.notes"
          rows="4"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-teal-500 focus:border-transparent"
          placeholder="추가 메모사항을 입력하세요"
        ></textarea>
      </div>
    </form>

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
          @click="handleSubmit"
          :disabled="!formData.company_name?.trim() || loading"
          class="px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <LoadingSpinner v-if="loading" size="small" color="white" class="mr-2" />
          {{ isEdit ? '수정하기' : '등록하기' }}
        </button>
      </div>
    </template>
  </BaseModal>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { BaseModal, LoadingSpinner } from '@/components/common'
import type { CustomerCreate, CustomerUpdate } from '@/types'

// Props 정의
interface Props {
  show: boolean
  isEdit: boolean
  formData: CustomerCreate | CustomerUpdate
  loading: boolean
}

const props = defineProps<Props>()

// Emits 정의
const emit = defineEmits<{
  'close': []
  'submit': [data: CustomerCreate | CustomerUpdate]
  'update:formData': [data: CustomerCreate | CustomerUpdate]
}>()

// 폼 데이터 computed
const formData = computed({
  get: () => props.formData,
  set: (value) => emit('update:formData', value)
})

// 폼 제출 처리
const handleSubmit = () => {
  if (!formData.value.company_name?.trim()) {
    return
  }
  emit('submit', formData.value)
}
</script> 