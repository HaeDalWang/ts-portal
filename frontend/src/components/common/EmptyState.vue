<template>
  <div 
    :class="[
      'text-center',
      containerClasses[size],
      'bg-white rounded-xl shadow-lg border border-gray-200'
    ]"
  >
    <!-- 아이콘 -->
    <div class="mx-auto mb-4" :class="iconContainerClasses[size]">
      <slot name="icon">
        <svg 
          :class="iconClasses[size]" 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor"
        >
          <path 
            v-if="icon === 'search'" 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            stroke-width="2" 
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" 
          />
          <path 
            v-else-if="icon === 'users'" 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            stroke-width="2" 
            d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" 
          />
          <path 
            v-else-if="icon === 'document'" 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            stroke-width="2" 
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" 
          />
          <path 
            v-else-if="icon === 'calendar'" 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            stroke-width="2" 
            d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" 
          />
          <path 
            v-else-if="icon === 'folder'" 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            stroke-width="2" 
            d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" 
          />
          <path 
            v-else-if="icon === 'clipboard'" 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            stroke-width="2" 
            d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" 
          />
          <path 
            v-else 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            stroke-width="2" 
            d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2M4 13h2m13-8V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v1M7 8h10l-1 8H8L7 8z" 
          />
        </svg>
      </slot>
    </div>
    
    <!-- 제목 -->
    <h3 :class="titleClasses[size]">
      {{ title }}
    </h3>
    
    <!-- 설명 -->
    <p v-if="description" :class="descriptionClasses[size]">
      {{ description }}
    </p>
    
    <!-- 액션 버튼들 -->
    <div v-if="$slots.actions || actionButton" :class="actionContainerClasses[size]">
      <slot name="actions">
        <button
          v-if="actionButton"
          @click="$emit('action')"
          :class="[
            'font-medium rounded-lg transition-colors',
            buttonClasses[buttonColor],
            buttonSizeClasses[size]
          ]"
        >
          {{ actionButton }}
        </button>
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
// Props 정의
interface Props {
  title: string
  description?: string
  icon?: 'search' | 'users' | 'document' | 'calendar' | 'folder' | 'clipboard' | 'box'
  size?: 'small' | 'medium' | 'large'
  actionButton?: string
  buttonColor?: 'blue' | 'purple' | 'teal' | 'orange' | 'green' | 'gray'
}

const props = withDefaults(defineProps<Props>(), {
  icon: 'box',
  size: 'medium',
  buttonColor: 'blue'
})

// Emits 정의
defineEmits<{
  'action': []
}>()

// 스타일 클래스들
const containerClasses = {
  small: 'p-6',
  medium: 'p-8',
  large: 'p-12'
}

const iconContainerClasses = {
  small: 'w-12 h-12',
  medium: 'w-16 h-16',
  large: 'w-20 h-20'
}

const iconClasses = {
  small: 'w-6 h-6 text-gray-400',
  medium: 'w-8 h-8 text-gray-400',
  large: 'w-10 h-10 text-gray-400'
}

const titleClasses = {
  small: 'text-lg font-semibold text-gray-900 mb-2',
  medium: 'text-xl font-semibold text-gray-900 mb-2',
  large: 'text-2xl font-semibold text-gray-900 mb-3'
}

const descriptionClasses = {
  small: 'text-sm text-gray-600 mb-4',
  medium: 'text-base text-gray-600 mb-4',
  large: 'text-lg text-gray-600 mb-6'
}

const actionContainerClasses = {
  small: 'mt-4',
  medium: 'mt-4',
  large: 'mt-6'
}

const buttonClasses = {
  blue: 'bg-blue-600 hover:bg-blue-700 text-white',
  purple: 'bg-purple-600 hover:bg-purple-700 text-white',
  teal: 'bg-teal-600 hover:bg-teal-700 text-white',
  orange: 'bg-orange-600 hover:bg-orange-700 text-white',
  green: 'bg-green-600 hover:bg-green-700 text-white',
  gray: 'bg-gray-600 hover:bg-gray-700 text-white'
}

const buttonSizeClasses = {
  small: 'px-3 py-2 text-sm',
  medium: 'px-4 py-2 text-sm',
  large: 'px-6 py-3 text-base'
}
</script> 