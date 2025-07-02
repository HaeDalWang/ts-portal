/**
 * AWS 피드 관리 Composable
 * Vue 3 Composition API 기반
 */

import { ref, computed, onMounted } from 'vue'
import { feedsService } from '@/services/feeds'
import type { 
  FeedInfo, 
  FeedItem, 
  FeedState 
} from '@/types/feeds'

// 글로벌 상태 (모든 컴포넌트에서 공유)
const feeds = ref<Record<string, FeedInfo>>({})
const allItems = ref<FeedItem[]>([])
const latestItems = ref<FeedItem[]>([])
const selectedFeedItems = ref<FeedItem[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const lastUpdated = ref<string | null>(null)

export function useFeeds() {
  // 계산된 속성
  const feedsList = computed(() => Object.entries(feeds.value))
  const hasFeeds = computed(() => feedsList.value.length > 0)
  const totalItems = computed(() => allItems.value.length)

  /**
   * 피드 목록 로드
   */
  const loadFeeds = async (): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      const response = await feedsService.getFeeds()
      feeds.value = response.feeds
      console.log('📰 피드 목록 로드 성공:', response.total, '개 피드')
      return true
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '피드 목록을 가져올 수 없습니다.'
      error.value = errorMessage
      console.error('📰 피드 목록 로드 실패:', errorMessage)
      return false
      
    } finally {
      loading.value = false
    }
  }

  /**
   * 모든 피드 아이템 로드
   */
  const loadAllFeeds = async (limit: number = 10): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      const response = await feedsService.getAllFeeds(limit)
      allItems.value = response.items
      lastUpdated.value = response.timestamp
      console.log('📰 모든 피드 로드 성공:', response.total, '개 아이템')
      return true
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '피드를 가져올 수 없습니다.'
      error.value = errorMessage
      console.error('📰 모든 피드 로드 실패:', errorMessage)
      return false
      
    } finally {
      loading.value = false
    }
  }

  /**
   * 특정 피드 로드
   */
  const loadFeed = async (feedId: string, limit: number = 10): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      const response = await feedsService.getFeed(feedId, limit)
      selectedFeedItems.value = response.items
      lastUpdated.value = response.timestamp
      console.log('📰 특정 피드 로드 성공:', response.feed_name, response.total, '개 아이템')
      return true
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '피드를 가져올 수 없습니다.'
      error.value = errorMessage
      console.error('📰 특정 피드 로드 실패:', errorMessage)
      return false
      
    } finally {
      loading.value = false
    }
  }

  /**
   * 최신 소식 로드
   */
  const loadLatestNews = async (limit: number = 5): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      const response = await feedsService.getLatestNews(limit)
      latestItems.value = response.latest_news
      lastUpdated.value = response.timestamp
      console.log('📰 최신 소식 로드 성공:', response.total, '개 아이템')
      return true
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '최신 소식을 가져올 수 없습니다.'
      error.value = errorMessage
      console.error('📰 최신 소식 로드 실패:', errorMessage)
      return false
      
    } finally {
      loading.value = false
    }
  }

  /**
   * 피드 검색
   */
  const searchFeeds = (query: string): FeedItem[] => {
    const searchTerm = query.toLowerCase().trim()
    if (!searchTerm) return allItems.value

    return allItems.value.filter(item => 
      item.title.toLowerCase().includes(searchTerm) ||
      item.summary.toLowerCase().includes(searchTerm) ||
      (item.feed_name && item.feed_name.toLowerCase().includes(searchTerm))
    )
  }

  /**
   * 날짜 포맷팅
   */
  const formatDate = (dateString: string): string => {
    return feedsService.formatDate(dateString)
  }

  /**
   * 에러 초기화
   */
  const clearError = (): void => {
    error.value = null
  }

  /**
   * 새로고침
   */
  const refresh = async (): Promise<void> => {
    console.log('📰 피드 새로고침 시작')
    await Promise.all([
      loadFeeds(),
      loadAllFeeds(),
      loadLatestNews()
    ])
    console.log('📰 피드 새로고침 완료')
  }

  /**
   * 외부 링크 열기
   */
  const openLink = (url: string): void => {
    if (url) {
      window.open(url, '_blank', 'noopener,noreferrer')
    }
  }

  return {
    // 상태
    feeds: computed(() => feeds.value),
    feedsList,
    allItems: computed(() => allItems.value),
    latestItems: computed(() => latestItems.value),
    selectedFeedItems: computed(() => selectedFeedItems.value),
    loading: computed(() => loading.value),
    error: computed(() => error.value),
    lastUpdated: computed(() => lastUpdated.value),
    hasFeeds,
    totalItems,
    
    // 메서드
    loadFeeds,
    loadAllFeeds,
    loadFeed,
    loadLatestNews,
    searchFeeds,
    formatDate,
    clearError,
    refresh,
    openLink
  }
} 