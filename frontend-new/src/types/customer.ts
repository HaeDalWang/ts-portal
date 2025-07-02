/**
 * Customer 관련 타입 정의
 */

// 고객사 상태 enum (백엔드와 동일)
export type CustomerStatus = 'Active' | 'Pending' | 'Expired' | 'Suspended'

// 담당자 역할 (백엔드와 동일)
export type AssignmentRole = 'Primary' | 'Secondary' | 'Backup'

// 고객사 기본 정보 (백엔드 스키마와 일치)
export interface Customer {
  id: number
  company_name: string
  contact_person?: string
  contact_email?: string
  contact_phone?: string
  contract_type?: string
  contract_start?: string
  contract_end?: string
  status: string
  notes?: string
  is_active: boolean
  contract_days_remaining?: number
  created_at: string
  updated_at: string
  assignments?: Assignment[]
}

// 고객사 생성 요청 (백엔드 스키마와 일치)
export interface CustomerCreate {
  company_name: string
  contact_person?: string
  contact_email?: string
  contact_phone?: string
  contract_type?: string
  contract_start?: string
  contract_end?: string
  status?: CustomerStatus
  notes?: string
}

// 고객사 수정 요청 (백엔드 스키마와 일치)
export interface CustomerUpdate {
  company_name?: string
  contact_person?: string
  contact_email?: string
  contact_phone?: string
  contract_type?: string
  contract_start?: string
  contract_end?: string
  status?: CustomerStatus
  notes?: string
}

// 담당자 배정 정보 (백엔드 스키마와 일치)
export interface Assignment {
  id: number
  member_id: number
  customer_id: number
  role: AssignmentRole
  assigned_date: string
  end_date?: string
  is_primary: boolean
  is_active: boolean
  responsibilities?: string
  duration_days: number
  created_at: string
  updated_at: string
  member?: MemberInfo
  customer?: Customer
}

// 담당자 배정 생성 요청
export interface AssignmentCreate {
  member_id: number
  customer_id: number
  role?: AssignmentRole
  is_primary?: boolean
  responsibilities?: string
  end_date?: string
}

// 담당자 배정 수정 요청
export interface AssignmentUpdate {
  role?: AssignmentRole
  is_primary?: boolean
  responsibilities?: string
  end_date?: string
  is_active?: boolean
}

// API 응답 타입들 (백엔드 스키마와 일치)
export interface CustomerResponse extends Customer {}

export interface CustomerListResponse {
  total: number
  customers: Customer[]
}

export interface AssignmentResponse extends Assignment {}

export interface AssignmentListResponse {
  assignments: Assignment[]
  total: number
  skip: number
  limit: number
}

// 팀원 정보 (다른 서비스에서 가져온 정보)
export interface MemberInfo {
  id: number
  name: string
  email: string
  position?: string
  team?: string
}

// 검색 및 필터 파라미터
export interface CustomerSearchParams {
  q?: string
  status?: CustomerStatus
  active_only?: boolean
  contract_type?: string
  skip?: number
  limit?: number
}

export interface AssignmentSearchParams {
  member_id?: number
  customer_id?: number
  active_only?: boolean
  skip?: number
  limit?: number
}

// 통계 정보 (백엔드 스키마와 일치)
export interface CustomerStats {
  total_customers: number
  active_customers: number
  inactive_customers: number
  expired_customers: number
  expiring_soon: number
  active_rate: number
}

export interface AssignmentStats {
  total_assignments: number
  active_assignments: number
  primary_assignments: number
  secondary_assignments: number
  backup_assignments: number
  assignments_by_member: Record<string, number>
} 