<template>
  <!-- 버튼 내부용 작은 스피너 -->
  <svg 
    v-if="size === 'small'" 
    :class="['animate-spin', sizeClasses.small, colorClass]"
    xmlns="http://www.w3.org/2000/svg" 
    fill="none" 
    viewBox="0 0 24 24"
  >
    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
  </svg>

  <!-- 페이지/섹션용 큰 스피너 -->
  <div 
    v-else-if="size === 'large'" 
    :class="['animate-spin rounded-full border-b-2', sizeClasses.large, colorClass]"
  ></div>

  <!-- 중간 크기 스피너 -->
  <svg 
    v-else 
    :class="['animate-spin', sizeClasses.medium, colorClass]"
    fill="none" 
    viewBox="0 0 24 24"
  >
    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
  </svg>
</template>

<script setup lang="ts">
import { computed } from 'vue'

// Props 정의
interface Props {
  size?: 'small' | 'medium' | 'large'
  color?: 'white' | 'blue' | 'purple' | 'teal' | 'orange' | 'gray'
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  size: 'medium',
  color: 'blue'
})

// 크기별 클래스
const sizeClasses = {
  small: 'w-3 h-3 -ml-1 mr-1',
  medium: 'w-5 h-5',
  large: 'w-8 h-8'
}

// 색상별 클래스
const colorClasses = {
  white: 'text-white',
  blue: 'text-blue-600 border-blue-600',
  purple: 'text-purple-600 border-purple-600',
  teal: 'text-teal-600 border-teal-600',
  orange: 'text-orange-600 border-orange-600',
  gray: 'text-gray-600 border-gray-600'
}

// 계산된 색상 클래스
const colorClass = computed(() => {
  const baseClass = colorClasses[props.color]
  return props.className ? `${baseClass} ${props.className}` : baseClass
})
</script> 