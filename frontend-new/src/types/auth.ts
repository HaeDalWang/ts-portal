/**
 * Auth Service 타입 정의
 * JWT 기반 인증 시스템
 */

// 사용자 권한
export enum UserRole {
  ADMIN = 'admin',
  POWER_USER = 'power_user', 
  USER = 'user'
}

// 사용자 정보 (백엔드 CurrentUserResponse와 일치)
export interface User {
  id: number
  name: string
  email: string
  role: UserRole
  position?: string
  team: string
  is_active: boolean
  last_login?: string
}

// 로그인 요청
export interface LoginRequest {
  username: string
  password: string
}

// 로그인 응답
export interface LoginResponse {
  access_token: string
  token_type: string
  expires_in: number
  user: User
}

// 토큰 검증 요청
export interface TokenVerifyRequest {
  token: string
}

// 토큰 검증 응답
export interface TokenVerifyResponse {
  valid: boolean
  user?: User
  expired?: boolean
}

// 인증 상태
export interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  loading: boolean
  error: string | null
} 