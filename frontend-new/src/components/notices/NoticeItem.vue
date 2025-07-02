<template>
  <div class="notice-item" :class="{ pinned, important: notice.priority === 'important' }">
    <!-- 헤더 -->
    <div class="notice-header">
      <div class="priority-badge" :style="{ backgroundColor: notice.priority_color }">
        <span class="priority-icon">{{ notice.priority_icon }}</span>
        <span class="priority-label">{{ notice.priority_display }}</span>
      </div>
      
      <div class="notice-meta">
        <span class="author" v-if="notice.author">{{ notice.author.name }}</span>
        <span class="date">{{ formatDate(notice.created_at) }}</span>
        <span v-if="pinned" class="pin-indicator">📌</span>
      </div>
    </div>

    <!-- 제목 -->
    <h3 class="notice-title" @click="toggleExpanded">
      {{ notice.title }}
      <span class="expand-icon" :class="{ expanded }">▼</span>
    </h3>

    <!-- 내용 (확장 시) -->
    <div v-if="expanded" class="notice-content">
      <div class="content-text" v-html="formattedContent"></div>
      
      <!-- 메타 정보 -->
      <div class="notice-footer">
        <div class="footer-info">
          <span class="creation-date">작성: {{ formatFullDate(notice.created_at) }}</span>
          <span v-if="notice.updated_at !== notice.created_at" class="update-date">
            수정: {{ formatFullDate(notice.updated_at) }}
          </span>
        </div>
        
        <!-- 액션 버튼들 -->
        <div class="notice-actions">
          <button
            v-if="canEdit"
            @click.stop="handleEdit"
            class="action-btn edit-btn"
            title="수정"
          >
            ✏️
          </button>
          
          <button
            v-if="canDelete"
            @click.stop="handleDelete"
            class="action-btn delete-btn"
            title="삭제"
          >
            🗑️
          </button>
        </div>
      </div>
    </div>

    <!-- 요약 (축소 시) -->
    <div v-else class="notice-summary">
      <p class="summary-text">{{ summary }}</p>
      
      <!-- 간단한 액션 -->
      <div class="summary-actions">
        <button
          v-if="canEdit"
          @click.stop="handleEdit"
          class="quick-action edit"
          title="수정"
        >
          ✏️
        </button>
        
        <button
          v-if="canDelete"
          @click.stop="handleDelete"
          class="quick-action delete"
          title="삭제"
        >
          🗑️
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuth } from '@/composables/useAuth'
import { useNotices } from '@/composables/useNotices'
import type { NoticeResponse } from '@/types/notices'

// Props 정의
interface Props {
  notice: NoticeResponse
  pinned?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  pinned: false
})

// Events 정의
const emit = defineEmits<{
  edit: [notice: NoticeResponse]
  delete: [notice: NoticeResponse]
}>()

// 상태
const expanded = ref(false)

// Composables
const { user } = useAuth()
const { formatDate, canDeleteNotice } = useNotices()

// 계산된 속성
const summary = computed(() => {
  const text = props.notice.content
  return text.length > 150 ? text.substring(0, 150) + '...' : text
})

const formattedContent = computed(() => {
  return props.notice.content.replace(/\n/g, '<br>')
})

const canEdit = computed(() => {
  // 테스트를 위해 임시로 항상 true
  return true
})

const canDelete = computed(() => {
  // 테스트를 위해 임시로 항상 true (백엔드에서 권한 체크)
  return true
})

// 메서드
const toggleExpanded = () => {
  expanded.value = !expanded.value
}

const handleEdit = () => {
  emit('edit', props.notice)
}

const handleDelete = () => {
  emit('delete', props.notice)
}

const formatFullDate = (dateString: string): string => {
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return '날짜 정보 없음'
  }
}
</script>

<style scoped>
.notice-item {
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1.5rem;
  background: white;
  transition: all 0.2s;
  cursor: pointer;
}

.notice-item:hover {
  border-color: #cbd5e0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.notice-item.pinned {
  border-color: #f59e0b;
  background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%);
}

.notice-item.important {
  border-color: #ef4444;
  background: linear-gradient(135deg, #fef2f2 0%, #ffffff 100%);
}

/* 헤더 */
.notice-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.priority-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
}

.notice-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.author {
  font-weight: 500;
  color: #374151;
}

.pin-indicator {
  color: #f59e0b;
  font-size: 1rem;
}

/* 제목 */
.notice-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 1rem 0;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  line-height: 1.4;
}

.notice-title:hover {
  color: #3b82f6;
}

.expand-icon {
  transition: transform 0.2s;
  font-size: 0.875rem;
  color: #6b7280;
}

.expand-icon.expanded {
  transform: rotate(180deg);
}

/* 내용 */
.notice-content {
  margin-top: 1rem;
}

.content-text {
  line-height: 1.6;
  color: #374151;
  margin-bottom: 1.5rem;
  white-space: pre-wrap;
}

.notice-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #f3f4f6;
}

.footer-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 0.75rem;
  color: #6b7280;
}

/* 요약 */
.notice-summary {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.summary-text {
  flex: 1;
  color: #6b7280;
  line-height: 1.5;
  margin: 0;
}

.summary-actions {
  display: flex;
  gap: 0.5rem;
}

/* 액션 버튼 */
.notice-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn, .quick-action {
  padding: 0.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 2rem;
  height: 2rem;
}

.action-btn:hover, .quick-action:hover {
  border-color: #3b82f6;
  background: #f8fafc;
  transform: translateY(-1px);
}

.delete-btn:hover, .quick-action.delete:hover {
  border-color: #ef4444;
  background: #fef2f2;
  color: #ef4444;
}

.edit-btn:hover, .quick-action.edit:hover {
  border-color: #f59e0b;
  background: #fffbeb;
  color: #f59e0b;
}

.quick-action {
  opacity: 0.7;
  transition: opacity 0.2s, all 0.2s;
}

.notice-item:hover .quick-action {
  opacity: 1;
}

/* 반응형 */
@media (max-width: 768px) {
  .notice-item {
    padding: 1rem;
  }

  .notice-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .priority-badge {
    align-self: flex-start;
  }

  .notice-meta {
    gap: 0.75rem;
  }

  .notice-title {
    font-size: 1.125rem;
  }

  .notice-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .notice-actions {
    align-self: flex-end;
  }

  .notice-summary {
    flex-direction: column;
    gap: 1rem;
  }

  .summary-actions {
    align-self: flex-end;
  }
}
</style> 