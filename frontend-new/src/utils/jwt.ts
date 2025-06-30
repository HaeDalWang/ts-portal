/**
 * JWT 토큰 관리 유틸리티
 * 토큰 저장, 조회, 검증, 만료 확인
 */

interface JwtPayload {
  user_id: number
  username: string
  email: string
  role: string
  exp: number
  iat: number
}

export class JwtManager {
  private readonly TOKEN_KEY = 'ts_portal_token_v2'
  private readonly USER_KEY = 'ts_portal_user_v2'

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
    localStorage.removeItem(this.USER_KEY)
  }

  /**
   * 토큰 존재 여부 확인
   */
  hasToken(): boolean {
    return !!this.getToken()
  }

  /**
   * JWT 페이로드 디코딩 (검증 없이)
   */
  decodeToken(token?: string): JwtPayload | null {
    const jwt = token || this.getToken()
    if (!jwt) return null

    try {
      const base64Url = jwt.split('.')[1]
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      )
      
      return JSON.parse(jsonPayload) as JwtPayload
    } catch (error) {
      console.error('JWT 디코딩 실패:', error)
      return null
    }
  }

  /**
   * 토큰 만료 확인
   */
  isTokenExpired(token?: string): boolean {
    const payload = this.decodeToken(token)
    if (!payload) return true

    const currentTime = Math.floor(Date.now() / 1000)
    return payload.exp < currentTime
  }

  /**
   * 토큰 만료까지 남은 시간 (초)
   */
  getTimeUntilExpiry(token?: string): number {
    const payload = this.decodeToken(token)
    if (!payload) return 0

    const currentTime = Math.floor(Date.now() / 1000)
    return Math.max(0, payload.exp - currentTime)
  }

  /**
   * 토큰 유효성 검사 (형식 + 만료)
   */
  isValidToken(token?: string): boolean {
    const jwt = token || this.getToken()
    if (!jwt) return false

    // JWT 형식 확인 (3개 부분으로 구성)
    const parts = jwt.split('.')
    if (parts.length !== 3) return false

    // 만료 확인
    return !this.isTokenExpired(jwt)
  }

  /**
   * 사용자 정보 저장
   */
  setUser(user: any): void {
    localStorage.setItem(this.USER_KEY, JSON.stringify(user))
  }

  /**
   * 사용자 정보 조회
   */
  getUser<T = any>(): T | null {
    const userStr = localStorage.getItem(this.USER_KEY)
    if (!userStr) return null

    try {
      return JSON.parse(userStr) as T
    } catch {
      return null
    }
  }

  /**
   * 모든 인증 정보 삭제
   */
  clearAll(): void {
    this.removeToken()
  }
}

// 싱글톤 인스턴스 생성
export const jwtManager = new JwtManager()

// 기본 export
export default jwtManager 