<template>
  <Teleport to="body">
    <Transition
      enter-active-class="duration-300 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="duration-200 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div 
        v-if="show" 
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
        @click="handleBackdropClick"
      >
        <Transition
          enter-active-class="duration-300 ease-out"
          enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100"
          leave-active-class="duration-200 ease-in"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
        >
          <div 
            v-if="show"
            :class="[
              'bg-white rounded-lg shadow-xl mx-4 overflow-hidden',
              sizeClasses[size],
              maxHeightClasses[maxHeight]
            ]"
            @click.stop
          >
            <!-- 모달 헤더 -->
            <div 
              v-if="$slots.header || title"
              :class="[
                'px-6 py-4 border-b border-gray-200',
                headerBgClasses[headerStyle]
              ]"
            >
              <slot name="header">
                <div class="flex items-center justify-between">
                  <div>
                    <h3 :class="titleClasses[size]">
                      {{ title }}
                    </h3>
                    <p v-if="subtitle" :class="subtitleClasses[size]">
                      {{ subtitle }}
                    </p>
                  </div>
                  <button
                    v-if="closable"
                    @click="$emit('close')"
                    class="text-gray-400 hover:text-gray-600 transition-colors focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 rounded-md p-1"
                  >
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </slot>
            </div>

            <!-- 모달 본문 -->
            <div 
              :class="[
                'overflow-y-auto',
                contentClasses[size],
                contentMaxHeight[maxHeight]
              ]"
            >
              <slot />
            </div>

            <!-- 모달 푸터 -->
            <div 
              v-if="$slots.footer"
              :class="[
                'px-6 py-4 border-t border-gray-200',
                footerBgClasses[footerStyle]
              ]"
            >
              <slot name="footer" />
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
// Props 정의
interface Props {
  show: boolean
  title?: string
  subtitle?: string
  size?: 'small' | 'medium' | 'large' | 'xlarge'
  maxHeight?: 'auto' | 'screen' | 'half'
  closable?: boolean
  closeOnBackdrop?: boolean
  headerStyle?: 'default' | 'colored'
  footerStyle?: 'default' | 'colored'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'medium',
  maxHeight: 'auto',
  closable: true,
  closeOnBackdrop: true,
  headerStyle: 'default',
  footerStyle: 'default'
})

// Emits 정의
const $emit = defineEmits<{
  'close': []
}>()

// 백드롭 클릭 핸들러
const handleBackdropClick = () => {
  if (props.closeOnBackdrop) {
    $emit('close')
  }
}

// 스타일 클래스들
const sizeClasses = {
  small: 'max-w-md w-full',
  medium: 'max-w-2xl w-full',
  large: 'max-w-4xl w-full',
  xlarge: 'max-w-6xl w-full'
}

const maxHeightClasses = {
  auto: '',
  screen: 'max-h-[90vh]',
  half: 'max-h-[50vh]'
}

const contentClasses = {
  small: 'px-6 py-4',
  medium: 'px-6 py-4',
  large: 'px-6 py-6',
  xlarge: 'px-8 py-6'
}

const contentMaxHeight = {
  auto: '',
  screen: 'max-h-[60vh]',
  half: 'max-h-[30vh]'
}

const titleClasses = {
  small: 'text-lg font-semibold text-gray-900',
  medium: 'text-lg font-semibold text-gray-900',
  large: 'text-xl font-semibold text-gray-900',
  xlarge: 'text-2xl font-semibold text-gray-900'
}

const subtitleClasses = {
  small: 'text-sm text-gray-500',
  medium: 'text-sm text-gray-500',
  large: 'text-base text-gray-500',
  xlarge: 'text-base text-gray-500'
}

const headerBgClasses = {
  default: 'bg-gray-50',
  colored: 'bg-white'
}

const footerBgClasses = {
  default: 'bg-gray-50',
  colored: 'bg-white'
}
</script> 