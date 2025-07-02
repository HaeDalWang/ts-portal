/**
 * Kong Gateway API 클래스
 * 모든 MSA 서비스 연동의 기반이 되는 핵심 클래스
 */

import type { HttpMethod, ApiResponse, ApiError, ApiRequestOptions } from '@/types/api'

export class KongApiClient {
  private readonly baseUrl: string
  private readonly timeout: number
  private defaultHeaders: Record<string, string>
  private authToken?: string

  constructor(baseUrl?: string) {
    // 환경변수에서 API URL 가져오기, 없으면 기본값 사용
    this.baseUrl = baseUrl || import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
    this.timeout = 10000 // 10초
    this.defaultHeaders = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    
    // 개발 환경에서 API URL 로깅
    if (import.meta.env.DEV) {
      console.log('🔧 API Base URL:', this.baseUrl)
    }
  }

  /**
   * JWT 토큰 설정
   */
  setAuthToken(token: string): void {
    this.authToken = token
    this.defaultHeaders['Authorization'] = `Bearer ${token}`
  }

  /**
   * JWT 토큰 제거
   */
  removeAuthToken(): void {
    delete this.defaultHeaders['Authorization']
    this.authToken = undefined
  }

  /**
   * 현재 사용자 정보 헤더 추가
   */
  private async addUserHeaders(): Promise<Record<string, string>> {
    const userHeaders: Record<string, string> = {}
    
    try {
      // JWT에서 사용자 정보 가져오기
      const { jwtManager } = await import('@/utils/jwt')
      const user = jwtManager.getUser()
      
      if (user && typeof user === 'object' && 'id' in user && 'role' in user) {
        userHeaders['X-User-ID'] = String(user.id)
        userHeaders['X-User-Role'] = String(user.role)
        console.log('🔐 사용자 헤더 추가:', { userId: user.id, role: user.role })
      }
    } catch (error) {
      console.warn('⚠️ 사용자 헤더 추가 실패:', error)
    }
    
    return userHeaders
  }

  /**
   * HTTP 요청 실행
   */
  private async request<T>(
    method: string,
    endpoint: string,
    options: ApiRequestOptions = {}
  ): Promise<T> {
    const { data, headers: customHeaders, timeout = 10000, signal } = options

    // 사용자 정보 헤더 추가
    const userHeaders = await this.addUserHeaders()

    // 기본 헤더 설정
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...this.defaultHeaders,
      ...userHeaders,
      ...customHeaders
    }

    // 토큰 로깅
    if (this.authToken) {
      console.log('🔐 API 요청에 토큰 추가:', endpoint, 'Token:', this.authToken.substring(0, 20) + '...')
    } else {
      console.log('⚠️ API 요청에 토큰 없음:', endpoint)
    }

    // 요청 설정
    const config: RequestInit = {
      method,
      headers,
      signal: signal || AbortSignal.timeout(timeout)
    }

    // GET 요청이 아닌 경우 body 추가
    if (method !== 'GET' && data) {
      config.body = JSON.stringify(data)
    }

    const url = `${this.baseUrl}${endpoint}`
    console.log(`🌐 ${method} ${url}`)

    try {
      const response = await fetch(url, config)
      
      // 응답 상태 확인
      if (!response.ok) {
        const errorText = await response.text()
        console.error(`❌ API 에러 [${response.status}]:`, errorText)
        
        if (response.status === 401) {
          throw new Error(`인증 오류: ${errorText}`)
        } else if (response.status === 403) {
          throw new Error(`권한 오류: ${errorText}`)
        } else if (response.status >= 500) {
          throw new Error(`서버 오류: ${errorText}`)
        } else {
          throw new Error(`요청 실패 (${response.status}): ${errorText}`)
        }
      }

      // JSON 응답 파싱
      const result = await response.json()
      console.log(`✅ ${method} ${url} 성공`)
      return result

    } catch (error) {
      if (error instanceof Error) {
        console.error(`💥 ${method} ${url} 실패:`, error.message)
        throw error
      }
      throw new Error('알 수 없는 오류가 발생했습니다.')
    }
  }

  /**
   * GET 요청
   */
  async get<T = any>(endpoint: string, options?: ApiRequestOptions): Promise<T> {
    return this.request<T>('GET', endpoint, options)
  }

  /**
   * POST 요청
   */
  async post<T = any>(endpoint: string, data?: any, options?: ApiRequestOptions): Promise<T> {
    return this.request<T>('POST', endpoint, { data, ...options })
  }

  /**
   * PUT 요청
   */
  async put<T = any>(endpoint: string, data?: any, options?: ApiRequestOptions): Promise<T> {
    return this.request<T>('PUT', endpoint, { data, ...options })
  }

  /**
   * DELETE 요청
   */
  async delete<T = any>(endpoint: string, options?: ApiRequestOptions): Promise<T> {
    return this.request<T>('DELETE', endpoint, options)
  }

  /**
   * PATCH 요청
   */
  async patch<T = any>(endpoint: string, data?: any, options?: ApiRequestOptions): Promise<T> {
    return this.request<T>('PATCH', endpoint, { data, ...options })
  }

  /**
   * Kong Gateway 상태 확인
   */
  async healthCheck(): Promise<boolean> {
    try {
      await this.get('/health')
      return true
    } catch {
      return false
    }
  }
}

// 싱글톤 인스턴스 생성
export const kongApi = new KongApiClient()

// 기본 export
export default kongApi 