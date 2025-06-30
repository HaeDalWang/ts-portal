/**
 * API 관련 공통 타입 정의
 * Kong Gateway를 통한 MSA 서비스 연동
 */

// HTTP 메서드
export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'

// API 응답 기본 구조
export interface ApiResponse<T = any> {
  data?: T
  message?: string
  status: number
  success: boolean
}

// API 에러 응답
export interface ApiError {
  detail: string
  status: number
  timestamp?: string
  service?: string
}

// 페이지네이션
export interface Pagination {
  page: number
  size: number
  total: number
  pages: number
}

// 페이지네이션된 응답
export interface PaginatedResponse<T> {
  items: T[]
  pagination: Pagination
}

// 로딩 상태
export interface LoadingState {
  loading: boolean
  error: string | null
}

// API 요청 옵션
export interface ApiRequestOptions {
  headers?: Record<string, string>
  timeout?: number
  retries?: number
  data?: any
  signal?: AbortSignal
}

// Kong Gateway 서비스 정보
export interface ServiceInfo {
  name: string
  port: number
  baseUrl: string
  healthEndpoint: string
} 