/**
 * Vue 3 애플리케이션 엔트리 포인트
 * TS Portal Frontend v2.0
 */

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// 글로벌 스타일 import
import './styles/global.css'

// Vue 애플리케이션 생성
const app = createApp(App)

// 라우터 등록
app.use(router)

// 🔥 앱 시작 시 인증 상태 초기화
async function initializeApp() {
  try {
    const { useAuth } = await import('./composables/useAuth')
    const { initialize } = useAuth()
    await initialize()
    console.log('🚀 앱 초기화 완료')
  } catch (error) {
    console.error('🔥 앱 초기화 실패:', error)
  }
}

// 애플리케이션 마운트 및 초기화
app.mount('#app')
initializeApp()

console.log('🚀 TS Portal Frontend v2.0 시작됨')
console.log('🔗 Kong Gateway:', 'http://localhost:8080')
console.log('📱 Frontend:', 'http://localhost:5174') 