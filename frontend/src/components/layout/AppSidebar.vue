<template>
  <div
    :class="[
      'bg-white shadow-lg transition-all duration-300 ease-in-out flex flex-col',
      isSidebarCollapsed ? 'w-16' : 'w-52'
    ]"
  >
    <!-- 사이드바 헤더 -->
    <AppHeader 
      :is-sidebar-collapsed="isSidebarCollapsed"
      @toggle-sidebar="toggleSidebarCollapse"
    />

    <!-- 사이드바 네비게이션 -->
    <AppNavigation 
      :is-sidebar-collapsed="isSidebarCollapsed"
      :current-user="currentUser"
      @logout="logout"
    />
  </div>
</template>

<script setup lang="ts">
import AppHeader from './AppHeader.vue'
import AppNavigation from './AppNavigation.vue'

interface Props {
  isSidebarCollapsed: boolean
  currentUser: any
}

interface Emits {
  (event: 'toggle-sidebar'): void
  (event: 'logout'): void
}

defineProps<Props>()
const emit = defineEmits<Emits>()

const toggleSidebarCollapse = () => {
  emit('toggle-sidebar')
}

const logout = () => {
  emit('logout')
}
</script>