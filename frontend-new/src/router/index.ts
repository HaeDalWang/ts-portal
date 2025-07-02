/**
 * Vue Router 설정
 * 라우터 가드 및 인증 체크 포함
 */

import { createRouter, createWebHistory } from 'vue-router'
import { jwtManager } from '@/utils/jwt'

// 라우터 설정
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      redirect: '/dashboard'
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/LoginView.vue'),
      meta: {
        requiresAuth: false,
        title: '로그인 - TS Portal'
      }
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('@/views/DashboardView.vue'),
      meta: {
        requiresAuth: true,
        title: '대시보드 - TS Portal'
      }
    },
    {
      path: '/members',
      name: 'Members',
      component: () => import('@/views/MemberView.vue'),
      meta: {
        requiresAuth: true,
        title: '팀원 관리 - TS Portal'
      }
    },
    {
      path: '/customers',
      name: 'Customers',
      component: () => import('@/views/CustomerView.vue'),
      meta: {
        requiresAuth: true,
        title: '고객사 관리 - TS Portal'
      }
    },
    {
      path: '/calendar',
      name: 'Calendar',
      component: () => import('@/views/CalendarView.vue'),
      meta: {
        requiresAuth: true,
        title: '일정 관리 - TS Portal'
      }
    },
    {
      path: '/notices',
      name: 'Notices',
      component: () => import('@/views/NoticesView.vue'),
      meta: {
        requiresAuth: true,
        title: '공지사항 - TS Portal'
      }
    },
    {
      path: '/feeds',
      name: 'Feeds',
      component: () => import('@/views/AwsFeedsView.vue'),
      meta: {
        requiresAuth: true,
        title: 'AWS 피드 - TS Portal'
      }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/views/NotFoundView.vue'),
      meta: {
        requiresAuth: false,
        title: '페이지를 찾을 수 없음 - TS Portal'
      }
    }
  ]
})

/**
 * 라우터 가드 - 인증 체크
 */
router.beforeEach(async (to, from, next) => {
  // 페이지 타이틀 설정
  if (to.meta.title) {
    document.title = to.meta.title as string
  }

  // 인증이 필요한 페이지 체크
  if (to.meta.requiresAuth) {
    const token = jwtManager.getToken()
    
    console.log('🔐 라우터 가드:', { 
      path: to.path, 
      hasToken: !!token, 
      isExpired: token ? jwtManager.isTokenExpired(token) : 'no-token' 
    })
    
    // 토큰이 없거나 만료된 경우
    if (!token || jwtManager.isTokenExpired(token)) {
      console.log('🔐 인증 필요: 로그인 페이지로 리디렉션')
      next({
        name: 'Login',
        query: { redirect: to.fullPath } // 로그인 후 원래 페이지로 돌아가기
      })
      return
    }
    
    // 토큰이 있지만 Kong API 클라이언트에 설정되지 않은 경우
    try {
      const { kongApi } = await import('@/services/api')
      kongApi.setAuthToken(token)
      console.log('🔐 라우터 가드에서 토큰 설정 완료')
    } catch (err) {
      console.error('🔐 라우터 가드에서 토큰 설정 실패:', err)
    }
  }

  // 이미 로그인된 사용자가 로그인 페이지 접근 시
  if (to.name === 'Login') {
    const token = jwtManager.getToken()
    if (token && !jwtManager.isTokenExpired(token)) {
      console.log('🔐 이미 로그인됨: 대시보드로 리디렉션')
      next({ name: 'Dashboard' })
      return
    }
  }

  next()
})

/**
 * 라우터 에러 핸들링
 */
router.onError((error) => {
  console.error('🔥 라우터 에러:', error)
})

export default router 