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
            placeholder="회사명, 담당자, 이메일, 계약 타입으로 검색..."
            class="block w-full pl-10 pr-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-teal-500 focus:border-teal-500"
          />
        </div>
      </div>
      <div class="flex items-center space-x-3">
        <select
          :value="selectedStatus"
          @change="$emit('update:selectedStatus', ($event.target as HTMLSelectElement).value)"
          class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-teal-500 focus:border-teal-500"
        >
          <option v-for="option in statusOptions" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
        <div class="text-xs text-gray-500">
          {{ filteredCount }}개 표시
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Props 정의
interface Props {
  searchQuery: string
  selectedStatus: string
  filteredCount: number
}

defineProps<Props>()

// Emits 정의
defineEmits<{
  'update:searchQuery': [value: string]
  'update:selectedStatus': [value: string]
}>()

// 상태 옵션
const statusOptions = [
  { value: 'all', label: '전체', color: 'bg-gray-100 text-gray-800' },
  { value: 'Active', label: '활성', color: 'bg-green-100 text-green-800' },
  { value: 'Inactive', label: '비활성', color: 'bg-gray-100 text-gray-800' },
  { value: 'Expired', label: '만료', color: 'bg-red-100 text-red-800' }
]
</script> 