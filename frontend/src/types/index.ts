/**
 * API 타입 정의
 */

// 공통 타입들
export interface BaseEntity {
  id: number
  created_at: string
  updated_at: string
}

// 팀원 관련 타입들
export interface Member extends BaseEntity {
  name: string
  email: string
  phone?: string
  position?: string
  team: string
  skills?: string
  skills_list: string[]
  join_date?: string
  profile_image?: string
  is_active: boolean
  role: string
}

export interface MemberCreate {
  name: string
  email: string
  phone?: string
  position?: string
  team?: string
  skills?: string
  join_date?: string
  profile_image?: string
  is_active?: boolean
}

export interface MemberUpdate {
  name?: string
  email?: string
  phone?: string
  position?: string
  team?: string
  skills?: string
  join_date?: string
  profile_image?: string
  is_active?: boolean
  role?: string
}

export interface MemberListResponse {
  total: number
  members: Member[]
}

export interface MemberStats {
  total_members: number
  active_members: number
  inactive_members: number
  active_rate: number
}

// 고객사 관련 타입들
export interface Customer extends BaseEntity {
  company_name: string
  main_assignee_id?: number | null
  sub_assignee_id?: number | null
  main_assignee?: Member | null
  sub_assignee?: Member | null
  contact_email?: string
  contact_phone?: string
  support_level?: string
  contract_start?: string
  contract_end?: string
  status: string
  notes?: string
  is_active: boolean
  contract_days_remaining?: number
}

export interface CustomerCreate {
  company_name: string
  main_assignee_id?: number | null
  sub_assignee_id?: number | null
  contact_email?: string
  contact_phone?: string
  support_level?: string
  contract_start?: string
  contract_end?: string
  status?: string
  notes?: string
}

export interface CustomerUpdate {
  company_name?: string
  main_assignee_id?: number | null
  sub_assignee_id?: number | null
  contact_email?: string
  contact_phone?: string
  support_level?: string
  contract_start?: string
  contract_end?: string
  status?: string
  notes?: string
}

export interface CustomerListResponse {
  total: number
  customers: Customer[]
}

export interface CustomerStats {
  total_customers: number
  active_customers: number
  inactive_customers: number
  expired_customers: number
  expiring_soon: number
  active_rate: number
}

// 담당 배정 관련 타입들 (향후 사용)
export interface Assignment extends BaseEntity {
  member_id: number
  customer_id: number
  is_primary: boolean
  assigned_date: string
  notes?: string
  member?: Member
  customer?: Customer
}

// 팀 일정 관련 타입들 (향후 사용)
export interface Event extends BaseEntity {
  title: string
  description?: string
  event_type: string
  start_time: string
  end_time?: string
  location?: string
  participants?: string
  is_recurring: boolean
}

// 공지사항 관련 타입들
export interface Notice extends BaseEntity {
  title: string
  content: string
  priority: 'normal' | 'caution' | 'important'
  author_id: number
  author?: Member
  is_pinned: boolean
  is_active: boolean
  views: number
}

export interface NoticeCreate {
  title: string
  content: string
  priority?: 'normal' | 'caution' | 'important'
  author_id: number
  is_pinned?: boolean
}

export interface NoticeUpdate {
  title?: string
  content?: string
  priority?: 'normal' | 'caution' | 'important'
  is_pinned?: boolean
  is_active?: boolean
}

export interface NoticeListResponse {
  total: number
  notices: Notice[]
}

export interface NoticeStats {
  total_notices: number
  pinned_notices: number
  recent_notices: number
  by_priority: {
    normal: number
    caution: number
    important: number
  }
}

export interface NoticeSearchParams {
  q?: string
  priority?: 'normal' | 'caution' | 'important'
  author_id?: number
  is_pinned?: boolean
  active_only?: boolean
}

// API 응답 타입들
export interface ApiError {
  detail: string
  status_code?: number
}

export interface SearchParams {
  q: string
  active_only?: boolean
}

export interface PaginationParams {
  skip?: number
  limit?: number
  active_only?: boolean
} 