<template>
  <div :class="['flex items-center h-16 border-b border-gray-200', isSidebarCollapsed ? 'justify-center px-2' : 'justify-between px-4']">
    <!-- TS 로고 (펼쳐진 상태에서만 표시) -->
    <div v-if="!isSidebarCollapsed" class="flex items-center">
      <div 
        :class="[
          'flex items-center justify-center font-bold text-white rounded-lg shadow-md transition-all duration-300',
          'bg-gradient-to-br from-blue-500 to-blue-600',
          'w-8 h-8 text-xs'
        ]"
      >
        TS
      </div>
    </div>

    <!-- 접기/펴기 버튼 (펼쳐진 상태) -->
    <button
      v-if="!isSidebarCollapsed"
      @click="toggleSidebarCollapse"
      :class="[
        'p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 transition-colors'
      ]"
    >
      <svg 
        :class="[
          'w-5 h-5 transition-transform duration-300'
        ]" 
        fill="none" 
        viewBox="0 0 24 24" 
        stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
      </svg>
    </button>
    
    <!-- 펼치기 버튼 (접힌 상태) -->
    <button
      v-if="isSidebarCollapsed"
      @click="toggleSidebarCollapse"
      class="w-full h-full flex items-center justify-center hover:bg-gray-50 transition-colors"
    >
      <svg 
        class="w-4 h-4 text-gray-400" 
        fill="none" 
        viewBox="0 0 24 24" 
        stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7" />
      </svg>
    </button>
  </div>
</template>

<script setup lang="ts">
interface Props {
  isSidebarCollapsed: boolean
}

interface Emits {
  (event: 'toggle-sidebar'): void
}

defineProps<Props>()
const emit = defineEmits<Emits>()

const toggleSidebarCollapse = () => {
  emit('toggle-sidebar')
}
</script> 