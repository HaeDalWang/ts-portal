/**
 * 인증 서비스
 * 로그인, 로그아웃, 토큰 관리, 권한 확인 등을 담당
 */

import { api } from './api'

// 사용자 권한 타입
export enum UserRole {
  ADMIN = 'admin',
  POWER_USER = 'power_user',
  USER = 'user'
}

// 사용자 정보 타입
export interface User {
  id: number
  name: string
  email: string
  phone?: string
  position?: string
  team: string
  role: UserRole
  is_active: boolean
  last_login?: string
  mfa_enabled: boolean
  created_at: string
  updated_at: string
  skills_list: string[]
}

// 로그인 요청 타입
export interface LoginRequest {
  email: string
  password: string
}

// 로그인 응답 타입
export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

// 현재 사용자 정보 타입
export interface CurrentUser {
  id: number
  email: string
  name: string
  role: UserRole
  is_active: boolean
}

class AuthService {
  private readonly TOKEN_KEY = 'ts_portal_token'
  private readonly USER_KEY = 'ts_portal_user'

  /**
   * 로그인
   */
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    try {
      const response = await api.post<any>('/auth/login', credentials)
      
      console.log('🔐 로그인 응답:', response)
      
      // API 응답 구조 확인 후 적절히 처리
      let token: string
      let user: User
      
      if (response.access_token) {
        // 응답에 직접 토큰이 있는 경우
        token = response.access_token
        user = response.user
      } else if (response.data && response.data.access_token) {
        // 응답이 data 객체로 감싸진 경우
        token = response.data.access_token
        user = response.data.user
      } else {
        throw new Error('로그인 응답 형식이 올바르지 않습니다.')
      }
      
      // 토큰과 사용자 정보 저장
      this.setToken(token)
      this.setUser(user)
      
      console.log('🔐 토큰 저장됨:', token)
      console.log('👤 사용자 정보 저장됨:', user)
      
      return response
    } catch (error) {
      console.error('🔐 로그인 에러:', error)
      throw new Error('로그인에 실패했습니다. 이메일과 비밀번호를 확인해주세요.')
    }
  }

  /**
   * 로그아웃
   */
  logout(): void {
    this.removeToken()
    this.removeUser()
    // 로그인 페이지로 리디렉션은 호출하는 곳에서 처리
  }

  /**
   * 토큰 저장
   */
  setToken(token: string): void {
    localStorage.setItem(this.TOKEN_KEY, token)
  }

  /**
   * 토큰 조회
   */
  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY)
  }

  /**
   * 토큰 삭제
   */
  removeToken(): void {
    localStorage.removeItem(this.TOKEN_KEY)
  }

  /**
   * 사용자 정보 저장
   */
  setUser(user: User): void {
    localStorage.setItem(this.USER_KEY, JSON.stringify(user))
  }

  /**
   * 사용자 정보 조회
   */
  getUser(): User | null {
    const userStr = localStorage.getItem(this.USER_KEY)
    return userStr ? JSON.parse(userStr) : null
  }

  /**
   * 사용자 정보 삭제
   */
  removeUser(): void {
    localStorage.removeItem(this.USER_KEY)
  }

  /**
   * 로그인 상태 확인
   */
  isAuthenticated(): boolean {
    const token = this.getToken()
    const user = this.getUser()
    return !!(token && user)
  }

  /**
   * 토큰 검증 및 사용자 정보 갱신
   */
  async verifyToken(): Promise<CurrentUser | null> {
    try {
      const token = this.getToken()
      if (!token) return null

      const response = await api.post<CurrentUser>('/auth/verify')
      return response
    } catch (error) {
      // 토큰이 유효하지 않으면 로그아웃 처리
      this.logout()
      return null
    }
  }

  /**
   * 내 정보 조회
   */
  async getMyInfo(): Promise<User> {
    try {
      const response = await api.post<User>('/auth/verify')
      this.setUser(response) // 최신 정보로 업데이트
      return response
    } catch (error) {
      throw new Error('사용자 정보를 가져올 수 없습니다.')
    }
  }

  /**
   * 비밀번호 변경
   */
  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    try {
      await api.post('/auth/change-password', {
        current_password: currentPassword,
        new_password: newPassword
      })
    } catch (error: any) {
      console.error('🔒 비밀번호 변경 실패:', error)
      throw new Error(error.response?.data?.detail || '비밀번호 변경에 실패했습니다.')
    }
  }

  /**
   * 내 정보 수정
   */
  async updateMyInfo(updateData: { email?: string; phone?: string; skills?: string[] }): Promise<User> {
    try {
      const currentUser = this.getUser()
      if (!currentUser) {
        throw new Error('로그인이 필요합니다.')
      }

      // 기술스택이 배열로 전달된 경우 문자열로 변환
      const requestData = {
        ...updateData,
        skills: Array.isArray(updateData.skills) ? updateData.skills.join(', ') : updateData.skills
      }

      const response = await api.put<User>(`/members/${currentUser.id}`, requestData)
      
      // 로컬 저장소의 사용자 정보 업데이트
      this.setUser(response)
      
      return response
    } catch (error: any) {
      console.error('👤 프로필 수정 실패:', error)
      throw new Error(error.response?.data?.detail || '프로필 수정에 실패했습니다.')
    }
  }

  /**
   * 권한 확인
   */
  hasPermission(requiredRole: UserRole): boolean {
    const user = this.getUser()
    if (!user) return false

    const roleHierarchy = {
      [UserRole.USER]: 0,
      [UserRole.POWER_USER]: 1,
      [UserRole.ADMIN]: 2
    }

    return roleHierarchy[user.role] >= roleHierarchy[requiredRole]
  }

  /**
   * 관리자 권한 확인
   */
  isAdmin(): boolean {
    const user = this.getUser()
    return user?.role === UserRole.ADMIN
  }

  /**
   * 파워유저 이상 권한 확인
   */
  isPowerUserOrAbove(): boolean {
    const user = this.getUser()
    return user?.role === UserRole.POWER_USER || user?.role === UserRole.ADMIN
  }

  /**
   * Authorization 헤더 생성
   */
  getAuthHeader(): Record<string, string> {
    const token = this.getToken()
    return token ? { Authorization: `Bearer ${token}` } : {}
  }
}

// 싱글톤 인스턴스 생성
export const authService = new AuthService()
export default authService 