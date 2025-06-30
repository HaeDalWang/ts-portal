/**
 * 인증 상태 관리 Composable
 * Vue 3 Composition API 기반
 */

import { ref, computed, onMounted } from 'vue'
import { authService } from '@/services/auth'
import { jwtManager } from '@/utils/jwt'
import type { User, LoginRequest, AuthState } from '@/types/auth'

// 글로벌 상태 (모든 컴포넌트에서 공유)
const user = ref<User | null>(null)
const token = ref<string | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

export function useAuth() {
  // 계산된 속성
  const isAuthenticated = computed(() => {
    return !!token.value && !!user.value && jwtManager.isValidToken(token.value)
  })

  const currentUser = computed(() => user.value)

  /**
   * 로그인
   */
  const login = async (credentials: LoginRequest): Promise<boolean> => {
    loading.value = true
    error.value = null

    try {
      const response = await authService.login(credentials)
      
      // 상태 업데이트
      token.value = response.access_token
      user.value = response.user
      
      // 로컬 스토리지에 저장
      jwtManager.setToken(response.access_token)
      jwtManager.setUser(response.user)
      
      // 🔥 Kong API 클라이언트에 토큰 설정 확인
      const { kongApi } = await import('@/services/api')
      kongApi.setAuthToken(response.access_token)
      
      console.log('🔐 로그인 성공:', response.user.name)
      console.log('🔐 토큰 설정 완료:', response.access_token.substring(0, 20) + '...')
      return true
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '로그인에 실패했습니다.'
      error.value = errorMessage
      console.error('🔐 로그인 실패:', errorMessage)
      return false
      
    } finally {
      loading.value = false
    }
  }

  /**
   * 로그아웃
   */
  const logout = async (): Promise<void> => {
    loading.value = true
    
    try {
      await authService.logout()
    } catch (err) {
      console.warn('로그아웃 API 호출 실패:', err)
    } finally {
      // 상태 초기화 (API 실패와 관계없이)
      token.value = null
      user.value = null
      error.value = null
      
      // 로컬 스토리지 정리
      jwtManager.clearAll()
      
      loading.value = false
      console.log('🔐 로그아웃 완료')
    }
  }

  /**
   * 토큰 검증 및 사용자 정보 갱신
   */
  const verifyToken = async (): Promise<boolean> => {
    const storedToken = jwtManager.getToken()
    if (!storedToken || jwtManager.isTokenExpired(storedToken)) {
      console.log('🔐 토큰 없음 또는 만료됨')
      await logout()
      return false
    }

    loading.value = true
    
    try {
      // getCurrentUser로 토큰 검증 및 사용자 정보 조회
      const userData = await authService.getCurrentUser()
      
      // 상태 업데이트
      token.value = storedToken
      user.value = userData
      jwtManager.setUser(userData)
      
      console.log('🔐 토큰 검증 성공:', userData.name)
      return true
      
    } catch (err) {
      console.error('🔐 토큰 검증 실패:', err)
      await logout()
      return false
      
    } finally {
      loading.value = false
    }
  }

  /**
   * 사용자 정보 새로고침
   */
  const refreshUser = async (): Promise<boolean> => {
    if (!isAuthenticated.value) {
      console.log('🔐 인증되지 않은 상태, refreshUser 중단')
      return false
    }

    loading.value = true
    
    try {
      // verifyToken 대신 getCurrentUser 사용
      const userData = await authService.getCurrentUser()
      user.value = userData
      jwtManager.setUser(userData)
      console.log('🔐 사용자 정보 갱신 성공:', userData.name)
      return true
      
    } catch (err) {
      console.error('🔐 사용자 정보 갱신 실패:', err)
      error.value = '사용자 정보를 가져올 수 없습니다.'
      
      // 401 에러인 경우 로그아웃 처리
      if (err instanceof Error && err.message.includes('401')) {
        console.log('🔐 401 에러로 인한 자동 로그아웃')
        await logout()
      }
      
      return false
      
    } finally {
      loading.value = false
    }
  }

  /**
   * 권한 확인
   */
  const hasRole = (requiredRole: string): boolean => {
    if (!user.value) return false
    
    const roleHierarchy = { user: 0, power_user: 1, admin: 2 }
    const userLevel = roleHierarchy[user.value.role as keyof typeof roleHierarchy] ?? -1
    const requiredLevel = roleHierarchy[requiredRole as keyof typeof roleHierarchy] ?? 999
    
    return userLevel >= requiredLevel
  }

  /**
   * 관리자 권한 확인
   */
  const isAdmin = computed(() => hasRole('admin'))

  /**
   * 파워유저 이상 권한 확인
   */
  const isPowerUser = computed(() => hasRole('power_user'))

  /**
   * 에러 초기화
   */
  const clearError = (): void => {
    error.value = null
  }

  /**
   * 초기화 (앱 시작 시)
   */
  const initialize = async (): Promise<void> => {
    const storedToken = jwtManager.getToken()
    const storedUser = jwtManager.getUser<User>()
    
    console.log('🔐 초기화 시작:', { hasToken: !!storedToken, hasUser: !!storedUser })
    
    if (storedToken && storedUser && !jwtManager.isTokenExpired(storedToken)) {
      // 저장된 정보로 상태 복원
      token.value = storedToken
      user.value = storedUser
      
      // 🔥 중요: Kong API 클라이언트에 토큰 설정
      const { kongApi } = await import('@/services/api')
      kongApi.setAuthToken(storedToken)
      
      console.log('🔐 토큰 복원 완료:', storedToken.substring(0, 20) + '...')
      
      // 토큰 검증 (백그라운드에서)
      try {
        await verifyToken()
        console.log('🔐 토큰 검증 성공')
      } catch (err) {
        console.warn('🔐 토큰 검증 실패, 로그아웃:', err)
        await logout()
      }
    } else {
      console.log('🔐 저장된 인증 정보 없음 또는 만료됨')
    }
  }

  return {
    // 상태
    user: currentUser,
    loading: computed(() => loading.value),
    error: computed(() => error.value),
    isAuthenticated,
    isAdmin,
    isPowerUser,
    
    // 메서드
    login,
    logout,
    verifyToken,
    refreshUser,
    hasRole,
    clearError,
    initialize
  }
} 