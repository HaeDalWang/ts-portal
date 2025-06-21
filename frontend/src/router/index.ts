import { createRouter, createWebHistory } from 'vue-router'
import authService from '@/services/authService'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import AwsTipsView from '../views/AwsTipsView.vue'
import ProfileView from '../views/ProfileView.vue'
import AdminView from '../views/AdminView.vue'
import TeamView from '../views/TeamView.vue'
import MspView from '../views/MspView.vue'
import NoticesView from '../views/NoticesView.vue'
import LunchView from '../views/LunchView.vue'
import NotFoundView from '../views/NotFoundView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true }
    },
    {
      path: '/team',
      name: 'team',
      component: TeamView,
      meta: { requiresAuth: true }
    },
    {
      path: '/msp',
      name: 'msp',
      component: MspView,
      meta: { requiresAuth: true }
    },
    {
      path: '/notices',
      name: 'notices',
      component: NoticesView,
      meta: { requiresAuth: true }
    },
    {
      path: '/lunch',
      name: 'lunch',
      component: LunchView,
      meta: { requiresAuth: true }
    },
    {
      path: '/aws-tips',
      name: 'aws-tips',
      component: AwsTipsView,
      meta: { requiresAuth: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true }
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminView,
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: NotFoundView
    }
  ]
})

// 라우터 가드
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('ts_portal_token')
  const user = authService.getUser()
  
  console.log('🛣️ 라우터 가드:', {
    to: to.path,
    from: from.path,
    token: token ? '존재함' : '없음',
    user: user ? user.name : '없음',
    requiresAuth: to.meta.requiresAuth,
    requiresAdmin: to.meta.requiresAdmin
  })
  
  if (to.meta.requiresAuth && !token) {
    console.log('🚫 인증 필요 - 로그인 페이지로 이동')
    next('/login')
  } else if (to.meta.requiresAdmin && (!user || user.role !== 'admin')) {
    // 관리자 권한이 필요한 페이지에 일반 사용자가 접근하려고 할 때
    console.log('🚫 관리자 권한 필요 - 홈으로 이동')
    next('/')
  } else if (to.name === 'login' && token) {
    console.log('✅ 이미 로그인됨 - 홈으로 이동')
    next('/')
  } else {
    console.log('✅ 라우터 가드 통과')
    next()
  }
})

export default router 