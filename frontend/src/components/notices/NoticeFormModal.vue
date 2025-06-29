<template>
  <BaseModal
    :show="show"
    :title="isEdit ? '공지사항 편집' : '새 공지사항 작성'"
    size="large"
    @close="$emit('close')"
  >
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label class="block text-xs font-medium text-gray-700 mb-2">제목</label>
        <input
          v-model="formData.title"
          type="text"
          required
          class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="공지사항 제목을 입력하세요"
        >
      </div>
      
      <div>
        <label class="block text-xs font-medium text-gray-700 mb-2">내용</label>
        <textarea
          v-model="formData.content"
          required
          rows="8"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="공지사항 내용을 입력하세요"
        ></textarea>
      </div>
      
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-xs font-medium text-gray-700 mb-2">중요도</label>
          <select
            v-model="formData.priority"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="normal">📢 일반</option>
            <option value="caution">⚠️ 주의</option>
            <option value="important">🚨 중요</option>
          </select>
        </div>
        
        <div class="flex items-end">
          <label class="flex items-center">
            <input
              v-model="formData.is_pinned"
              type="checkbox"
              class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
            >
            <span class="ml-2 text-xs text-gray-700">📌 상단 고정</span>
          </label>
        </div>
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
          :disabled="!formData.title?.trim() || !formData.content?.trim()"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {{ isEdit ? '수정하기' : '작성하기' }}
        </button>
      </div>
    </template>
  </BaseModal>
</template>

<script setup lang="ts">
import { computed, watch } from 'vue'
import { BaseModal } from '@/components/common'
import type { NoticeCreate, NoticeUpdate } from '@/types'

// Props 정의
interface Props {
  show: boolean
  isEdit: boolean
  formData: NoticeCreate | NoticeUpdate
}

const props = defineProps<Props>()

// Emits 정의
const emit = defineEmits<{
  'close': []
  'submit': [data: NoticeCreate | NoticeUpdate]
  'update:formData': [data: NoticeCreate | NoticeUpdate]
}>()

// 폼 데이터 computed
const formData = computed({
  get: () => props.formData,
  set: (value) => emit('update:formData', value)
})

// 폼 제출 처리
const handleSubmit = () => {
  if (!formData.value.title?.trim() || !formData.value.content?.trim()) {
    return
  }
  emit('submit', formData.value)
}

// 모달이 닫힐 때 폼 초기화
watch(() => props.show, (newShow) => {
  if (!newShow && !props.isEdit) {
    // 새 공지사항 작성 모달이 닫힐 때만 초기화
    emit('update:formData', {
      title: '',
      content: '',
      priority: 'normal',
      author_id: 1,
      is_pinned: false
    })
  }
})
</script> 