/**
 * AWS Feeds Service
 * Kong Gateway를 통한 feeds-service 연동
 */

import { kongApi } from './api'
import type { 
  FeedsListResponse, 
  AllFeedsResponse, 
  FeedResponse, 
  LatestNewsResponse 
} from '@/types/feeds'

export class FeedsService {
  private readonly baseUrl = '/api/feeds'

  /**
   * 사용 가능한 피드 목록 조회
   */
  async getFeeds(): Promise<FeedsListResponse> {
    console.log('📰 피드 목록 조회 요청')
    const response = await kongApi.get<FeedsListResponse>(`${this.baseUrl}/`)
    console.log('📰 피드 목록 조회 성공:', response.total, '개 피드')
    return response
  }

  /**
   * 모든 피드에서 최신 소식 조회
   */
  async getAllFeeds(limit: number = 5): Promise<AllFeedsResponse> {
    console.log('📰 모든 피드 조회 요청:', { limit })
    const params = new URLSearchParams({ limit: limit.toString() })
    const response = await kongApi.get<AllFeedsResponse>(`${this.baseUrl}/all?${params}`)
    console.log('📰 모든 피드 조회 성공:', response.total, '개 아이템')
    return response
  }

  /**
   * 특정 피드 조회
   */
  async getFeed(feedId: string, limit: number = 10): Promise<FeedResponse> {
    console.log('📰 특정 피드 조회 요청:', { feedId, limit })
    const params = new URLSearchParams({ limit: limit.toString() })
    const response = await kongApi.get<FeedResponse>(`${this.baseUrl}/${feedId}?${params}`)
    console.log('📰 특정 피드 조회 성공:', response.feed_name, response.total, '개 아이템')
    return response
  }

  /**
   * 최신 AWS 소식 조회
   */
  async getLatestNews(limit: number = 3): Promise<LatestNewsResponse> {
    console.log('📰 최신 소식 조회 요청:', { limit })
    const params = new URLSearchParams({ limit: limit.toString() })
    const response = await kongApi.get<LatestNewsResponse>(`${this.baseUrl}/latest?${params}`)
    console.log('📰 최신 소식 조회 성공:', response.total, '개 아이템')
    return response
  }

  /**
   * 날짜 포맷팅 유틸리티
   */
  formatDate(dateString: string): string {
    if (!dateString) return '날짜 정보 없음'
    
    try {
      const date = new Date(dateString)
      const now = new Date()
      const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60))
      
      if (diffInHours < 1) return '방금 전'
      if (diffInHours < 24) return `${diffInHours}시간 전`
      if (diffInHours < 24 * 7) return `${Math.floor(diffInHours / 24)}일 전`
      
      return date.toLocaleDateString('ko-KR')
    } catch (error) {
      return '날짜 정보 없음'
    }
  }
}

// 싱글톤 인스턴스 생성
export const feedsService = new FeedsService()

// 기본 export
export default feedsService 