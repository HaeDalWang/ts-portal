<template>
  <div class="space-y-4">
    <div 
      v-for="notice in notices" 
      :key="notice.id"
      :class="[
        'bg-white rounded-xl shadow-lg border border-gray-200 p-6 hover:shadow-xl transition-all duration-200 cursor-pointer',
        notice.is_pinned ? 'ring-2 ring-yellow-200 bg-yellow-50' : ''
      ]"
      @click="$emit('notice-click', notice)"
    >
      <div class="flex items-start justify-between mb-4">
        <div class="flex items-start space-x-4 flex-1">
          <!-- 아이콘 -->
          <div :class="['w-10 h-10 rounded-lg flex items-center justify-center text-lg', getPriorityColor(notice.priority)]">
            {{ getPriorityIcon(notice.priority) }}
          </div>
          
          <div class="flex-1 min-w-0">
            <div class="flex items-center space-x-2 mb-2">
              <h3 class="text-sm font-semibold text-gray-900 truncate">{{ notice.title }}</h3>
              <span v-if="notice.is_pinned" class="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs font-semibold rounded-full">
                📌 고정
              </span>
            </div>
            <div class="flex items-center space-x-3 text-xs text-gray-600 mb-3">
              <span>{{ getAuthorName(notice.author_id) }}</span>
              <span>•</span>
              <span>{{ formatDate.relative(notice.created_at) }}</span>
              <span>•</span>
              <span>조회 {{ notice.views }}회</span>
            </div>
            <p class="text-xs text-gray-600 leading-relaxed line-clamp-2">
              {{ formatText.truncate(notice.content, 120) }}
            </p>
          </div>
        </div>
        
        <div class="flex items-center space-x-3 ml-4">
          <!-- 중요도 배지 -->
          <span :class="['px-3 py-1 rounded-full text-xs font-semibold', getPriorityColor(notice.priority)]">
            {{ getPriorityLabel(notice.priority) }}
          </span>
          
          <!-- 액션 버튼들 -->
          <div class="flex items-center space-x-1">
            <button
              @click.stop="$emit('edit-notice', notice)"
              class="text-gray-400 hover:text-blue-600 transition-colors p-1"
              title="편집"
            >
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </button>
            <button
              @click.stop="$emit('delete-notice', notice.id)"
              class="text-gray-400 hover:text-red-600 transition-colors p-1"
              title="삭제"
            >
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { formatDate, formatText } from '@/components/common'
import type { Notice, Member } from '@/types'

// Props 정의
interface Props {
  notices: Notice[]
  members: Member[]
}

const props = defineProps<Props>()

// Emits 정의
defineEmits<{
  'notice-click': [notice: Notice]
  'edit-notice': [notice: Notice]
  'delete-notice': [noticeId: number]
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

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 