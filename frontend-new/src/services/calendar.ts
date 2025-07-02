/**
 * Calendar Service API 클래스
 * Kong Gateway를 통한 calendar-service 연동
 */

import { kongApi } from './api'
import type {
  EventCreate,
  EventUpdate,
  EventResponse,
  EventListResponse,
  EventStats,
  CalendarEventResponse,
  SearchParams,
  PaginationParams,
  EventTypeInfo
} from '@/types/calendar'

/**
 * 달력 이벤트 서비스
 */
export class CalendarService {
  private readonly baseUrl = '/api/events'

  /**
   * 이벤트 생성
   */
  async createEvent(eventData: EventCreate): Promise<EventResponse> {
    try {
      console.log('📅 이벤트 생성 요청:', eventData)
      
      // 하위 호환성을 위한 필드 변환
      const requestData = {
        ...eventData,
        is_all_day: eventData.is_all_day ?? eventData.all_day ?? false,
        attendees: eventData.attendees || (eventData.participants ? [eventData.participants] : undefined)
      }
      
      const response = await kongApi.post<EventResponse>(this.baseUrl, requestData)
      console.log('📅 이벤트 생성 성공:', response.id)
      return response
    } catch (error) {
      console.error('📅 이벤트 생성 실패:', error)
      throw error
    }
  }

  /**
   * 이벤트 목록 조회
   */
  async getEvents(
    skip: number = 0,
    limit: number = 100,
    searchParams?: SearchParams
  ): Promise<EventListResponse> {
    try {
      const params = new URLSearchParams()
      params.append('skip', skip.toString())
      params.append('limit', limit.toString())
      
      if (searchParams) {
        if (searchParams.q) params.append('q', searchParams.q)
        if (searchParams.event_type) params.append('event_type', searchParams.event_type)
        if (searchParams.member_id) params.append('member_id', searchParams.member_id.toString())
        if (searchParams.start_date) params.append('start_date', searchParams.start_date)
        if (searchParams.end_date) params.append('end_date', searchParams.end_date)
      }

      console.log('📅 이벤트 목록 조회 요청:', { skip, limit, searchParams })
      const response = await kongApi.get<EventListResponse>(`${this.baseUrl}?${params.toString()}`)
      console.log('📅 이벤트 목록 조회 성공:', response.total, '개')
      return response
    } catch (error) {
      console.error('📅 이벤트 목록 조회 실패:', error)
      throw error
    }
  }

  /**
   * 달력용 이벤트 조회 (FullCalendar 형식)
   */
  async getCalendarEvents(
    startDate: string,
    endDate: string,
    memberId?: number
  ): Promise<CalendarEventResponse[]> {
    try {
      const params = new URLSearchParams()
      params.append('start', startDate)
      params.append('end', endDate)
      if (memberId) params.append('member_id', memberId.toString())

      console.log('📅 달력용 이벤트 조회 요청:', { startDate, endDate, memberId })
      const response = await kongApi.get<CalendarEventResponse[]>(`${this.baseUrl}/calendar?${params.toString()}`)
      console.log('📅 달력용 이벤트 조회 성공:', response.length, '개')
      return response
    } catch (error) {
      console.error('📅 달력용 이벤트 조회 실패:', error)
      throw error
    }
  }

  /**
   * 오늘 일정 조회
   */
  async getTodayEvents(): Promise<EventResponse[]> {
    try {
      console.log('📅 오늘 일정 조회 요청')
      const response = await kongApi.get<EventResponse[]>(`${this.baseUrl}/today`)
      console.log('📅 오늘 일정 조회 성공:', response.length, '개')
      return response
    } catch (error) {
      console.error('📅 오늘 일정 조회 실패:', error)
      throw error
    }
  }

  /**
   * 다가오는 일정 조회
   */
  async getUpcomingEvents(days: number = 7): Promise<EventResponse[]> {
    try {
      const params = new URLSearchParams()
      params.append('days', days.toString())

      console.log('📅 다가오는 일정 조회 요청:', days, '일')
      const response = await kongApi.get<EventResponse[]>(`${this.baseUrl}/upcoming?${params.toString()}`)
      console.log('📅 다가오는 일정 조회 성공:', response.length, '개')
      return response
    } catch (error) {
      console.error('📅 다가오는 일정 조회 실패:', error)
      throw error
    }
  }

  /**
   * 이벤트 검색
   */
  async searchEvents(
    searchParams: SearchParams,
    pagination: PaginationParams
  ): Promise<EventListResponse> {
    try {
      return await this.getEvents(pagination.skip, pagination.limit, searchParams)
    } catch (error) {
      console.error('📅 이벤트 검색 실패:', error)
      throw error
    }
  }

  /**
   * 간단한 텍스트 검색
   */
  async simpleSearch(query: string): Promise<EventResponse[]> {
    try {
      const params = new URLSearchParams()
      params.append('q', query)

      console.log('📅 이벤트 간단 검색 요청:', query)
      const response = await kongApi.get<EventResponse[]>(`${this.baseUrl}/search?${params.toString()}`)
      console.log('📅 이벤트 간단 검색 성공:', response.length, '개')
      return response
    } catch (error) {
      console.error('📅 이벤트 간단 검색 실패:', error)
      throw error
    }
  }

  /**
   * 이벤트 통계 조회
   */
  async getEventStats(): Promise<EventStats> {
    try {
      console.log('📅 이벤트 통계 조회 요청')
      const response = await kongApi.get<EventStats>(`${this.baseUrl}/stats`)
      console.log('📅 이벤트 통계 조회 성공')
      return response
    } catch (error) {
      console.error('📅 이벤트 통계 조회 실패:', error)
      throw error
    }
  }

  /**
   * 이벤트 타입 목록 조회
   */
  async getEventTypes(): Promise<EventTypeInfo[]> {
    try {
      console.log('📅 이벤트 타입 목록 조회 요청')
      const response = await kongApi.get<Array<{ value: string; label: string }>>(`${this.baseUrl}/types`)
      
      // 아이콘과 색상 추가
      const eventTypesWithIcons: EventTypeInfo[] = response.map(type => ({
        ...type,
        icon: this.getEventTypeIcon(type.value),
        color: this.getEventTypeColor(type.value),
        description: this.getEventTypeDescription(type.value)
      }))
      
      console.log('📅 이벤트 타입 목록 조회 성공:', eventTypesWithIcons.length, '개')
      return eventTypesWithIcons
    } catch (error) {
      console.error('📅 이벤트 타입 목록 조회 실패:', error)
      throw error
    }
  }

  /**
   * 단일 이벤트 조회
   */
  async getEvent(eventId: number): Promise<EventResponse> {
    try {
      console.log('📅 이벤트 조회 요청:', eventId)
      const response = await kongApi.get<EventResponse>(`${this.baseUrl}/${eventId}`)
      console.log('📅 이벤트 조회 성공:', response.id)
      return response
    } catch (error) {
      console.error('📅 이벤트 조회 실패:', error)
      throw error
    }
  }

  /**
   * 이벤트 수정
   */
  async updateEvent(eventId: number, eventData: EventUpdate): Promise<EventResponse> {
    try {
      console.log('📅 이벤트 수정 요청:', eventId, eventData)
      
      // 하위 호환성을 위한 필드 변환
      const requestData = {
        ...eventData,
        is_all_day: eventData.is_all_day ?? eventData.all_day,
        attendees: eventData.attendees || (eventData.participants ? [eventData.participants] : undefined)
      }
      
      const response = await kongApi.put<EventResponse>(`${this.baseUrl}/${eventId}`, requestData)
      console.log('📅 이벤트 수정 성공:', response.id)
      return response
    } catch (error) {
      console.error('📅 이벤트 수정 실패:', error)
      throw error
    }
  }

  /**
   * 이벤트 삭제
   */
  async deleteEvent(eventId: number): Promise<void> {
    try {
      console.log('📅 이벤트 삭제 요청:', eventId)
      await kongApi.delete(`${this.baseUrl}/${eventId}`)
      console.log('📅 이벤트 삭제 성공:', eventId)
    } catch (error) {
      console.error('📅 이벤트 삭제 실패:', error)
      throw error
    }
  }

  /**
   * 날짜 포맷팅 헬퍼
   */
  formatDate(dateString: string): string {
    try {
      const date = new Date(dateString)
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    } catch {
      return '날짜 오류'
    }
  }

  /**
   * 시간 포맷팅 헬퍼
   */
  formatTime(dateString: string): string {
    try {
      const date = new Date(dateString)
      return date.toLocaleTimeString('ko-KR', {
        hour: '2-digit',
        minute: '2-digit'
      })
    } catch {
      return '시간 오류'
    }
  }

  /**
   * 날짜+시간 포맷팅 헬퍼
   */
  formatDateTime(dateString: string): string {
    try {
      const date = new Date(dateString)
      return date.toLocaleString('ko-KR', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    } catch {
      return '날짜 시간 오류'
    }
  }

  /**
   * 이벤트 타입별 아이콘 반환
   */
  private getEventTypeIcon(eventType: string): string {
    const icons: Record<string, string> = {
      vacation: '🏖️',
      remote: '🏠',
      business_trip: '✈️',
      project: '📊',
      education: '📚',
      meeting: '🤝',
      other: '📅'
    }
    return icons[eventType] || '📅'
  }

  /**
   * 이벤트 타입별 색상 반환
   */
  private getEventTypeColor(eventType: string): string {
    const colors: Record<string, string> = {
      vacation: '#10B981',     // 초록색 (휴가)
      remote: '#3B82F6',       // 파란색 (재택근무)
      business_trip: '#F59E0B', // 주황색 (출장)
      project: '#8B5CF6',      // 보라색 (프로젝트)
      education: '#EF4444',    // 빨간색 (교육)
      meeting: '#06B6D4',      // 청록색 (회의)
      other: '#6B7280'         // 회색 (기타)
    }
    return colors[eventType] || '#6B7280'
  }

  /**
   * 이벤트 타입별 설명 반환
   */
  private getEventTypeDescription(eventType: string): string {
    const descriptions: Record<string, string> = {
      vacation: '휴가 및 연차',
      remote: '재택근무',
      business_trip: '출장 및 외부 업무',
      project: '프로젝트 관련 일정',
      education: '교육, 세미나, 컨퍼런스',
      meeting: '회의 및 미팅',
      other: '기타 일정'
    }
    return descriptions[eventType] || '기타 일정'
  }
}

// 싱글톤 인스턴스 내보내기
export const calendarService = new CalendarService() 