<template>
  <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">제목</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">중요도</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">작성자</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">작성일</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">조회수</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">상태</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">액션</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr
            v-for="notice in notices"
            :key="notice.id"
            :class="[
              'hover:bg-gray-50 cursor-pointer transition-colors',
              notice.is_pinned ? 'bg-yellow-50' : ''
            ]"
            @click="$emit('notice-click', notice)"
          >
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="text-sm font-medium text-gray-900 truncate max-w-xs">
                  {{ notice.title }}
                </div>
                <span v-if="notice.is_pinned" class="ml-2 text-xs">📌</span>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="['inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold', getPriorityColor(notice.priority)]">
                {{ getPriorityIcon(notice.priority) }} {{ getPriorityLabel(notice.priority) }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ getAuthorName(notice.author_id) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-xs text-gray-500">
              {{ formatDate.datetime(notice.created_at) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-xs text-gray-500">
              {{ notice.views }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="['inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold', notice.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800']">
                {{ notice.is_active ? '활성' : '비활성' }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <div class="flex items-center justify-end space-x-2">
                <button
                  @click.stop="$emit('edit-notice', notice)"
                  class="text-blue-600 hover:text-blue-900 transition-colors"
                  title="편집"
                >
                  편집
                </button>
                <button
                  @click.stop="$emit('delete-notice', notice.id)"
                  class="text-red-600 hover:text-red-900 transition-colors"
                  title="삭제"
                >
                  삭제
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