<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import authService from '@/services/authService'
import { AppSidebar, AppFooter } from '@/components/layout'

const route = useRoute()
const router = useRouter()
const isSidebarCollapsed = ref(false)

// 현재 사용자 정보를 반응형 ref로 관리
const currentUser = ref(authService.getUser())

// 라우트 변경 시 사용자 정보 업데이트
watch(route, () => {
  const user = authService.getUser()
  currentUser.value = user
  console.log('👤 사용자 정보 업데이트:', user)
}, { immediate: true })

// 컴포넌트 마운트 시 사용자 정보 로드
onMounted(() => {
  currentUser.value = authService.getUser()
})

const toggleSidebarCollapse = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

const logout = () => {
  console.log('🚪 로그아웃 실행')
  authService.logout()
  currentUser.value = null // 즉시 UI 업데이트
  console.log('👤 사용자 정보 초기화:', currentUser.value)
  router.push('/login')
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- 사이드바 -->
    <AppSidebar 
      :is-sidebar-collapsed="isSidebarCollapsed"
      :current-user="currentUser"
      @toggle-sidebar="toggleSidebarCollapse"
      @logout="logout"
    />

    <!-- 메인 컨텐츠 영역 -->
    <div class="flex-1 flex flex-col">
      <!-- 페이지 컨텐츠 -->
      <main class="flex-1 p-4">
        <div class="max-w-7xl mx-auto">
          <RouterView />
        </div>
      </main>

      <!-- 푸터 -->
      <AppFooter />
    </div>
  </div>
</template>

<style scoped>
/* 추가 커스텀 스타일이 필요한 경우 여기에 작성 */
</style>
