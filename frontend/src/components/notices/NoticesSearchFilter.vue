<template>
  <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-4">
    <div class="flex flex-col md:flex-row gap-3">
      <div class="flex-1">
        <div class="relative">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <input
            :value="searchQuery"
            @input="$emit('update:searchQuery', ($event.target as HTMLInputElement).value)"
            type="text"
            class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 text-sm"
            placeholder="공지사항 검색..."
          />
        </div>
      </div>
      
      <div class="flex flex-col sm:flex-row gap-2">
        <select
          :value="selectedPriority"
          @change="$emit('update:selectedPriority', ($event.target as HTMLSelectElement).value)"
          class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 text-sm"
        >
          <option v-for="option in priorityOptions" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
        
        <label class="inline-flex items-center px-3 py-2 border border-gray-300 rounded-md cursor-pointer hover:bg-gray-50">
          <input
            :checked="showPinnedOnly"
            @change="$emit('update:showPinnedOnly', ($event.target as HTMLInputElement).checked)"
            type="checkbox"
            class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
          />
          <span class="ml-2 text-sm text-gray-700">고정 공지만</span>
        </label>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Props 정의
interface Props {
  searchQuery: string
  selectedPriority: string
  showPinnedOnly: boolean
}

defineProps<Props>()

// Emits 정의
defineEmits<{
  'update:searchQuery': [value: string]
  'update:selectedPriority': [value: string]
  'update:showPinnedOnly': [value: boolean]
}>()

// 우선순위 옵션
const priorityOptions = [
  { value: 'all', label: '전체', color: 'bg-gray-100 text-gray-800', icon: '📋' },
  { value: 'important', label: '중요', color: 'bg-red-100 text-red-800', icon: '🚨' },
  { value: 'caution', label: '주의', color: 'bg-yellow-100 text-yellow-800', icon: '⚠️' },
  { value: 'normal', label: '일반', color: 'bg-blue-100 text-blue-800', icon: '📢' }
]
</script> 