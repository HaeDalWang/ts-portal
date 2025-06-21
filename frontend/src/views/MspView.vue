<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { customerService, memberService } from '../services'
import type { Customer, CustomerStats, CustomerCreate, CustomerUpdate, Member } from '../types'

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

// 새로운 상태들 추가
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showAssignModal = ref(false)
const editingCustomer = ref<Customer | null>(null)
const assigningCustomer = ref<Customer | null>(null)
const availableMembers = ref<Member[]>([])
const selectedAssigneeId = ref<number | null>(null)
const formLoading = ref(false)
const successMessage = ref<string | null>(null)

// 폼 데이터
const createForm = ref<CustomerCreate>({
  company_name: '',
  contact_person: '',
  contact_email: '',
  contact_phone: '',
  contract_type: '',
  contract_start: '',
  contract_end: '',
  notes: '',
  status: 'Active'
})

const editForm = ref<CustomerUpdate>({
  company_name: '',
  contact_person: '',
  contact_email: '',
  contact_phone: '',
  contract_type: '',
  contract_start: '',
  contract_end: '',
  status: '',
  notes: ''
})

// 상태 옵션
const statusOptions = [
  { value: 'all', label: '전체', color: 'bg-gray-100 text-gray-800' },
  { value: 'Active', label: '활성', color: 'bg-green-100 text-green-800' },
  { value: 'Inactive', label: '비활성', color: 'bg-gray-100 text-gray-800' },
  { value: 'Expired', label: '만료', color: 'bg-red-100 text-red-800' }
]

// 계약 타입 옵션
const contractTypeOptions = [
  'Full MSP',
  'Consulting',
  'Support',
  'Monitoring',
  'Development',
  'Maintenance'
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

// 팀원 목록 로딩
const loadMembers = async () => {
  try {
    availableMembers.value = await memberService.getActiveMembers()
  } catch (err: any) {
    console.error('팀원 목록 로딩 오류:', err)
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

// 새 고객사 추가 모달 열기
const openCreateModal = () => {
  createForm.value = {
    company_name: '',
    contact_person: '',
    contact_email: '',
    contact_phone: '',
    contract_type: '',
    contract_start: '',
    contract_end: '',
    notes: '',
    status: 'Active'
  }
  showCreateModal.value = true
}

// 고객사 수정 모달 열기
const openEditModal = (customer: Customer) => {
  editingCustomer.value = customer
  editForm.value = {
    company_name: customer.company_name,
    contact_person: customer.contact_person || '',
    contact_email: customer.contact_email || '',
    contact_phone: customer.contact_phone || '',
    contract_type: customer.contract_type || '',
    contract_start: customer.contract_start || '',
    contract_end: customer.contract_end || '',
    status: customer.status,
    notes: customer.notes || ''
  }
  showEditModal.value = true
}

// 담당팀원 할당 모달 열기
const openAssignModal = (customer: Customer) => {
  assigningCustomer.value = customer
  selectedAssigneeId.value = null
  showAssignModal.value = true
  loadMembers()
}

// 새 고객사 생성
const createCustomer = async () => {
  try {
    formLoading.value = true
    error.value = null
    
    await customerService.createCustomer(createForm.value)
    
    successMessage.value = '새 고객사가 성공적으로 등록되었습니다.'
    showCreateModal.value = false
    await loadCustomers()
    
    setTimeout(() => {
      successMessage.value = null
    }, 3000)
  } catch (err: any) {
    error.value = err.message || '고객사 등록 중 오류가 발생했습니다.'
  } finally {
    formLoading.value = false
  }
}

// 고객사 정보 수정
const updateCustomer = async () => {
  if (!editingCustomer.value) return
  
  try {
    formLoading.value = true
    error.value = null
    
    await customerService.updateCustomer(editingCustomer.value.id, editForm.value)
    
    successMessage.value = '고객사 정보가 성공적으로 수정되었습니다.'
    showEditModal.value = false
    editingCustomer.value = null
    await loadCustomers()
    
    setTimeout(() => {
      successMessage.value = null
    }, 3000)
  } catch (err: any) {
    error.value = err.message || '고객사 수정 중 오류가 발생했습니다.'
  } finally {
    formLoading.value = false
  }
}

// 담당팀원 할당 (메모 필드에 저장)
const assignMember = async () => {
  if (!assigningCustomer.value || !selectedAssigneeId.value) return
  
  try {
    formLoading.value = true
    error.value = null
    
    const selectedMember = availableMembers.value.find(m => m.id === selectedAssigneeId.value)
    if (!selectedMember) return
    
    const currentNotes = assigningCustomer.value.notes || ''
    const memberInfo = `담당자: ${selectedMember.name} (${selectedMember.email})`
    
    // 기존 담당자 정보 제거하고 새로운 담당자 정보 추가
    const notesWithoutAssignee = currentNotes.replace(/담당자:.*?\n?/g, '').trim()
    const updatedNotes = notesWithoutAssignee ? `${memberInfo}\n${notesWithoutAssignee}` : memberInfo
    
    await customerService.updateCustomer(assigningCustomer.value.id, {
      notes: updatedNotes
    })
    
    successMessage.value = `${selectedMember.name}님이 ${assigningCustomer.value.company_name}의 담당자로 할당되었습니다.`
    showAssignModal.value = false
    assigningCustomer.value = null
    selectedAssigneeId.value = null
    await loadCustomers()
    
    setTimeout(() => {
      successMessage.value = null
    }, 3000)
  } catch (err: any) {
    error.value = err.message || '담당팀원 할당 중 오류가 발생했습니다.'
  } finally {
    formLoading.value = false
  }
}

// 모달 닫기 함수들
const closeCreateModal = () => {
  showCreateModal.value = false
}

const closeEditModal = () => {
  showEditModal.value = false
  editingCustomer.value = null
}

const closeAssignModal = () => {
  showAssignModal.value = false
  assigningCustomer.value = null
  selectedAssigneeId.value = null
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

// 날짜 입력 포맷팅 (YYYY-MM-DD)
const formatDateForInput = (dateString?: string | null) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toISOString().split('T')[0]
}

// 컴포넌트 마운트 시 데이터 로딩
onMounted(() => {
  loadCustomers()
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 성공 메시지 -->
    <div v-if="successMessage" class="fixed top-4 right-4 z-50 bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded-lg shadow-lg">
      <div class="flex items-center">
        <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        {{ successMessage }}
      </div>
    </div>

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
          
          <!-- 액션 버튼들 -->
          <div class="flex items-center space-x-2">
            <button 
              @click="openCreateModal"
              class="px-3 py-1.5 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors text-sm font-medium flex items-center space-x-1"
            >
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              <span>새 고객사</span>
            </button>
            
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
        class="bg-white rounded-xl shadow-lg border border-gray-200 p-4 hover:shadow-xl transition-shadow"
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

        <!-- 카드 액션 버튼들 -->
        <div class="flex items-center justify-between space-x-2">
          <div :class="`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${customer.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`">
            <div :class="`w-2 h-2 rounded-full mr-1 ${customer.is_active ? 'bg-green-400' : 'bg-gray-400'}`"></div>
            {{ customer.is_active ? '활성' : '비활성' }}
          </div>
          <div class="flex items-center space-x-1">
            <button 
              @click="showCustomerDetail(customer)" 
              class="text-teal-600 hover:text-teal-800 text-xs font-medium px-2 py-1 rounded hover:bg-teal-50"
            >
              보기
            </button>
            <button 
              @click="openEditModal(customer)" 
              class="text-blue-600 hover:text-blue-800 text-xs font-medium px-2 py-1 rounded hover:bg-blue-50"
            >
              수정
            </button>
            <button 
              @click="openAssignModal(customer)" 
              class="text-purple-600 hover:text-purple-800 text-xs font-medium px-2 py-1 rounded hover:bg-purple-50"
            >
              할당
            </button>
          </div>
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
                <div class="flex items-center space-x-2">
                  <button @click="showCustomerDetail(customer)" class="text-teal-600 hover:text-teal-900">
                    보기
                  </button>
                  <button @click="openEditModal(customer)" class="text-blue-600 hover:text-blue-900">
                    수정
                  </button>
                  <button @click="openAssignModal(customer)" class="text-purple-600 hover:text-purple-900">
                    할당
                  </button>
                </div>
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
      <button 
        @click="openCreateModal"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
      >
        첫 번째 고객사 추가하기
      </button>
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

    <!-- 새 고객사 추가 모달 -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50" @click="closeCreateModal">
      <div class="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto" @click.stop>
        <div class="p-6">
          <!-- 모달 헤더 -->
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-bold text-gray-900">새 고객사 등록</h2>
            <button @click="closeCreateModal" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- 폼 -->
          <form @submit.prevent="createCustomer" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-2">회사명 *</label>
                <input
                  v-model="createForm.company_name"
                  type="text"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                  placeholder="회사명을 입력하세요"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">담당자명</label>
                <input
                  v-model="createForm.contact_person"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                  placeholder="담당자명"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">이메일</label>
                <input
                  v-model="createForm.contact_email"
                  type="email"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                  placeholder="이메일 주소"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">전화번호</label>
                <input
                  v-model="createForm.contact_phone"
                  type="tel"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                  placeholder="전화번호"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">계약 타입</label>
                <select
                  v-model="createForm.contract_type"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="">계약 타입 선택</option>
                  <option v-for="type in contractTypeOptions" :key="type" :value="type">
                    {{ type }}
                  </option>
                </select>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">계약 시작일</label>
                <input
                  v-model="createForm.contract_start"
                  type="date"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">계약 종료일</label>
                <input
                  v-model="createForm.contract_end"
                  type="date"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">상태</label>
                <select
                  v-model="createForm.status"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="Active">활성</option>
                  <option value="Inactive">비활성</option>
                  <option value="Expired">만료</option>
                </select>
              </div>
              
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-2">메모</label>
                <textarea
                  v-model="createForm.notes"
                  rows="3"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                  placeholder="특이사항이나 메모를 입력하세요"
                ></textarea>
              </div>
            </div>

            <!-- 모달 푸터 -->
            <div class="flex justify-end space-x-3 pt-6 border-t">
              <button
                type="button"
                @click="closeCreateModal"
                class="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
              >
                취소
              </button>
              <button
                type="submit"
                :disabled="formLoading || !createForm.company_name"
                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                <span v-if="formLoading">등록 중...</span>
                <span v-else>등록</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- 고객사 수정 모달 -->
    <div v-if="showEditModal && editingCustomer" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50" @click="closeEditModal">
      <div class="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto" @click.stop>
        <div class="p-6">
          <!-- 모달 헤더 -->
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-bold text-gray-900">고객사 정보 수정</h2>
            <button @click="closeEditModal" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- 폼 -->
          <form @submit.prevent="updateCustomer" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-2">회사명 *</label>
                <input
                  v-model="editForm.company_name"
                  type="text"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                  placeholder="회사명을 입력하세요"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">담당자명</label>
                <input
                  v-model="editForm.contact_person"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                  placeholder="담당자명"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">이메일</label>
                <input
                  v-model="editForm.contact_email"
                  type="email"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                  placeholder="이메일 주소"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">전화번호</label>
                <input
                  v-model="editForm.contact_phone"
                  type="tel"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                  placeholder="전화번호"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">계약 타입</label>
                <select
                  v-model="editForm.contract_type"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="">계약 타입 선택</option>
                  <option v-for="type in contractTypeOptions" :key="type" :value="type">
                    {{ type }}
                  </option>
                </select>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">계약 시작일</label>
                <input
                  v-model="editForm.contract_start"
                  type="date"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">계약 종료일</label>
                <input
                  v-model="editForm.contract_end"
                  type="date"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">상태</label>
                <select
                  v-model="editForm.status"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="Active">활성</option>
                  <option value="Inactive">비활성</option>
                  <option value="Expired">만료</option>
                </select>
              </div>
              
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-2">메모</label>
                <textarea
                  v-model="editForm.notes"
                  rows="3"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                  placeholder="특이사항이나 메모를 입력하세요"
                ></textarea>
              </div>
            </div>

            <!-- 모달 푸터 -->
            <div class="flex justify-end space-x-3 pt-6 border-t">
              <button
                type="button"
                @click="closeEditModal"
                class="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
              >
                취소
              </button>
              <button
                type="submit"
                :disabled="formLoading || !editForm.company_name"
                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                <span v-if="formLoading">수정 중...</span>
                <span v-else>수정</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- 담당팀원 할당 모달 -->
    <div v-if="showAssignModal && assigningCustomer" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50" @click="closeAssignModal">
      <div class="bg-white rounded-xl shadow-2xl max-w-lg w-full" @click.stop>
        <div class="p-6">
          <!-- 모달 헤더 -->
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-xl font-bold text-gray-900">담당팀원 할당</h2>
            <button @click="closeAssignModal" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- 고객사 정보 -->
          <div class="bg-gray-50 rounded-lg p-4 mb-6">
            <h3 class="font-semibold text-gray-900 mb-2">{{ assigningCustomer.company_name }}</h3>
            <p class="text-sm text-gray-600">{{ assigningCustomer.contact_person || '담당자 미등록' }}</p>
          </div>

          <!-- 팀원 선택 -->
          <form @submit.prevent="assignMember" class="space-y-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">담당팀원 선택 *</label>
              <select
                v-model="selectedAssigneeId"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-purple-500 focus:border-purple-500"
              >
                <option value="">팀원을 선택하세요</option>
                <option v-for="member in availableMembers" :key="member.id" :value="member.id">
                  {{ member.name }} ({{ member.team }}) - {{ member.position || '직책 미등록' }}
                </option>
              </select>
            </div>

            <!-- 선택된 팀원 정보 -->
            <div v-if="selectedAssigneeId" class="bg-purple-50 rounded-lg p-4">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-purple-600 rounded-full flex items-center justify-center text-white font-bold">
                  {{ availableMembers.find(m => m.id === selectedAssigneeId)?.name.charAt(0) }}
                </div>
                <div>
                  <p class="font-medium text-gray-900">{{ availableMembers.find(m => m.id === selectedAssigneeId)?.name }}</p>
                  <p class="text-sm text-gray-600">{{ availableMembers.find(m => m.id === selectedAssigneeId)?.email }}</p>
                </div>
              </div>
            </div>

            <!-- 모달 푸터 -->
            <div class="flex justify-end space-x-3 pt-6 border-t">
              <button
                type="button"
                @click="closeAssignModal"
                class="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
              >
                취소
              </button>
              <button
                type="submit"
                :disabled="formLoading || !selectedAssigneeId"
                class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 transition-colors"
              >
                <span v-if="formLoading">할당 중...</span>
                <span v-else>할당</span>
              </button>
            </div>
          </form>
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