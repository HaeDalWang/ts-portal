<template>
  <div class="aws-feeds-view">
    <!-- 헤더 -->
    <div class="feeds-header">
      <div class="header-content">
        <h1 class="page-title">
          <span class="icon">📰</span>
          AWS 소식
        </h1>
        <p class="page-subtitle">최신 AWS 블로그와 소식을 확인해보세요</p>
      </div>
      
      <!-- 컨트롤 -->
      <div class="feeds-controls">
        <div class="search-box">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="피드 검색..."
            class="search-input"
          />
          <span class="search-icon">🔍</span>
        </div>
        
        <button
          @click="refresh"
          :disabled="loading"
          class="refresh-btn"
          :class="{ loading }"
        >
          <span class="refresh-icon">🔄</span>
          새로고침
        </button>
      </div>
    </div>

    <!-- 에러 메시지 -->
    <div v-if="error" class="error-message">
      <span class="error-icon">❌</span>
      {{ error }}
      <button @click="clearError" class="error-close">×</button>
    </div>

    <!-- 로딩 상태 -->
    <div v-if="loading && !allItems.length" class="loading-state">
      <div class="loading-spinner">⏳</div>
      <p>AWS 소식을 가져오는 중...</p>
    </div>

    <!-- 메인 콘텐츠 -->
    <div v-else class="feeds-content">
      <!-- 탭 네비게이션 -->
      <div class="tabs">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="['tab', { active: activeTab === tab.id }]"
        >
          <span class="tab-icon">{{ tab.icon }}</span>
          {{ tab.label }}
          <span v-if="tab.count" class="tab-count">{{ tab.count }}</span>
        </button>
      </div>

      <!-- 탭 콘텐츠 -->
      <div class="tab-content">
        <!-- 전체 피드 -->
        <div v-if="activeTab === 'all'" class="feed-section">
          <div class="section-header">
            <h2>전체 AWS 소식</h2>
            <p v-if="lastUpdated" class="last-updated">
              마지막 업데이트: {{ formatDate(lastUpdated) }}
            </p>
          </div>
          
          <div class="feed-grid">
            <FeedItem
              v-for="item in displayedItems"
              :key="`${item.feed_id}-${item.title}`"
              :item="item"
              @click="openLink(item.link)"
            />
          </div>
          
          <div v-if="!displayedItems.length && !loading" class="empty-state">
            <span class="empty-icon">📭</span>
            <p>표시할 피드가 없습니다.</p>
          </div>
        </div>

        <!-- 최신 소식 -->
        <div v-if="activeTab === 'latest'" class="feed-section">
          <div class="section-header">
            <h2>오늘의 AWS 소식</h2>
            <p>가장 최근 발행된 AWS 소식입니다</p>
          </div>
          
          <div class="latest-grid">
            <FeedItem
              v-for="item in latestItems"
              :key="`latest-${item.title}`"
              :item="item"
              :compact="false"
              @click="openLink(item.link)"
            />
          </div>
        </div>

        <!-- 피드별 보기 -->
        <div v-if="activeTab === 'feeds'" class="feeds-section">
          <div class="section-header">
            <h2>피드별 보기</h2>
            <p>AWS 서비스별로 분류된 소식을 확인하세요</p>
          </div>
          
          <div class="feeds-list">
            <div
              v-for="[feedId, feedInfo] in feedsList"
              :key="feedId"
              class="feed-card"
              @click="loadFeedDetails(feedId)"
            >
              <div class="feed-card-header">
                <h3>{{ feedInfo.name }}</h3>
                <span class="feed-icon">📡</span>
              </div>
              <p class="feed-description">{{ feedInfo.description }}</p>
              <div class="feed-card-footer">
                <span class="view-link">자세히 보기 →</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useFeeds } from '@/composables/useFeeds'
import FeedItem from '@/components/feeds/FeedItem.vue'

// Composable 사용
const {
  allItems,
  latestItems,
  feedsList,
  loading,
  error,
  lastUpdated,
  loadFeeds,
  loadAllFeeds,
  loadLatestNews,
  searchFeeds,
  formatDate,
  clearError,
  refresh,
  openLink
} = useFeeds()

// 로컬 상태
const searchQuery = ref('')
const activeTab = ref('all')

// 탭 설정
const tabs = computed(() => [
  {
    id: 'all',
    label: '전체',
    icon: '📰',
    count: allItems.value.length
  },
  {
    id: 'latest',
    label: '최신 소식',
    icon: '⚡',
    count: latestItems.value.length
  },
  {
    id: 'feeds',
    label: '피드별',
    icon: '📂',
    count: feedsList.value.length
  }
])

// 검색된 아이템
const displayedItems = computed(() => {
  if (!searchQuery.value.trim()) {
    return allItems.value
  }
  return searchFeeds(searchQuery.value)
})

// 피드 상세 로드
const loadFeedDetails = async (feedId: string) => {
  console.log('📰 피드 상세 로드:', feedId)
  // 향후 피드 상세 페이지로 이동하거나 모달 표시
  alert(`${feedId} 피드 상세 기능은 추후 구현 예정입니다.`)
}

// 컴포넌트 마운트 시 초기 로드
onMounted(async () => {
  console.log('📰 AWS 피드 뷰 마운트됨')
  await Promise.all([
    loadFeeds(),
    loadAllFeeds(15),
    loadLatestNews(8)
  ])
})

// 검색어 변경 시 로그
watch(searchQuery, (newQuery) => {
  if (newQuery) {
    console.log('📰 피드 검색:', newQuery)
  }
})
</script>

<style scoped>
.aws-feeds-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

/* 헤더 */
.feeds-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  gap: 2rem;
}

.header-content {
  flex: 1;
}

.page-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.page-subtitle {
  font-size: 1.1rem;
  color: #718096;
  margin: 0;
}

.feeds-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.search-box {
  position: relative;
}

.search-input {
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 1rem;
  width: 250px;
  outline: none;
  transition: border-color 0.2s;
}

.search-input:focus {
  border-color: #3182ce;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #a0aec0;
}

.refresh-btn {
  padding: 0.75rem 1.5rem;
  background: #3182ce;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
}

.refresh-btn:hover:not(:disabled) {
  background: #2c5aa0;
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.refresh-btn.loading .refresh-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 에러 메시지 */
.error-message {
  background: #fed7d7;
  color: #c53030;
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.error-close {
  margin-left: auto;
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  color: #c53030;
}

/* 로딩 상태 */
.loading-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #718096;
}

.loading-spinner {
  font-size: 2rem;
  margin-bottom: 1rem;
  animation: spin 2s linear infinite;
}

/* 탭 */
.tabs {
  display: flex;
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 2rem;
}

.tab {
  padding: 1rem 1.5rem;
  border: none;
  background: none;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  color: #718096;
}

.tab.active {
  color: #3182ce;
  border-bottom-color: #3182ce;
}

.tab:hover {
  color: #2c5aa0;
}

.tab-count {
  background: #e2e8f0;
  color: #4a5568;
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: bold;
}

.tab.active .tab-count {
  background: #3182ce;
  color: white;
}

/* 섹션 */
.section-header {
  margin-bottom: 1.5rem;
}

.section-header h2 {
  font-size: 1.5rem;
  font-weight: bold;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
}

.section-header p {
  color: #718096;
  margin: 0;
}

.last-updated {
  font-size: 0.875rem;
  color: #a0aec0;
}

/* 피드 그리드 */
.feed-grid,
.latest-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

/* 피드 목록 */
.feeds-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.feed-card {
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.2s;
  background: white;
}

.feed-card:hover {
  border-color: #3182ce;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.feed-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.feed-card-header h3 {
  font-size: 1.25rem;
  font-weight: bold;
  color: #1a202c;
  margin: 0;
}

.feed-icon {
  font-size: 1.5rem;
}

.feed-description {
  color: #718096;
  margin: 0 0 1rem 0;
  line-height: 1.5;
}

.feed-card-footer {
  text-align: right;
}

.view-link {
  color: #3182ce;
  font-weight: 500;
  font-size: 0.875rem;
}

/* 빈 상태 */
.empty-state {
  text-align: center;
  padding: 3rem 2rem;
  color: #718096;
}

.empty-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
}

/* 반응형 */
@media (max-width: 768px) {
  .aws-feeds-view {
    padding: 1rem;
  }
  
  .feeds-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .feeds-controls {
    width: 100%;
    justify-content: stretch;
  }
  
  .search-input {
    width: 100%;
  }
  
  .tabs {
    overflow-x: auto;
  }
  
  .feed-grid,
  .latest-grid {
    grid-template-columns: 1fr;
  }
}
</style> 