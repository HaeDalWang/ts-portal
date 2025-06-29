<template>
  <div 
    v-if="message" 
    :class="[
      'border rounded-lg p-4',
      typeClasses[type],
      sizeClasses[size]
    ]"
  >
    <div class="flex">
      <div class="flex-shrink-0">
        <svg 
          :class="[iconSizeClasses[size], iconColorClasses[type]]" 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor"
        >
          <path 
            v-if="type === 'error'" 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            stroke-width="2" 
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" 
          />
          <path 
            v-else-if="type === 'warning'" 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            stroke-width="2" 
            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" 
          />
          <path 
            v-else-if="type === 'success'" 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            stroke-width="2" 
            d="M5 13l4 4L19 7" 
          />
          <path 
            v-else 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            stroke-width="2" 
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" 
          />
        </svg>
      </div>
      <div class="ml-3 flex-1">
        <h3 v-if="title" :class="['font-semibold', titleColorClasses[type], textSizeClasses[size]]">
          {{ title }}
        </h3>
        <p :class="['mt-1', textColorClasses[type], textSizeClasses[size]]">
          {{ message }}
        </p>
        
        <!-- 액션 버튼 (선택사항) -->
        <div v-if="$slots.actions || retryAction" class="mt-4">
          <slot name="actions">
            <button
              v-if="retryAction"
              @click="$emit('retry')"
              :class="[
                'font-medium rounded-lg transition-colors',
                buttonClasses[type],
                buttonSizeClasses[size]
              ]"
            >
              다시 시도
            </button>
          </slot>
        </div>
      </div>
      
      <!-- 닫기 버튼 (선택사항) -->
      <div v-if="dismissible" class="ml-auto pl-3">
        <button
          @click="$emit('dismiss')"
          :class="['inline-flex rounded-md p-1.5 focus:outline-none focus:ring-2 focus:ring-offset-2', dismissButtonClasses[type]]"
        >
          <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Props 정의
interface Props {
  message: string
  title?: string
  type?: 'error' | 'warning' | 'success' | 'info'
  size?: 'small' | 'medium' | 'large'
  dismissible?: boolean
  retryAction?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  type: 'error',
  size: 'medium',
  dismissible: false,
  retryAction: false
})

// Emits 정의
defineEmits<{
  'dismiss': []
  'retry': []
}>()

// 스타일 클래스들
const typeClasses = {
  error: 'bg-red-50 border-red-200',
  warning: 'bg-yellow-50 border-yellow-200',
  success: 'bg-green-50 border-green-200',
  info: 'bg-blue-50 border-blue-200'
}

const sizeClasses = {
  small: 'p-3',
  medium: 'p-4',
  large: 'p-6'
}

const iconSizeClasses = {
  small: 'h-4 w-4',
  medium: 'h-5 w-5',
  large: 'h-6 w-6'
}

const iconColorClasses = {
  error: 'text-red-400',
  warning: 'text-yellow-400',
  success: 'text-green-400',
  info: 'text-blue-400'
}

const titleColorClasses = {
  error: 'text-red-800',
  warning: 'text-yellow-800',
  success: 'text-green-800',
  info: 'text-blue-800'
}

const textColorClasses = {
  error: 'text-red-700',
  warning: 'text-yellow-700',
  success: 'text-green-700',
  info: 'text-blue-700'
}

const textSizeClasses = {
  small: 'text-xs',
  medium: 'text-sm',
  large: 'text-base'
}

const buttonClasses = {
  error: 'bg-red-600 hover:bg-red-700 text-white',
  warning: 'bg-yellow-600 hover:bg-yellow-700 text-white',
  success: 'bg-green-600 hover:bg-green-700 text-white',
  info: 'bg-blue-600 hover:bg-blue-700 text-white'
}

const buttonSizeClasses = {
  small: 'px-2 py-1 text-xs',
  medium: 'px-3 py-2 text-sm',
  large: 'px-4 py-2 text-base'
}

const dismissButtonClasses = {
  error: 'text-red-500 hover:bg-red-100 focus:ring-red-600',
  warning: 'text-yellow-500 hover:bg-yellow-100 focus:ring-yellow-600',
  success: 'text-green-500 hover:bg-green-100 focus:ring-green-600',
  info: 'text-blue-500 hover:bg-blue-100 focus:ring-blue-600'
}
</script> 