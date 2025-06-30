/**
 * Member Service 타입 정의
 * 팀원 관리 시스템
 */

import type { UserRole } from './auth'

// 팀원 정보 (백엔드 Member 모델과 일치)
export interface Member {
  id: number
  name: string
  username?: string
  email: string
  phone?: string
  password_hash?: string  // 보안상 프론트엔드에서는 사용하지 않음
  role: UserRole
  last_login?: string
  position?: string
  team: string
  skills?: string
  join_date?: string
  is_active: boolean
  profile_image_url?: string
  created_at: string
  updated_at: string
}

// 팀원 목록 응답 (백엔드 MemberListPaginated와 일치)
export interface MemberListResponse {
  items: Member[]
  total: number
  page: number
  size: number
  pages: number
}

// 팀원 검색 파라미터
export interface MemberSearchParams {
  team?: string
  position?: string
  role?: UserRole
  is_active?: boolean
  search?: string  // 이름, 이메일 등으로 검색
  page?: number
  size?: number
}

// 팀원 생성 요청
export interface CreateMemberRequest {
  name: string
  username?: string
  email: string
  phone?: string
  password?: string  // 생성 시에만 필요
  role: UserRole
  position?: string
  team: string
  skills?: string
  join_date?: string
  profile_image_url?: string
}

// 팀원 수정 요청
export interface UpdateMemberRequest {
  name?: string
  username?: string
  email?: string
  phone?: string
  role?: UserRole
  position?: string
  team?: string
  skills?: string
  join_date?: string
  is_active?: boolean
  profile_image_url?: string
}

// 팀 통계
export interface TeamStats {
  team: string
  total_members: number
  active_members: number
  admin_count: number
  power_user_count: number
  user_count: number
}

// 팀원 상태
export interface MemberState {
  members: Member[]
  currentMember: Member | null
  loading: boolean
  error: string | null
  totalCount: number
  currentPage: number
  pageSize: number
}

// 팀원 필터 옵션
export interface MemberFilterOptions {
  teams: string[]
  positions: string[]
  roles: UserRole[]
} 