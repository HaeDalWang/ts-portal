/**
 * 권한 관련 유틸리티 함수
 */

export interface User {
  id: number
  role: string
  is_active: boolean
  [key: string]: any
}

/**
 * 사용자 권한 레벨
 */
export enum UserRole {
  USER = 'user',
  POWER_USER = 'power_user', 
  ADMIN = 'admin'
}

/**
 * 권한 계층 구조
 */
const ROLE_HIERARCHY = {
  [UserRole.USER]: 0,
  [UserRole.POWER_USER]: 1,
  [UserRole.ADMIN]: 2
}

/**
 * 사용자가 특정 권한 이상인지 확인
 */
export function hasPermission(user: User | null, requiredRole: UserRole): boolean {
  if (!user || !user.is_active) return false
  
  const userLevel = ROLE_HIERARCHY[user.role as UserRole] || 0
  const requiredLevel = ROLE_HIERARCHY[requiredRole] || 0
  
  return userLevel >= requiredLevel
}

/**
 * 관리자 권한 확인
 */
export function isAdmin(user: User | null): boolean {
  return user?.role === UserRole.ADMIN && user?.is_active
}

/**
 * 파워유저 이상 권한 확인
 */
export function isPowerUserOrAbove(user: User | null): boolean {
  return hasPermission(user, UserRole.POWER_USER)
}

/**
 * 팀원 정보 수정 권한 확인
 */
export function canEditMember(user: User | null, targetMemberId: number): boolean {
  if (!user || !user.is_active) return false
  
  // 관리자는 모든 팀원 수정 가능
  if (user.role === UserRole.ADMIN) return true
  
  // 파워유저는 모든 팀원 수정 가능
  if (user.role === UserRole.POWER_USER) return true
  
  // 일반 사용자는 자신만 수정 가능
  if (user.role === UserRole.USER) return user.id === targetMemberId
  
  return false
}

/**
 * 팀원 삭제 권한 확인 (관리자만 가능)
 */
export function canDeleteMember(user: User | null, targetMemberId: number): boolean {
  if (!user || !user.is_active) return false
  
  // 관리자만 삭제 가능
  if (user.role !== UserRole.ADMIN) return false
  
  // 자기 자신은 삭제 불가
  if (user.id === targetMemberId) return false
  
  return true
}

/**
 * 공지사항 생성 권한 확인
 */
export function canCreateNotice(user: User | null, priority: string = 'normal'): boolean {
  if (!user || !user.is_active) return false
  
  // 관리자와 파워유저는 모든 우선순위 공지 생성 가능
  if (user.role === UserRole.ADMIN || user.role === UserRole.POWER_USER) {
    return true
  }
  
  // 일반 사용자는 일반 우선순위만 생성 가능
  if (user.role === UserRole.USER) {
    return priority === 'normal'
  }
  
  return false
}

/**
 * MSP 고객사 관리 권한 확인 (모든 로그인 사용자 가능)
 */
export function canManageCustomers(user: User | null): boolean {
  return user?.is_active || false
}

/**
 * 관리자 페이지 접근 권한 확인
 */
export function canAccessAdminPage(user: User | null): boolean {
  return isPowerUserOrAbove(user)
}

/**
 * 사용자별 수정 가능한 필드 목록 반환
 */
export function getAllowedMemberFields(user: User | null, targetMemberId: number): string[] {
  if (!user || !user.is_active) return []
  
  // 관리자는 모든 필드 수정 가능
  if (user.role === UserRole.ADMIN) {
    return ['name', 'email', 'phone', 'position', 'team', 'skills', 'join_date', 'profile_image', 'is_active', 'role']
  }
  
  // 파워유저는 권한 변경 제외하고 모든 필드 수정 가능
  if (user.role === UserRole.POWER_USER) {
    return ['name', 'email', 'phone', 'position', 'team', 'skills', 'join_date', 'profile_image', 'is_active']
  }
  
  // 일반 사용자는 자신의 기본 정보만 수정 가능
  if (user.role === UserRole.USER && user.id === targetMemberId) {
    return ['email', 'phone', 'skills', 'profile_image']
  }
  
  return []
}

/**
 * 이벤트 생성 권한 확인 (모든 로그인 사용자 가능)
 */
export function canCreateEvent(user: User | null): boolean {
  return user?.is_active || false
} 