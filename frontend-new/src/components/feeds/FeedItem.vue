<template>
  <div class="feed-item" :class="{ compact }" @click="handleClick">
    <div class="feed-item-header">
      <div class="feed-source">
        <span class="feed-badge" v-if="item.feed_name">{{ item.feed_name }}</span>
        <span class="author" v-if="item.author">{{ item.author }}</span>
      </div>
      <div class="published-date">
        {{ formattedDate }}
      </div>
    </div>
    
    <h3 class="feed-title">{{ item.title }}</h3>
    
    <p class="feed-summary" v-if="!compact">{{ item.summary }}</p>
    
    <div class="feed-footer">
      <span class="read-more">자세히 보기 →</span>
      <div class="feed-actions">
        <button 
          @click.stop="copyLink" 
          class="action-btn"
          title="링크 복사"
        >
          📋
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { FeedItem as FeedItemType } from '@/types/feeds'

// Props 정의
interface Props {
  item: FeedItemType
  compact?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  compact: false
})

// Events 정의
const emit = defineEmits<{
  click: [item: FeedItemType]
}>()

// 날짜 포맷팅
const formattedDate = computed(() => {
  if (!props.item.published) return '날짜 정보 없음'
  
  try {
    const date = new Date(props.item.published)
    const now = new Date()
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60))
    
    if (diffInHours < 1) return '방금 전'
    if (diffInHours < 24) return `${diffInHours}시간 전`
    if (diffInHours < 24 * 7) return `${Math.floor(diffInHours / 24)}일 전`
    
    return date.toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  } catch {
    return '날짜 정보 없음'
  }
})

// 클릭 처리
const handleClick = () => {
  emit('click', props.item)
}

// 링크 복사
const copyLink = async () => {
  if (!props.item.link) return
  
  try {
    await navigator.clipboard.writeText(props.item.link)
    console.log('📋 링크 복사됨:', props.item.link)
    // 향후 토스트 메시지 추가 가능
  } catch (error) {
    console.error('📋 링크 복사 실패:', error)
  }
}
</script>

<style scoped>
.feed-item {
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.2s;
  background: white;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.feed-item:hover {
  border-color: #3182ce;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.feed-item.compact {
  padding: 1rem;
  gap: 0.75rem;
}

.feed-item-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.feed-source {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.feed-badge {
  background: #3182ce;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.author {
  color: #718096;
  font-size: 0.875rem;
}

.published-date {
  color: #a0aec0;
  font-size: 0.875rem;
  white-space: nowrap;
}

.feed-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.feed-item.compact .feed-title {
  font-size: 1rem;
  -webkit-line-clamp: 1;
}

.feed-summary {
  color: #4a5568;
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.feed-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.read-more {
  color: #3182ce;
  font-weight: 500;
  font-size: 0.875rem;
}

.feed-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  background: none;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  padding: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
}

.action-btn:hover {
  border-color: #3182ce;
  background: #f7fafc;
}

/* AWS 블로그별 색상 */
.feed-badge:has-text("AWS Blog") {
  background: #ff9500;
}

.feed-badge:has-text("AWS What's New") {
  background: #34d399;
}

.feed-badge:has-text("AWS Security Blog") {
  background: #ef4444;
}

/* 반응형 */
@media (max-width: 768px) {
  .feed-item {
    padding: 1rem;
  }
  
  .feed-item-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .feed-source {
    width: 100%;
  }
  
  .published-date {
    align-self: flex-end;
  }
}
</style> 