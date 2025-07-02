<template>
  <div class="event-card" :class="{ compact, [event.status]: true }">
    <!-- 이벤트 헤더 -->
    <div class="event-header">
      <div class="event-type" :style="{ backgroundColor: event.color || eventTypeColor }">
        <span class="type-icon">{{ event.event_type_icon }}</span>
        <span class="type-label">{{ event.event_type_display }}</span>
      </div>
      
      <div class="event-actions">
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

    <!-- 이벤트 제목 -->
    <h3 class="event-title">{{ event.title }}</h3>

    <!-- 이벤트 시간 -->
    <div class="event-time">
      <span class="time-icon">🕐</span>
      <div class="time-content">
        <div class="start-time">
          {{ formatDateTime(event.start_time) }}
        </div>
        <div v-if="event.end_time" class="end-time">
          ~ {{ formatDateTime(event.end_time) }}
        </div>
        <div v-if="event.duration_minutes > 0" class="duration">
          ({{ formatDuration(event.duration_minutes) }})
        </div>
      </div>
    </div>

    <!-- 이벤트 설명 (compact 모드가 아닐 때만) -->
    <div v-if="!compact && event.description" class="event-description">
      {{ event.description }}
    </div>

    <!-- 이벤트 정보 -->
    <div class="event-info">
      <!-- 장소 -->
      <div v-if="event.location" class="info-item">
        <span class="info-icon">📍</span>
        <span class="info-text">{{ event.location }}</span>
      </div>
      
      <!-- 참가자 -->
      <div v-if="event.participants" class="info-item">
        <span class="info-icon">👥</span>
        <span class="info-text">{{ event.participants }}</span>
      </div>

      <!-- 종일 일정 -->
      <div v-if="event.all_day" class="info-item">
        <span class="info-icon">📅</span>
        <span class="info-text">종일 일정</span>
      </div>

      <!-- 반복 일정 -->
      <div v-if="event.is_recurring" class="info-item">
        <span class="info-icon">🔄</span>
        <span class="info-text">반복 일정</span>
      </div>
    </div>

    <!-- 이벤트 메타 정보 -->
    <div class="event-meta">
      <div class="creator-info">
        <span class="creator-icon">👤</span>
        <span class="creator-name">{{ event.creator?.name || '알 수 없음' }}</span>
      </div>
      
      <div class="date-info">
        <span class="created-date">{{ formatDate(event.created_at) }} 생성</span>
        <span v-if="event.updated_at !== event.created_at" class="updated-date">
          {{ formatDate(event.updated_at) }} 수정
        </span>
      </div>
    </div>

    <!-- 상태 뱃지 -->
    <div class="status-badges">
      <span v-if="event.is_today" class="status-badge today">오늘</span>
      <span v-if="event.is_upcoming" class="status-badge upcoming">예정</span>
      <span v-if="event.is_ongoing" class="status-badge ongoing">진행중</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuth } from '@/composables/useAuth'
import { useCalendar } from '@/composables/useCalendar'
import type { EventResponse } from '@/types/calendar'

// Props 정의
interface Props {
  event: EventResponse
  compact?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  compact: false
})

// Events 정의
const emit = defineEmits<{
  edit: [event: EventResponse]
  delete: [event: EventResponse]
}>()

// Composables
const { user } = useAuth()
const { canEditEvent, canDeleteEvent, formatDate, formatDateTime } = useCalendar()

// 계산된 속성
const eventTypeColor = computed(() => {
  // 이벤트 타입별 색상 반환
  const colors: Record<string, string> = {
    vacation: '#10B981',
    remote: '#3B82F6',
    business_trip: '#F59E0B',
    project: '#8B5CF6',
    education: '#EF4444',
    meeting: '#06B6D4',
    other: '#6B7280'
  }
  return colors[props.event.event_type] || props.event.default_color || '#6B7280'
})

const canEdit = computed(() => {
  return user.value && canEditEvent(props.event)
})

const canDelete = computed(() => {
  return user.value && canDeleteEvent(props.event)
})

// 메서드
const handleEdit = () => {
  emit('edit', props.event)
}

const handleDelete = () => {
  emit('delete', props.event)
}

const formatDuration = (minutes: number): string => {
  if (minutes < 60) {
    return `${minutes}분`
  } else if (minutes < 1440) { // 24시간 미만
    const hours = Math.floor(minutes / 60)
    const remainingMinutes = minutes % 60
    return remainingMinutes > 0 ? `${hours}시간 ${remainingMinutes}분` : `${hours}시간`
  } else {
    const days = Math.floor(minutes / 1440)
    const remainingHours = Math.floor((minutes % 1440) / 60)
    return remainingHours > 0 ? `${days}일 ${remainingHours}시간` : `${days}일`
  }
}
</script>

<style scoped>
.event-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1.5rem;
  transition: all 0.2s;
  cursor: pointer;
  position: relative;
}

.event-card:hover {
  border-color: #cbd5e0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

.event-card.compact {
  padding: 1rem;
}

.event-card.today {
  border-left: 4px solid #3182ce;
}

.event-card.upcoming {
  border-left: 4px solid #f59e0b;
}

.event-card.ongoing {
  border-left: 4px solid #10b981;
}

/* 이벤트 헤더 */
.event-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.event-type {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
}

.event-actions {
  display: flex;
  gap: 0.5rem;
  opacity: 0;
  transition: opacity 0.2s;
}

.event-card:hover .event-actions {
  opacity: 1;
}

.action-btn {
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

.action-btn:hover {
  border-color: #3b82f6;
  background: #f8fafc;
  transform: translateY(-1px);
}

.delete-btn:hover {
  border-color: #ef4444;
  background: #fef2f2;
  color: #ef4444;
}

.edit-btn:hover {
  border-color: #f59e0b;
  background: #fffbeb;
  color: #f59e0b;
}

/* 이벤트 제목 */
.event-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 1rem 0;
  line-height: 1.4;
}

.compact .event-title {
  font-size: 1.125rem;
  margin-bottom: 0.75rem;
}

/* 이벤트 시간 */
.event-time {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.5rem;
}

.time-icon {
  font-size: 1.25rem;
  margin-top: 0.125rem;
}

.time-content {
  flex: 1;
}

.start-time {
  font-weight: 600;
  color: #1f2937;
  font-size: 1rem;
}

.end-time {
  color: #6b7280;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.duration {
  color: #059669;
  font-size: 0.875rem;
  font-weight: 500;
  margin-top: 0.25rem;
}

/* 이벤트 설명 */
.event-description {
  color: #4b5563;
  line-height: 1.6;
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 0.5rem;
  border-left: 4px solid #e5e7eb;
}

/* 이벤트 정보 */
.event-info {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.info-icon {
  font-size: 1rem;
}

.info-text {
  font-weight: 500;
}

/* 메타 정보 */
.event-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #f3f4f6;
  font-size: 0.75rem;
  color: #6b7280;
}

.creator-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.creator-name {
  font-weight: 500;
  color: #374151;
}

.date-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
}

/* 상태 뱃지 */
.status-badges {
  position: absolute;
  top: 1rem;
  right: 1rem;
  display: flex;
  gap: 0.5rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
}

.status-badge.today {
  background: #3182ce;
}

.status-badge.upcoming {
  background: #f59e0b;
}

.status-badge.ongoing {
  background: #10b981;
}

/* 반응형 */
@media (max-width: 768px) {
  .event-card {
    padding: 1rem;
  }

  .event-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .event-actions {
    opacity: 1;
    align-self: flex-end;
  }

  .event-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .date-info {
    align-items: flex-start;
  }

  .event-info {
    flex-direction: column;
    gap: 0.5rem;
  }

  .status-badges {
    position: static;
    margin-top: 1rem;
    justify-content: flex-start;
  }
}
</style> 