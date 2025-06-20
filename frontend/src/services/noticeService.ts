/**
 * 공지사항 관련 API 서비스
 */

import { api } from './api'
import type {
  Notice,
  NoticeCreate,
  NoticeUpdate,
  NoticeListResponse,
  NoticeStats,
  NoticeSearchParams,
  PaginationParams
} from '../types'

export const noticeService = {
  // 공지사항 목록 조회
  async getNotices(params: PaginationParams = {}): Promise<NoticeListResponse> {
    const queryParams = {
      skip: params.skip || 0,
      limit: params.limit || 20
    }
    return api.get<NoticeListResponse>('/notices/', queryParams)
  },

  // 공지사항 단일 조회
  async getNotice(id: number): Promise<Notice> {
    return api.get<Notice>(`/notices/${id}`)
  },

  // 공지사항 검색
  async searchNotices(
    searchParams: NoticeSearchParams, 
    pagination: PaginationParams = {}
  ): Promise<NoticeListResponse> {
    const queryParams = {
      ...searchParams,
      skip: pagination.skip || 0,
      limit: pagination.limit || 20
    }
    return api.get<NoticeListResponse>('/notices/search', queryParams)
  },

  // 고정 공지사항 조회
  async getPinnedNotices(): Promise<Notice[]> {
    return api.get<Notice[]>('/notices/pinned')
  },

  // 최근 공지사항 조회
  async getRecentNotices(days: number = 7, limit: number = 5): Promise<Notice[]> {
    const queryParams = { days, limit }
    return api.get<Notice[]>('/notices/recent', queryParams)
  },

  // 작성자별 공지사항 조회
  async getNoticesByAuthor(
    authorId: number, 
    pagination: PaginationParams = {}
  ): Promise<NoticeListResponse> {
    const queryParams = {
      skip: pagination.skip || 0,
      limit: pagination.limit || 20
    }
    return api.get<NoticeListResponse>(`/notices/author/${authorId}`, queryParams)
  },

  // 공지사항 생성
  async createNotice(noticeData: NoticeCreate): Promise<Notice> {
    return api.post<Notice>('/notices/', noticeData)
  },

  // 공지사항 수정
  async updateNotice(id: number, noticeData: NoticeUpdate): Promise<Notice> {
    return api.put<Notice>(`/notices/${id}`, noticeData)
  },

  // 공지사항 삭제 (소프트 삭제)
  async deleteNotice(id: number): Promise<void> {
    return api.delete(`/notices/${id}`)
  },

  // 공지사항 통계
  async getNoticeStats(): Promise<NoticeStats> {
    return api.get<NoticeStats>('/notices/stats/summary')
  },

  // 중요도 목록 조회
  async getPriorityList(): Promise<Array<{
    value: string
    label: string
    icon: string
    color: string
  }>> {
    return api.get('/notices/priorities/list')
  },

  // 간편 함수들
  async getImportantNotices(): Promise<Notice[]> {
    const response = await this.searchNotices({ 
      priority: 'important', 
      active_only: true 
    })
    return response.notices
  },

  async searchNoticesByTitle(title: string): Promise<Notice[]> {
    const response = await this.searchNotices({ 
      q: title, 
      active_only: true 
    })
    return response.notices
  }
}

export default noticeService 