import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/aws-tips',
      name: 'aws-tips',
      component: () => import('../views/AwsTipsView.vue'),
    },
    {
      path: '/notices',
      name: 'notices',
      component: () => import('../views/NoticesView.vue'),
    },
    {
      path: '/lunch',
      name: 'lunch',
      component: () => import('../views/LunchView.vue'),
    },
    {
      path: '/team',
      name: 'team',
      component: () => import('../views/TeamView.vue'),
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
    },
    {
      path: '/msp',
      name: 'msp',
      component: () => import('../views/MspView.vue'),
    },
  ],
})

export default router 