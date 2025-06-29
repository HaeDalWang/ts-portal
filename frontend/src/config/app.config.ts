/**
 * 앱 전역 설정 관리
 * 환경변수 기반으로 앱 설정을 관리합니다.
 */

// 앱 설정 타입 정의
export interface AppConfig {
  name: string
  version: string
  environment: string
  debug: {
    enabled: boolean
    console: boolean
  }
  external: {
    naverMapClientId: string
  }
  ui: {
    defaultPageSize: number
    maxFileSize: number
    supportedImageTypes: string[]
  }
}

// 앱 설정 가져오기
const getAppConfig = (): AppConfig => {
  return {
    name: import.meta.env.VITE_APP_NAME || 'TS Portal',
    version: import.meta.env.VITE_APP_VERSION || '2.0.0',
    environment: import.meta.env.VITE_APP_ENV || 'development',
    debug: {
      enabled: import.meta.env.VITE_DEBUG_MODE === 'true',
      console: import.meta.env.VITE_CONSOLE_LOG === 'true',
    },
    external: {
      naverMapClientId: import.meta.env.VITE_NAVER_MAP_CLIENT_ID || '',
    },
    ui: {
      defaultPageSize: 10,
      maxFileSize: 5 * 1024 * 1024, // 5MB
      supportedImageTypes: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
    }
  }
}

// 앱 설정 내보내기
export const APP_CONFIG = getAppConfig()

// 디버그 정보 출력
if (APP_CONFIG.debug.console) {
  console.log('⚙️ [App Config] 앱 설정:')
  console.log(`  - 이름: ${APP_CONFIG.name}`)
  console.log(`  - 버전: ${APP_CONFIG.version}`)
  console.log(`  - 환경: ${APP_CONFIG.environment}`)
  console.log(`  - 디버그: ${APP_CONFIG.debug.enabled}`)
}

// 환경별 헬퍼 함수들
export const isDevelopment = (): boolean => APP_CONFIG.environment === 'development'
export const isProduction = (): boolean => APP_CONFIG.environment === 'production'
export const isDebugMode = (): boolean => APP_CONFIG.debug.enabled

// 로그 헬퍼 함수
export const debugLog = (message: string, ...args: any[]): void => {
  if (APP_CONFIG.debug.console) {
    console.log(`🐛 [Debug] ${message}`, ...args)
  }
}

export default APP_CONFIG 