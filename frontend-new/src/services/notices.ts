/**
 * Notice Service
 * Kong Gateway를 통한 notice-service 연동
 */

import { kongApi } from './api'
import type { 
  NoticeCreate,
  NoticeUpdate,
  NoticeResponse,
  NoticeListResponse,
  NoticeStats,
  SearchParams,
  PaginationParams,
  PriorityInfo
} from '@/types/notices'

export class NoticesService {
  private readonly baseUrl = '/api/notices'

  /**
   * 공지사항 목록 조회
   */
  async getNotices(skip: number = 0, limit: number = 20): Promise<NoticeListResponse> {
    console.log('📋 공지사항 목록 조회 요청:', { skip, limit })
    const params = new URLSearchParams({ 
      skip: skip.toString(), 
      limit: limit.toString() 
    })
    const response = await kongApi.get<NoticeListResponse>(`${this.baseUrl}/?${params}`)
    console.log('📋 공지사항 목록 조회 성공:', response.total, '개 공지사항')
    return response
  }

  /**
   * 공지사항 검색
   */
  async searchNotices(
    searchParams: SearchParams, 
    pagination: PaginationParams
  ): Promise<NoticeListResponse> {
    console.log('📋 공지사항 검색 요청:', { searchParams, pagination })
    
    const params = new URLSearchParams({
      skip: pagination.skip.toString(),
      limit: pagination.limit.toString()
    })
    
    // 검색 파라미터 추가
    if (searchParams.q) params.append('q', searchParams.q)
    if (searchParams.priority) params.append('priority', searchParams.priority)
    if (searchParams.author_id) params.append('author_id', searchParams.author_id.toString())
    if (searchParams.is_pinned !== undefined) params.append('is_pinned', searchParams.is_pinned.toString())
    if (searchParams.active_only !== undefined) params.append('active_only', searchParams.active_only.toString())
    
    const response = await kongApi.get<NoticeListResponse>(`${this.baseUrl}/search?${params}`)
    console.log('📋 공지사항 검색 성공:', response.total, '개 결과')
    return response
  }

  /**
   * 고정 공지사항 조회
   */
  async getPinnedNotices(): Promise<NoticeResponse[]> {
    console.log('📌 고정 공지사항 조회 요청')
    const response = await kongApi.get<NoticeResponse[]>(`${this.baseUrl}/pinned`)
    console.log('📌 고정 공지사항 조회 성공:', response.length, '개')
    return response
  }

  /**
   * 최근 공지사항 조회
   */
  async getRecentNotices(days: number = 7, limit: number = 5): Promise<NoticeResponse[]> {
    console.log('📅 최근 공지사항 조회 요청:', { days, limit })
    const params = new URLSearchParams({ 
      days: days.toString(), 
      limit: limit.toString() 
    })
    const response = await kongApi.get<NoticeResponse[]>(`${this.baseUrl}/recent?${params}`)
    console.log('📅 최근 공지사항 조회 성공:', response.length, '개')
    return response
  }

  /**
   * 공지사항 통계 조회
   */
  async getNoticeStats(): Promise<NoticeStats> {
    console.log('📊 공지사항 통계 조회 요청')
    const response = await kongApi.get<NoticeStats>(`${this.baseUrl}/stats`)
    console.log('📊 공지사항 통계 조회 성공')
    return response
  }

  /**
   * 작성자별 공지사항 조회
   */
  async getNoticesByAuthor(
    authorId: number, 
    skip: number = 0, 
    limit: number = 20
  ): Promise<NoticeListResponse> {
    console.log('👤 작성자별 공지사항 조회 요청:', { authorId, skip, limit })
    const params = new URLSearchParams({ 
      skip: skip.toString(), 
      limit: limit.toString() 
    })
    const response = await kongApi.get<NoticeListResponse>(`${this.baseUrl}/author/${authorId}?${params}`)
    console.log('👤 작성자별 공지사항 조회 성공:', response.total, '개')
    return response
  }

  /**
   * 특정 공지사항 조회
   */
  async getNotice(noticeId: number): Promise<NoticeResponse> {
    console.log('📋 공지사항 조회 요청:', noticeId)
    const response = await kongApi.get<NoticeResponse>(`${this.baseUrl}/${noticeId}`)
    console.log('📋 공지사항 조회 성공:', response.title)
    return response
  }

  /**
   * 공지사항 생성
   */
  async createNotice(noticeData: NoticeCreate): Promise<NoticeResponse> {
    console.log('📝 공지사항 생성 요청:', noticeData.title)
    const response = await kongApi.post<NoticeResponse>(`${this.baseUrl}/`, noticeData)
    console.log('📝 공지사항 생성 성공:', response.id)
    return response
  }

  /**
   * 공지사항 수정
   */
  async updateNotice(noticeId: number, noticeData: NoticeUpdate): Promise<NoticeResponse> {
    console.log('✏️ 공지사항 수정 요청:', noticeId)
    const response = await kongApi.put<NoticeResponse>(`${this.baseUrl}/${noticeId}`, noticeData)
    console.log('✏️ 공지사항 수정 성공:', response.id)
    return response
  }

  /**
   * 공지사항 삭제
   */
  async deleteNotice(noticeId: number): Promise<{ message: string }> {
    console.log('🗑️ 공지사항 삭제 요청:', noticeId)
    const response = await kongApi.delete<{ message: string }>(`${this.baseUrl}/${noticeId}`)
    console.log('🗑️ 공지사항 삭제 성공:', noticeId)
    return response
  }

  /**
   * 우선순위 목록 조회
   */
  async getPriorities(): Promise<PriorityInfo[]> {
    console.log('📊 우선순위 목록 조회 요청')
    const response = await kongApi.get<PriorityInfo[]>(`${this.baseUrl}/priorities/list`)
    console.log('📊 우선순위 목록 조회 성공:', response.length, '개')
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
      
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    } catch (error) {
      return '날짜 정보 없음'
    }
  }

  /**
   * 우선순위 색상 가져오기
   */
  getPriorityColor(priority: string): string {
    const colors = {
      normal: '#6B7280',
      caution: '#F59E0B',
      important: '#EF4444'
    }
    return colors[priority as keyof typeof colors] || '#6B7280'
  }

  /**
   * 우선순위 아이콘 가져오기
   */
  getPriorityIcon(priority: string): string {
    const icons = {
      normal: '📢',
      caution: '⚠️',
      important: '🚨'
    }
    return icons[priority as keyof typeof icons] || '📢'
  }
}

// 싱글톤 인스턴스 생성
export const noticesService = new NoticesService()

// 기본 export
export default noticesService 