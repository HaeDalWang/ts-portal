/**
 * API 기본 설정 및 공통 함수들
 */

import axios from 'axios'

// 환경변수에서 API URL 가져오기
const getApiBaseUrl = (): string => {
  // 임시로 하드코딩하여 확실히 /api 접두사 포함
  return 'http://localhost:8001/api'
}

// API 기본 설정
const API_BASE_URL = getApiBaseUrl()

console.log(`[API Config] Base URL: ${API_BASE_URL}`)
console.log(`[API Config] Environment: ${import.meta.env.VITE_APP_ENV || (import.meta.env.DEV ? 'development' : 'production')}`)

// axios 인스턴스 생성
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 요청 인터셉터 - 토큰 자동 추가
apiClient.interceptors.request.use(
  (config) => {
    console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`)
    
    // localStorage에서 토큰 가져와서 헤더에 추가
    const token = localStorage.getItem('ts_portal_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error) => {
    console.error('[API Request Error]', error)
    return Promise.reject(error)
  }
)

// 응답 인터셉터
apiClient.interceptors.response.use(
  (response) => {
    console.log(`[API Response] ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error('[API Response Error]', error.response?.data || error.message)
    
    // 에러 메시지 한국어화
    if (error.response?.status === 404) {
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

// HoneyBox API용 별도 클라이언트 (AWS 뉴스 피드)
export const createHoneyBoxClient = () => {
  const honeyboxUrl = import.meta.env.VITE_HONEYBOX_API_URL || 
    (import.meta.env.DEV ? 'http://localhost:8000' : 'https://tsapi.seungdobae.com/api/feeds')
  
  console.log(`[HoneyBox API] URL: ${honeyboxUrl}`)
  
  return axios.create({
    baseURL: honeyboxUrl,
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
    },
  })
}

export default apiClient 