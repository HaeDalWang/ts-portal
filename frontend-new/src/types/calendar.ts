/**
 * Calendar Service 타입 정의
 * 일정 관리 시스템
 */

// 이벤트 타입
export enum EventType {
  VACATION = 'vacation',
  REMOTE = 'remote',
  BUSINESS_TRIP = 'business_trip',
  PROJECT = 'project',
  EDUCATION = 'education',
  MEETING = 'meeting',
  OTHER = 'other'
}

// 생성자 정보
export interface CreatorInfo {
  id: number
  name: string
  email: string
  position?: string
  team?: string
}

// 이벤트 기본 타입
export interface EventBase {
  title: string
  description?: string
  event_type: EventType
  start_time: string // ISO 8601 형식
  end_time: string   // 필수로 변경 (데이터베이스에서 not null)
  is_all_day: boolean
  location?: string
  attendees?: string[] | Record<string, any>[] // JSON 형태로 변경
  is_recurring: boolean
  recurrence_rule?: string
  
  // 하위 호환성 필드들
  all_day?: boolean     // is_all_day의 별칭
  participants?: string // 문자열 형태 (하위 호환용)
  color?: string        // 계산된 색상 값
}

// 이벤트 생성 요청
export interface EventCreate extends EventBase {
  // created_by는 헤더에서 자동 추출됨
}

// 이벤트 수정 요청
export interface EventUpdate {
  title?: string
  description?: string
  event_type?: EventType
  start_time?: string
  end_time?: string
  is_all_day?: boolean
  location?: string
  attendees?: string[] | Record<string, any>[]
  is_recurring?: boolean
  recurrence_rule?: string
  
  // 하위 호환성 필드들
  all_day?: boolean
  participants?: string
  color?: string
}

// 이벤트 응답
export interface EventResponse extends EventBase {
  id: number
  created_by: number
  creator?: CreatorInfo
  created_at: string
  updated_at: string
  
  // 계산된 속성들
  event_type_display: string
  event_type_icon: string
  default_color: string
  duration_minutes: number
  is_today: boolean
  is_upcoming: boolean
  is_ongoing: boolean
  status: string
}

// 이벤트 목록 응답
export interface EventListResponse {
  total: number
  events: EventResponse[]
}

// 이벤트 통계
export interface EventStats {
  total_events: number
  today_events: number
  upcoming_events: number
  ongoing_events: number
  completed_events: number
  events_by_type: Record<string, number>
  events_by_member: Record<string, number>
}

// 달력용 이벤트 응답 (FullCalendar 형식)
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
  extendedProps: Record<string, any>
}

// 검색 파라미터
export interface SearchParams {
  q?: string
  event_type?: EventType
  member_id?: number
  start_date?: string // YYYY-MM-DD 형식
  end_date?: string
}

// 페이지네이션 파라미터
export interface PaginationParams {
  skip: number
  limit: number
}

// 이벤트 타입 정보
export interface EventTypeInfo {
  value: string
  label: string
  icon: string
  color: string
  description: string
}

// 일정 상태
export interface CalendarState {
  events: EventResponse[]
  todayEvents: EventResponse[]
  upcomingEvents: EventResponse[]
  calendarEvents: CalendarEventResponse[]
  loading: boolean
  error: string | null
  stats: EventStats | null
  eventTypes: EventTypeInfo[]
  selectedDate: string | null
  currentView: 'month' | 'week' | 'day' | 'list'
}

// 이벤트 폼 데이터
export interface EventFormData {
  title: string
  description: string
  event_type: EventType
  start_date: string
  start_time: string
  end_date: string
  end_time: string
  is_all_day: boolean
  location: string
  attendees: string
  is_recurring: boolean
  recurrence_rule: string
  color: string
  
  // 하위 호환성 필드들
  all_day: boolean
  participants: string
}

// 이벤트 상태 유형
export type EventStatus = 'completed' | 'ongoing' | 'upcoming' | 'today' 