<template>
  <div 
    :class="[
      'text-center',
      containerClasses[size],
      'bg-white rounded-xl shadow-lg border border-gray-200'
    ]"
  >
    <!-- 로딩 스피너 -->
    <div class="flex items-center justify-center mb-4">
      <LoadingSpinner 
        :size="spinnerSize" 
        :color="spinnerColor" 
      />
    </div>
    
    <!-- 로딩 메시지 -->
    <p :class="messageClasses[size]">
      {{ message }}
    </p>
    
    <!-- 추가 정보 (선택사항) -->
    <p v-if="subtitle" :class="subtitleClasses[size]">
      {{ subtitle }}
    </p>
    
    <!-- 진행률 바 (선택사항) -->
    <div v-if="showProgress && progress !== undefined" class="mt-4">
      <div class="flex justify-between text-sm text-gray-600 mb-2">
        <span>진행률</span>
        <span>{{ Math.round(progress) }}%</span>
      </div>
      <div class="w-full bg-gray-200 rounded-full h-2">
        <div 
          class="h-2 rounded-full transition-all duration-300"
          :class="progressColorClasses[spinnerColor]"
          :style="{ width: `${Math.min(100, Math.max(0, progress))}%` }"
        ></div>
      </div>
    </div>
    
    <!-- 취소 버튼 (선택사항) -->
    <div v-if="cancellable" class="mt-6">
      <button
        @click="$emit('cancel')"
        :class="[
          'px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-colors',
          buttonSizeClasses[size]
        ]"
      >
        취소
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import LoadingSpinner from './LoadingSpinner.vue'

// Props 정의
interface Props {
  message?: string
  subtitle?: string
  size?: 'small' | 'medium' | 'large'
  spinnerColor?: 'white' | 'blue' | 'purple' | 'teal' | 'orange' | 'gray'
  showProgress?: boolean
  progress?: number // 0-100
  cancellable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  message: '로딩 중...',
  size: 'medium',
  spinnerColor: 'blue',
  showProgress: false,
  cancellable: false
})

// Emits 정의
defineEmits<{
  'cancel': []
}>()

// 계산된 스피너 크기
const spinnerSize = computed(() => {
  const sizeMap = {
    small: 'medium',
    medium: 'large',
    large: 'large'
  }
  return sizeMap[props.size] as 'medium' | 'large'
})

// 스타일 클래스들
const containerClasses = {
  small: 'p-6',
  medium: 'p-8',
  large: 'p-12'
}

const messageClasses = {
  small: 'text-sm text-gray-600',
  medium: 'text-base text-gray-600',
  large: 'text-lg text-gray-600'
}

const subtitleClasses = {
  small: 'text-xs text-gray-500 mt-2',
  medium: 'text-sm text-gray-500 mt-2',
  large: 'text-base text-gray-500 mt-3'
}

const buttonSizeClasses = {
  small: 'px-3 py-1.5 text-xs',
  medium: 'px-4 py-2 text-sm',
  large: 'px-6 py-3 text-base'
}

const progressColorClasses = {
  white: 'bg-gray-600',
  blue: 'bg-blue-600',
  purple: 'bg-purple-600',
  teal: 'bg-teal-600',
  orange: 'bg-orange-600',
  gray: 'bg-gray-600'
}
</script> 