<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { customerService } from '../services'
import type { Customer, CustomerStats } from '../types'

// 반응형 상태
const customers = ref<Customer[]>([])
const stats = ref<CustomerStats | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)
const searchQuery = ref('')
const selectedStatus = ref('all')
const selectedMember = ref<Customer | null>(null)
const showCustomerModal = ref(false)
const viewMode = ref<'cards' | 'table'>('table')

// 상태 옵션
const statusOptions = [
  { value: 'all', label: '전체', color: 'bg-gray-100 text-gray-800' },
  { value: 'Active', label: '활성', color: 'bg-green-100 text-green-800' },
  { value: 'Inactive', label: '비활성', color: 'bg-gray-100 text-gray-800' },
  { value: 'Expired', label: '만료', color: 'bg-red-100 text-red-800' }
]

// 계산된 속성
const filteredCustomers = computed(() => {
  let filtered = customers.value

  // 상태 필터
  if (selectedStatus.value !== 'all') {
    filtered = filtered.filter(customer => customer.status === selectedStatus.value)
  }

  // 검색 필터
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(customer =>
      customer.company_name.toLowerCase().includes(query) ||
      customer.contact_person?.toLowerCase().includes(query) ||
      customer.contact_email?.toLowerCase().includes(query) ||
      customer.contract_type?.toLowerCase().includes(query)
    )
  }

  return filtered
})

// 계약 타입별 그룹화
const customersByType = computed(() => {
  const grouped: Record<string, Customer[]> = {}
  
  filteredCustomers.value.forEach(customer => {
    const type = customer.contract_type || '기타'
    if (!grouped[type]) {
      grouped[type] = []
    }
    grouped[type].push(customer)
  })
  
  return grouped
})

// 데이터 로딩 함수
const loadCustomers = async () => {
  try {
    loading.value = true
    error.value = null
    
    const [customersResponse, statsResponse] = await Promise.all([
      customerService.getCustomers({ limit: 1000 }),
      customerService.getCustomerStats()
    ])
    
    customers.value = customersResponse.customers
    stats.value = statsResponse
  } catch (err: any) {
    error.value = err.message || '데이터를 불러오는 중 오류가 발생했습니다.'
    console.error('고객사 데이터 로딩 오류:', err)
  } finally {
    loading.value = false
  }
}

// 고객사 상세 보기
const showCustomerDetail = (customer: Customer) => {
  selectedMember.value = customer
  showCustomerModal.value = true
}

// 고객사 모달 닫기
const closeCustomerModal = () => {
  showCustomerModal.value = false
  selectedMember.value = null
}

// 상태별 색상 반환
const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    'Active': 'bg-green-100 text-green-800',
    'Inactive': 'bg-gray-100 text-gray-800',
    'Expired': 'bg-red-100 text-red-800'
  }
  return colors[status] || 'bg-gray-100 text-gray-800'
}

// 계약 타입별 색상 반환
const getContractTypeColor = (type?: string) => {
  if (!type) return 'bg-gray-100 text-gray-800'
  
  const colors: Record<string, string> = {
    'Full MSP': 'bg-purple-100 text-purple-800',
    'Consulting': 'bg-blue-100 text-blue-800',
    'Support': 'bg-yellow-100 text-yellow-800',
    'Monitoring': 'bg-green-100 text-green-800'
  }
  
  return colors[type] || 'bg-gray-100 text-gray-800'
}

// 계약 만료까지 남은 일수에 따른 색상
const getDaysRemainingColor = (days?: number) => {
  if (!days || days < 0) return 'bg-red-100 text-red-800'
  if (days <= 30) return 'bg-orange-100 text-orange-800'
  if (days <= 90) return 'bg-yellow-100 text-yellow-800'
  return 'bg-green-100 text-green-800'
}

// 날짜 포맷팅
const formatDate = (dateString?: string) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('ko-KR')
}

// 컴포넌트 마운트 시 데이터 로딩
onMounted(() => {
  loadCustomers()
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 컴팩트 헤더 -->
    <div class="bg-white border-b border-gray-200 px-6 py-3">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-xl font-bold text-gray-900">MSP 관리</h1>
          <p class="text-sm text-gray-500">고객사 계약 관리</p>
        </div>
        
        <!-- 컴팩트 통계 -->
        <div class="flex items-center space-x-6">
          <div class="text-center">
            <div class="text-lg font-semibold text-blue-600">{{ stats?.total_customers || 0 }}</div>
            <div class="text-xs text-gray-500">전체</div>
          </div>
          <div class="text-center">
            <div class="text-lg font-semibold text-green-600">{{ stats?.active_customers || 0 }}</div>
            <div class="text-xs text-gray-500">활성</div>
          </div>
          <div class="text-center">
            <div class="text-lg font-semibold text-red-600">{{ stats?.expired_customers || 0 }}</div>
            <div class="text-xs text-gray-500">만료</div>
          </div>
          <div class="text-center">
            <div class="text-lg font-semibold text-yellow-600">{{ stats?.expiring_soon || 0 }}</div>
            <div class="text-xs text-gray-500">만료예정</div>
          </div>
          
          <!-- 뷰 모드 전환 -->
          <div class="flex bg-gray-100 rounded-lg p-1">
            <button
              @click="viewMode = 'cards'"
              :class="`px-2 py-1 rounded-md text-xs font-medium transition-colors ${
                viewMode === 'cards' 
                  ? 'bg-white text-gray-900 shadow-sm' 
                  : 'text-gray-600 hover:text-gray-900'
              }`"
            >
              카드
            </button>
            <button
              @click="viewMode = 'table'"
              :class="`px-2 py-1 rounded-md text-xs font-medium transition-colors ${
                viewMode === 'table' 
                  ? 'bg-white text-gray-900 shadow-sm' 
                  : 'text-gray-600 hover:text-gray-900'
              }`"
            >
              테이블
            </button>
          </div>
          
          <button 
            @click="loadCustomers"
            :disabled="loading"
            class="px-3 py-1.5 bg-teal-600 text-white rounded-md hover:bg-teal-700 disabled:opacity-50 transition-colors text-sm"
          >
            <svg v-if="loading" class="animate-spin -ml-1 mr-1 h-3 w-3 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            새로고침
          </button>
        </div>
      </div>
    </div>

    <!-- 메인 컨텐츠 -->
    <div class="p-6 space-y-6">

    <!-- 검색 및 필터 -->
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
              v-model="searchQuery"
              type="text"
              placeholder="회사명, 담당자, 이메일, 계약 타입으로 검색..."
              class="block w-full pl-10 pr-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-teal-500 focus:border-teal-500"
            />
          </div>
        </div>
        <div class="flex items-center space-x-3">
          <select
            v-model="selectedStatus"
            class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-teal-500 focus:border-teal-500"
          >
            <option v-for="option in statusOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>
          <div class="text-xs text-gray-500">
            {{ filteredCustomers.length }}개 표시
          </div>
        </div>
      </div>
    </div>

    <!-- 에러 메시지 -->
    <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-3">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-4 w-4 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
        </div>
        <div class="ml-3">
          <p class="text-xs text-red-800">{{ error }}</p>
        </div>
      </div>
    </div>

    <!-- 로딩 상태 -->
    <div v-if="loading" class="bg-white rounded-xl shadow-lg border border-gray-200 p-8 text-center">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-600 mx-auto mb-3"></div>
      <p class="text-xs text-gray-600">고객사 정보를 불러오는 중...</p>
    </div>

    <!-- 카드 뷰 -->
    <div v-else-if="viewMode === 'cards' && filteredCustomers.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="customer in filteredCustomers"
        :key="customer.id"
        @click="showCustomerDetail(customer)"
        class="bg-white rounded-xl shadow-lg border border-gray-200 p-4 hover:shadow-xl transition-shadow cursor-pointer"
      >
        <div class="flex items-start justify-between mb-3">
          <div class="flex-1">
            <h3 class="text-sm font-semibold text-gray-900 mb-1">{{ customer.company_name }}</h3>
            <p v-if="customer.contact_person" class="text-xs text-gray-600">{{ customer.contact_person }}</p>
          </div>
          <div class="flex flex-col items-end space-y-1">
            <span :class="`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(customer.status)}`">
              {{ customer.status }}
            </span>
            <span v-if="customer.contract_type" :class="`px-2 py-1 rounded-full text-xs font-medium ${getContractTypeColor(customer.contract_type)}`">
              {{ customer.contract_type }}
            </span>
          </div>
        </div>

        <div class="space-y-1 mb-3">
          <div v-if="customer.contact_email" class="flex items-center text-xs text-gray-600">
            <svg class="w-3 h-3 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
            </svg>
            {{ customer.contact_email }}
          </div>
          <div v-if="customer.contact_phone" class="flex items-center text-xs text-gray-600">
            <svg class="w-3 h-3 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
            </svg>
            {{ customer.contact_phone }}
          </div>
          <div class="flex items-center text-xs text-gray-600">
            <svg class="w-3 h-3 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            {{ formatDate(customer.contract_start) }} ~ {{ formatDate(customer.contract_end) }}
          </div>
        </div>

        <div v-if="customer.contract_days_remaining !== undefined" class="mb-3">
          <span :class="`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getDaysRemainingColor(customer.contract_days_remaining)}`">
            <svg class="w-3 h-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {{ customer.contract_days_remaining > 0 ? `${customer.contract_days_remaining}일 남음` : '만료됨' }}
          </span>
        </div>

        <div v-if="customer.notes" class="text-xs text-gray-600 bg-gray-50 rounded-lg p-2 mb-3">
          {{ customer.notes }}
        </div>

        <div class="flex items-center justify-between">
          <div :class="`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${customer.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`">
            <div :class="`w-2 h-2 rounded-full mr-1 ${customer.is_active ? 'bg-green-400' : 'bg-gray-400'}`"></div>
            {{ customer.is_active ? '활성' : '비활성' }}
          </div>
          <button class="text-teal-600 hover:text-teal-800 text-xs font-medium">
            자세히 보기 →
          </button>
        </div>
      </div>
    </div>

    <!-- 테이블 뷰 -->
    <div v-else-if="viewMode === 'table' && filteredCustomers.length > 0" class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">고객사</th>
              <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">담당자</th>
              <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">계약 타입</th>
              <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">계약 기간</th>
              <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">남은 일수</th>
              <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">상태</th>
              <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">액션</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="customer in filteredCustomers" :key="customer.id" class="hover:bg-gray-50">
              <td class="px-4 py-3 whitespace-nowrap">
                <div class="text-xs font-medium text-gray-900">{{ customer.company_name }}</div>
                <div v-if="customer.contact_email" class="text-xs text-gray-500">{{ customer.contact_email }}</div>
              </td>
              <td class="px-4 py-3 whitespace-nowrap">
                <div class="text-xs text-gray-900">{{ customer.contact_person || '-' }}</div>
                <div v-if="customer.contact_phone" class="text-xs text-gray-500">{{ customer.contact_phone }}</div>
              </td>
              <td class="px-4 py-3 whitespace-nowrap">
                <span v-if="customer.contract_type" :class="`px-2 py-1 rounded-full text-xs font-medium ${getContractTypeColor(customer.contract_type)}`">
                  {{ customer.contract_type }}
                </span>
                <span v-else class="text-xs text-gray-500">-</span>
              </td>
              <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-900">
                <div>{{ formatDate(customer.contract_start) }}</div>
                <div class="text-gray-500">{{ formatDate(customer.contract_end) }}</div>
              </td>
              <td class="px-4 py-3 whitespace-nowrap">
                <span v-if="customer.contract_days_remaining !== undefined" :class="`px-2 py-1 rounded-full text-xs font-medium ${getDaysRemainingColor(customer.contract_days_remaining)}`">
                  {{ customer.contract_days_remaining > 0 ? `${customer.contract_days_remaining}일` : '만료' }}
                </span>
                <span v-else class="text-xs text-gray-500">-</span>
              </td>
              <td class="px-4 py-3 whitespace-nowrap">
                <span :class="`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(customer.status)}`">
                  {{ customer.status }}
                </span>
              </td>
              <td class="px-4 py-3 whitespace-nowrap text-xs font-medium">
                <button @click="showCustomerDetail(customer)" class="text-teal-600 hover:text-teal-900">
                  보기
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 검색 결과 없음 -->
    <div v-else-if="!loading" class="bg-white rounded-xl shadow-lg border border-gray-200 p-12 text-center">
      <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-5 0H9m11 0a2 2 0 01-2 2H7a2 2 0 01-2-2m2-2h2m8 0h2" />
        </svg>
      </div>
      <h2 class="text-xl font-semibold text-gray-900 mb-2">고객사를 찾을 수 없습니다</h2>
      <p class="text-gray-600 mb-4">검색 조건을 변경하거나 필터를 확인해보세요.</p>
    </div>

    <!-- 고객사 상세 모달 -->
    <div v-if="showCustomerModal && selectedMember" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50" @click="closeCustomerModal">
      <div class="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto" @click.stop>
        <div class="p-6">
          <!-- 모달 헤더 -->
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-bold text-gray-900">고객사 상세 정보</h2>
            <button @click="closeCustomerModal" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- 고객사 정보 -->
          <div class="space-y-6">
            <!-- 기본 정보 -->
            <div class="flex items-center space-x-6">
              <div class="w-20 h-20 bg-gradient-to-br from-teal-400 to-teal-600 rounded-full flex items-center justify-center text-white font-bold text-2xl">
                {{ selectedMember.company_name.charAt(0) }}
              </div>
              <div class="flex-1">
                <h3 class="text-2xl font-bold text-gray-900 mb-1">{{ selectedMember.company_name }}</h3>
                <div class="flex items-center space-x-3 mb-2">
                  <span v-if="selectedMember.contract_type" :class="`px-3 py-1 rounded-full text-sm font-medium ${getContractTypeColor(selectedMember.contract_type)}`">
                    {{ selectedMember.contract_type }}
                  </span>
                  <span :class="`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(selectedMember.status)}`">
                    <div :class="`w-2 h-2 rounded-full mr-1 ${selectedMember.is_active ? 'bg-green-400' : 'bg-gray-400'}`"></div>
                    {{ selectedMember.status }}
                  </span>
                </div>
                <p v-if="selectedMember.contact_person" class="text-gray-600">담당자: {{ selectedMember.contact_person }}</p>
              </div>
            </div>

            <!-- 연락처 정보 -->
            <div class="bg-gray-50 rounded-lg p-4">
              <h4 class="font-semibold text-gray-900 mb-3">연락처 정보</h4>
              <div class="space-y-2">
                <div v-if="selectedMember.contact_email" class="flex items-center text-sm">
                  <svg class="w-4 h-4 mr-3 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                  </svg>
                  <span class="text-gray-600">이메일:</span>
                  <span class="ml-2 font-medium">{{ selectedMember.contact_email }}</span>
                </div>
                <div v-if="selectedMember.contact_phone" class="flex items-center text-sm">
                  <svg class="w-4 h-4 mr-3 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                  <span class="text-gray-600">전화번호:</span>
                  <span class="ml-2 font-medium">{{ selectedMember.contact_phone }}</span>
                </div>
              </div>
            </div>

            <!-- 계약 정보 -->
            <div class="bg-gray-50 rounded-lg p-4">
              <h4 class="font-semibold text-gray-900 mb-3">계약 정보</h4>
              <div class="space-y-2">
                <div class="flex items-center text-sm">
                  <svg class="w-4 h-4 mr-3 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <span class="text-gray-600">계약 타입:</span>
                  <span class="ml-2 font-medium">{{ selectedMember.contract_type || '-' }}</span>
                </div>
                <div class="flex items-center text-sm">
                  <svg class="w-4 h-4 mr-3 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span class="text-gray-600">계약 시작:</span>
                  <span class="ml-2 font-medium">{{ formatDate(selectedMember.contract_start) }}</span>
                </div>
                <div class="flex items-center text-sm">
                  <svg class="w-4 h-4 mr-3 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span class="text-gray-600">계약 종료:</span>
                  <span class="ml-2 font-medium">{{ formatDate(selectedMember.contract_end) }}</span>
                </div>
                <div v-if="selectedMember.contract_days_remaining !== undefined" class="flex items-center text-sm">
                  <svg class="w-4 h-4 mr-3 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span class="text-gray-600">남은 일수:</span>
                  <span class="ml-2 font-medium">{{ selectedMember.contract_days_remaining > 0 ? `${selectedMember.contract_days_remaining}일` : '만료됨' }}</span>
                </div>
              </div>
            </div>

            <!-- 메모 -->
            <div v-if="selectedMember.notes">
              <h4 class="font-semibold text-gray-900 mb-3">메모</h4>
              <div class="bg-gray-50 rounded-lg p-4">
                <p class="text-sm text-gray-700">{{ selectedMember.notes }}</p>
              </div>
            </div>
          </div>

          <!-- 모달 푸터 -->
          <div class="mt-8 flex justify-end">
            <button
              @click="closeCustomerModal"
              class="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
            >
              닫기
            </button>
          </div>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<style scoped>
/* 추가 애니메이션 및 스타일 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style> 