/**
 * API 기본 설정 및 공통 함수들
 * 환경변수 기반으로 API URL 관리
 */

import axios from 'axios'
import { API_CONFIG, getServiceUrl } from '@/config/api.config'
import { debugLog } from '@/config/app.config'

// axios 인스턴스 생성 (API Gateway 기반)
const apiClient = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 요청 인터셉터 - 토큰 자동 추가
apiClient.interceptors.request.use(
  (config) => {
    debugLog(`API Request: ${config.method?.toUpperCase()} ${config.url}`)
    
    // localStorage에서 토큰 가져와서 헤더에 추가
    const token = localStorage.getItem('ts_portal_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error) => {
    console.error('❌ [API Request Error]', error)
    return Promise.reject(error)
  }
)

// 응답 인터셉터
apiClient.interceptors.response.use(
  (response) => {
    debugLog(`API Response: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error('❌ [API Response Error]', error.response?.data || error.message)
    
    // 에러 메시지 한국어화
    if (error.response?.status === 401) {
      error.message = '인증이 필요합니다. 다시 로그인해주세요.'
      // 토큰 만료 시 로그인 페이지로 리다이렉트
      localStorage.removeItem('ts_portal_token')
      window.location.href = '/login'
    } else if (error.response?.status === 403) {
      error.message = '접근 권한이 없습니다.'
    } else if (error.response?.status === 404) {
      error.message = '요청한 리소스를 찾을 수 없습니다.'
    } else if (error.response?.status === 400) {
      error.message = error.response.data?.detail || '잘못된 요청입니다.'
    } else if (error.response?.status === 500) {
      error.message = '서버 내부 오류가 발생했습니다.'
    } else if (error.code === 'ECONNABORTED') {
      error.message = '요청 시간이 초과되었습니다.'
    } else if (error.code === 'ERR_NETWORK') {
      error.message = '네트워크 연결을 확인해주세요.'
    }
    
    return Promise.reject(error)
  }
)

// API 응답 타입 정의
export interface ApiResponse<T> {
  data: T
  status: number
  message?: string
}

// 페이징 응답 타입
export interface PaginatedResponse<T> {
  total: number
  items: T[]
  page?: number
  size?: number
}

// 공통 API 함수들
export const api = {
  // GET 요청
  get: <T>(url: string, params?: any): Promise<T> => 
    apiClient.get(url, { params }).then(response => response.data),
  
  // POST 요청
  post: <T>(url: string, data?: any): Promise<T> => 
    apiClient.post(url, data).then(response => response.data),
  
  // PUT 요청
  put: <T>(url: string, data?: any): Promise<T> => 
    apiClient.put(url, data).then(response => response.data),
  
  // PATCH 요청
  patch: <T>(url: string, data?: any): Promise<T> => 
    apiClient.patch(url, data).then(response => response.data),
  
  // DELETE 요청
  delete: (url: string): Promise<void> => 
    apiClient.delete(url).then(() => undefined),
}

// 서비스별 API 클라이언트 생성 함수
export const createServiceClient = (service: keyof typeof API_CONFIG.services) => {
  const serviceUrl = getServiceUrl(service)
  
  return axios.create({
    baseURL: serviceUrl,
    timeout: API_CONFIG.timeout,
    headers: {
      'Content-Type': 'application/json',
    },
  })
}

// Feeds Service용 별도 클라이언트 (AWS 소식)
export const createFeedsClient = () => {
  const feedsUrl = getServiceUrl('feeds')
  
  debugLog(`Feeds API URL: ${feedsUrl}`)
  
  return axios.create({
    baseURL: feedsUrl,
    timeout: API_CONFIG.timeout,
    headers: {
      'Content-Type': 'application/json',
    },
  })
}

// 기본 API 클라이언트 내보내기
export default apiClient 