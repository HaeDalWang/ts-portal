/**
 * 이벤트 관련 API 서비스
 */

import { api } from './api'

// 이벤트 타입 정의
export interface EventBase {
  title: string
  description?: string
  event_type: string
  start_time: string
  end_time?: string
  all_day: boolean
  location?: string
  participants?: string
  is_recurring: boolean
  recurrence_rule?: string
  color?: string
  created_by: number
}

export interface EventCreate extends EventBase {}

export interface EventUpdate {
  title?: string
  description?: string
  event_type?: string
  start_time?: string
  end_time?: string
  all_day?: boolean
  location?: string
  participants?: string
  is_recurring?: boolean
  recurrence_rule?: string
  color?: string
}

export interface EventResponse extends EventBase {
  id: number
  created_at: string
  updated_at: string
  event_type_display: string
  event_type_icon: string
  default_color: string
  duration_minutes: number
  is_today: boolean
  is_upcoming: boolean
  is_ongoing: boolean
  status: string
  creator?: any
}

export interface CalendarEventResponse {
  id: string
  title: string
  start: string
  end?: string
  allDay: boolean
  color?: string
  backgroundColor?: string
  borderColor?: string
  textColor?: string
  extendedProps: {
    event_type: string
    event_type_display: string
    description?: string
    location?: string
    participants?: string
    creator_name?: string
    creator_id: number
    duration_minutes: number
    status: string
  }
}

export interface EventStats {
  total_events: number
  today_events: number
  upcoming_events: number
  ongoing_events: number
  completed_events: number
  events_by_type: Record<string, number>
  events_by_member: Record<string, number>
}

export interface EventListResponse {
  total: number
  events: EventResponse[]
}

// 이벤트 타입 옵션
export const EVENT_TYPES = [
  { value: 'vacation', label: '휴가', icon: '🌴', color: '#10B981' },
  { value: 'remote', label: '재택근무', icon: '🏠', color: '#3B82F6' },
  { value: 'business_trip', label: '출장', icon: '✈️', color: '#F59E0B' },
  { value: 'project', label: '프로젝트', icon: '💼', color: '#8B5CF6' },
  { value: 'education', label: '교육/세미나', icon: '📚', color: '#06B6D4' },
  { value: 'meeting', label: '회의', icon: '🤝', color: '#EF4444' },
  { value: 'other', label: '기타', icon: '📝', color: '#6B7280' }
]

// 이벤트 서비스 클래스
export class EventService {
  /**
   * 이벤트 목록 조회
   */
  static async getEvents(params?: {
    skip?: number
    limit?: number
    member_id?: number
    event_type?: string
    start_date?: string
    end_date?: string
  }): Promise<EventListResponse> {
    return await api.get<EventListResponse>('/events/', params)
  }

  /**
   * 달력용 이벤트 조회 (FullCalendar 형식)
   */
  static async getCalendarEvents(
    start: string,
    end: string,
    member_id?: number
  ): Promise<CalendarEventResponse[]> {
    const params: any = { start, end }
    if (member_id) params.member_id = member_id

    return await api.get<CalendarEventResponse[]>('/events/calendar', params)
  }

  /**
   * 오늘 일정 조회
   */
  static async getTodayEvents(): Promise<EventResponse[]> {
    return await api.get<EventResponse[]>('/events/today')
  }

  /**
   * 다가오는 일정 조회
   */
  static async getUpcomingEvents(days: number = 7): Promise<EventResponse[]> {
    return await api.get<EventResponse[]>('/events/upcoming', { days })
  }

  /**
   * 이벤트 검색
   */
  static async searchEvents(query: string): Promise<EventResponse[]> {
    return await api.get<EventResponse[]>('/events/search', { q: query })
  }

  /**
   * 이벤트 통계 조회
   */
  static async getEventStats(): Promise<EventStats> {
    return await api.get<EventStats>('/events/stats/summary')
  }

  /**
   * 이벤트 타입 목록 조회
   */
  static async getEventTypes(): Promise<Array<{ value: string; label: string }>> {
    return await api.get<Array<{ value: string; label: string }>>('/events/types')
  }

  /**
   * 특정 이벤트 조회
   */
  static async getEvent(id: number): Promise<EventResponse> {
    return await api.get<EventResponse>(`/events/${id}`)
  }

  /**
   * 이벤트 생성
   */
  static async createEvent(data: EventCreate): Promise<EventResponse> {
    return await api.post<EventResponse>('/events/', data)
  }

  /**
   * 이벤트 수정
   */
  static async updateEvent(id: number, data: EventUpdate): Promise<EventResponse> {
    return await api.put<EventResponse>(`/events/${id}`, data)
  }

  /**
   * 이벤트 삭제
   */
  static async deleteEvent(id: number): Promise<void> {
    await api.delete(`/events/${id}`)
  }

  /**
   * 특정 팀원의 이벤트 조회
   */
  static async getMemberEvents(
    memberId: number,
    params?: {
      start_date?: string
      end_date?: string
      event_type?: string
    }
  ): Promise<EventResponse[]> {
    return await api.get<EventResponse[]>(`/events/member/${memberId}/events`, params)
  }

  /**
   * 타입별 이벤트 조회
   */
  static async getEventsByType(
    eventType: string,
    params?: {
      start_date?: string
      end_date?: string
    }
  ): Promise<EventResponse[]> {
    return await api.get<EventResponse[]>(`/events/type/${eventType}/events`, params)
  }

  // 유틸리티 메서드들

  /**
   * 이벤트 타입 정보 조회
   */
  static getEventTypeInfo(eventType: string) {
    return EVENT_TYPES.find(type => type.value === eventType) || EVENT_TYPES[EVENT_TYPES.length - 1]
  }

  /**
   * 날짜 포맷팅 (ISO 형식으로 변환)
   */
  static formatDateForAPI(date: Date): string {
    return date.toISOString()
  }

  /**
   * 날짜 파싱 (API 응답을 Date 객체로 변환)
   */
  static parseAPIDate(dateString: string): Date {
    return new Date(dateString)
  }

  /**
   * 이벤트 지속 시간 계산 (분 단위)
   */
  static calculateDuration(startTime: string, endTime?: string): number {
    if (!endTime) return 0
    
    const start = new Date(startTime)
    const end = new Date(endTime)
    return Math.floor((end.getTime() - start.getTime()) / (1000 * 60))
  }

  /**
   * 이벤트 상태 확인
   */
  static getEventStatus(startTime: string, endTime?: string): 'upcoming' | 'ongoing' | 'completed' {
    const now = new Date()
    const start = new Date(startTime)
    const end = endTime ? new Date(endTime) : null

    if (start > now) {
      return 'upcoming'
    } else if (end && end > now) {
      return 'ongoing'
    } else {
      return 'completed'
    }
  }
}

export default EventService 