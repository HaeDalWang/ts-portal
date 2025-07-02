/**
 * API 설정 통합 관리
 * 환경변수 기반으로 API URL 및 설정을 관리합니다.
 */

// 환경 타입 정의
export type Environment = 'development' | 'production' | 'test'

// API 설정 타입 정의
export interface ApiConfig {
  baseURL: string
  timeout: number
  services: {
    auth: string
    member: string
    customer: string
    calendar: string
    notice: string
    feeds: string
  }
}

// 현재 환경 감지
export const getCurrentEnvironment = (): Environment => {
  const env = import.meta.env.VITE_APP_ENV
  if (env === 'production') return 'production'
  if (env === 'test') return 'test'
  return 'development'
}

// 환경변수에서 API 설정 가져오기
const getApiConfig = (): ApiConfig => {
  const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'
  const timeout = parseInt(import.meta.env.VITE_API_TIMEOUT || '10000')

  // API Gateway를 통한 통합 접근이 기본
  const config: ApiConfig = {
    baseURL,
    timeout,
    services: {
      auth: `${baseURL}/auth`,
      member: `${baseURL}/members`, 
      customer: `${baseURL}/customers`,
      calendar: `${baseURL}/calendar`,
      notice: `${baseURL}/notices`,
      feeds: `${baseURL}/feeds`,
    }
  }

  // 개발 환경에서 직접 서비스 접근이 필요한 경우 (백업)
  if (getCurrentEnvironment() === 'development') {
    const directServices = {
      auth: import.meta.env.VITE_AUTH_SERVICE_URL,
      member: import.meta.env.VITE_MEMBER_SERVICE_URL,
      customer: import.meta.env.VITE_CUSTOMER_SERVICE_URL,
      calendar: import.meta.env.VITE_CALENDAR_SERVICE_URL,
      notice: import.meta.env.VITE_NOTICE_SERVICE_URL,
      feeds: import.meta.env.VITE_FEEDS_SERVICE_URL,
    }

    // 직접 서비스 URL이 설정된 경우에만 사용
    Object.entries(directServices).forEach(([key, url]) => {
      if (url && url !== 'undefined') {
        console.log(`🔧 [API Config] ${key} 서비스 직접 접근: ${url}`)
      }
    })
  }

  return config
}

// API 설정 내보내기
export const API_CONFIG = getApiConfig()

// 디버그 정보 출력
if (import.meta.env.VITE_DEBUG_MODE === 'true') {
  console.log('🔧 [API Config] 설정 정보:')
  console.log(`  - 환경: ${getCurrentEnvironment()}`)
  console.log(`  - Base URL: ${API_CONFIG.baseURL}`)
  console.log(`  - Timeout: ${API_CONFIG.timeout}ms`)
  console.log('  - 서비스 URL들:', API_CONFIG.services)
}

// 개별 서비스 URL 헬퍼 함수들
export const getServiceUrl = (service: keyof ApiConfig['services']): string => {
  return API_CONFIG.services[service]
}

// API 상태 확인 함수
export const checkApiHealth = async (): Promise<boolean> => {
  try {
    const response = await fetch(`${API_CONFIG.baseURL.replace('/api', '')}/health`)
    return response.ok
  } catch (error) {
    console.error('❌ [API Config] API 상태 확인 실패:', error)
    return false
  }
}

export default API_CONFIG 