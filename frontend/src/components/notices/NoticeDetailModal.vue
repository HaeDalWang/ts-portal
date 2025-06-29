<template>
  <BaseModal
    :show="show"
    :title="notice?.title || ''"
    size="large"
    @close="$emit('close')"
  >
    <template #header>
      <div class="flex items-start justify-between">
        <div class="flex items-center space-x-4">
          <div :class="['w-12 h-12 rounded-lg flex items-center justify-center text-xl', getPriorityColor(notice?.priority || 'normal')]">
            {{ getPriorityIcon(notice?.priority || 'normal') }}
          </div>
          <div>
            <h2 class="text-xl font-bold text-gray-900 mb-2">{{ notice?.title }}</h2>
            <div class="flex items-center space-x-3">
              <span :class="['px-3 py-1 rounded-full text-xs font-semibold', getPriorityColor(notice?.priority || 'normal')]">
                {{ getPriorityLabel(notice?.priority || 'normal') }}
              </span>
              <span v-if="notice?.is_pinned" class="px-3 py-1 bg-yellow-100 text-yellow-800 text-xs font-semibold rounded-full">
                📌 고정 공지
              </span>
            </div>
          </div>
        </div>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </template>

    <div v-if="notice">
      <div class="flex items-center space-x-4 text-xs text-gray-600 mb-6 pb-6 border-b border-gray-200">
        <span class="font-medium">{{ getAuthorName(notice.author_id) }}</span>
        <span>•</span>
        <span>{{ formatDate.datetime(notice.created_at) }}</span>
        <span>•</span>
        <span>조회 {{ notice.views }}회</span>
      </div>
      
      <div class="prose max-w-none">
        <div class="whitespace-pre-wrap text-gray-700 leading-relaxed text-sm">{{ notice.content }}</div>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-end space-x-3">
        <button
          @click="$emit('edit', notice)"
          class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
        >
          편집
        </button>
        <button
          @click="$emit('delete', notice?.id)"
          class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
        >
          삭제
        </button>
        <button
          @click="$emit('close')"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          닫기
        </button>
      </div>
    </template>
  </BaseModal>
</template>

<script setup lang="ts">
import { BaseModal, formatDate } from '@/components/common'
import type { Notice, Member } from '@/types'

// Props 정의
interface Props {
  show: boolean
  notice: Notice | null
  members: Member[]
}

const props = defineProps<Props>()

// Emits 정의
defineEmits<{
  'close': []
  'edit': [notice: Notice | null]
  'delete': [noticeId: number | undefined]
}>()

// 유틸리티 함수들
const getPriorityColor = (priority: Notice['priority']) => {
  const colors: Record<string, string> = {
    'important': 'bg-red-100 text-red-800',
    'caution': 'bg-yellow-100 text-yellow-800',
    'normal': 'bg-blue-100 text-blue-800'
  }
  return colors[priority] || 'bg-gray-100 text-gray-800'
}

const getPriorityIcon = (priority: Notice['priority']) => {
  const icons: Record<string, string> = {
    'important': '🚨',
    'caution': '⚠️',
    'normal': '📢'
  }
  return icons[priority] || '📢'
}

const getPriorityLabel = (priority: Notice['priority']) => {
  const labels: Record<string, string> = {
    'important': '중요',
    'caution': '주의',
    'normal': '일반'
  }
  return labels[priority] || '일반'
}

const getAuthorName = (authorId: number) => {
  const author = props.members.find(m => m.id === authorId)
  return author?.name || '알 수 없음'
}
</script> 