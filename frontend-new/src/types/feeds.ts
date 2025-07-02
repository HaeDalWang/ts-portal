/**
 * AWS Feeds Service 타입 정의
 * RSS 피드 기반 AWS 소식 수집 시스템
 */

// 피드 정보
export interface FeedInfo {
  name: string
  url: string
  description: string
}

// 피드 아이템
export interface FeedItem {
  title: string
  link: string
  summary: string
  published: string
  author: string
  feed_id?: string
  feed_name?: string
}

// 피드 목록 응답
export interface FeedsListResponse {
  feeds: Record<string, FeedInfo>
  total: number
}

// 모든 피드 응답
export interface AllFeedsResponse {
  items: FeedItem[]
  total: number
  timestamp: string
}

// 특정 피드 응답
export interface FeedResponse {
  feed_id: string
  feed_name: string
  description: string
  items: FeedItem[]
  total: number
  timestamp: string
}

// 최신 소식 응답
export interface LatestNewsResponse {
  latest_news: FeedItem[]
  total: number
  timestamp: string
}

// 피드 필터 옵션
export interface FeedFilters {
  feed_id?: string
  limit?: number
  search?: string
}

// 피드 상태
export interface FeedState {
  feeds: Record<string, FeedInfo>
  items: FeedItem[]
  loading: boolean
  error: string | null
  lastUpdated: string | null
} 