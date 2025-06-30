/**
 * Auth Service API
 * Kong Gateway를 통한 인증 서비스 연동 (/api/auth/*)
 */

import { kongApi } from './api'
import type { LoginRequest, LoginResponse, User, TokenVerifyResponse } from '@/types/auth'

export class AuthService {
  private readonly basePath = '/api/auth'

  /**
   * 로그인
   */
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await kongApi.post<LoginResponse>(`${this.basePath}/login`, credentials)
    
    // 🔥 토큰 설정은 useAuth에서 담당하도록 변경
    // if (response.access_token) {
    //   kongApi.setAuthToken(response.access_token)
    // }
    
    return response
  }

  /**
   * 로그아웃
   */
  async logout(): Promise<void> {
    try {
      await kongApi.post(`${this.basePath}/logout`)
    } finally {
      // 성공/실패 관계없이 토큰 제거
      kongApi.removeAuthToken()
    }
  }

  /**
   * 토큰 검증 및 사용자 정보 조회
   */
  async verifyToken(): Promise<User> {
    return kongApi.post<User>(`${this.basePath}/verify`)
  }

  /**
   * 현재 사용자 정보 조회
   */
  async getCurrentUser(): Promise<User> {
    return kongApi.get<User>(`${this.basePath}/me`)
  }

  /**
   * 토큰 갱신
   */
  async refreshToken(): Promise<LoginResponse> {
    const response = await kongApi.post<LoginResponse>(`${this.basePath}/refresh`)
    
    // 새 토큰을 API 클라이언트에 설정
    if (response.access_token) {
      kongApi.setAuthToken(response.access_token)
    }
    
    return response
  }

  /**
   * 비밀번호 변경
   */
  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    await kongApi.post(`${this.basePath}/change-password`, {
      current_password: currentPassword,
      new_password: newPassword
    })
  }

  /**
   * Auth Service 상태 확인
   */
  async healthCheck(): Promise<boolean> {
    try {
      await kongApi.get(`${this.basePath}/health`)
      return true
    } catch {
      return false
    }
  }
}

// 싱글톤 인스턴스 생성
export const authService = new AuthService()

// 기본 export
export default authService 