/**
 * Customer 관리 Composable
 * 고객사 관련 상태 관리 및 API 호출 로직
 */

import { ref, computed, reactive } from 'vue'
import { customerService, assignmentService } from '@/services/customer'
import type {
  Customer,
  CustomerCreate,
  CustomerUpdate,
  CustomerSearchParams,
  Assignment,
  AssignmentCreate,
  CustomerListResponse,
  CustomerStats
} from '@/types/customer'

export function useCustomer() {
  // 상태 관리
  const customers = ref<Customer[]>([])
  const currentCustomer = ref<Customer | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  
  // 페이지네이션 상태
  const pagination = reactive({
    total: 0,
    skip: 0,
    limit: 20
  })

  // 검색 필터 상태
  const searchParams = reactive<CustomerSearchParams>({
    q: '',
    status: undefined,
    active_only: false,
    contract_type: undefined,
    skip: 0,
    limit: 20
  })

  // 계산된 속성
  const hasCustomers = computed(() => customers.value.length > 0)
  const hasError = computed(() => !!error.value)
  const isLoading = computed(() => loading.value)

  /**
   * 에러 초기화
   */
  const clearError = () => {
    error.value = null
  }

  /**
   * 고객사 목록 조회
   */
  const fetchCustomers = async (params?: CustomerSearchParams) => {
    loading.value = true
    error.value = null
    
    try {
      const searchData = params || searchParams
      const response: CustomerListResponse = await customerService.getCustomers(searchData)
      
      customers.value = response.customers
      pagination.total = response.total
      pagination.skip = searchData.skip || 0
      pagination.limit = searchData.limit || 20
      
      console.log('✅ 고객사 목록 조회 성공:', customers.value.length, '개')
    } catch (err: any) {
      error.value = err.message || '고객사 목록을 불러오는데 실패했습니다.'
      console.error('❌ 고객사 목록 조회 실패:', err)
    } finally {
      loading.value = false
    }
  }

  /**
   * 고객사 상세 정보 조회
   */
  const fetchCustomer = async (id: number) => {
    loading.value = true
    error.value = null
    
    try {
      currentCustomer.value = await customerService.getCustomer(id)
      console.log('✅ 고객사 상세 조회 성공:', currentCustomer.value.company_name)
    } catch (err: any) {
      error.value = err.message || '고객사 정보를 불러오는데 실패했습니다.'
      console.error('❌ 고객사 상세 조회 실패:', err)
    } finally {
      loading.value = false
    }
  }

  /**
   * 고객사 생성
   */
  const createCustomer = async (data: CustomerCreate): Promise<boolean> => {
    loading.value = true
    error.value = null
    
    try {
      const newCustomer = await customerService.createCustomer(data)
      customers.value.unshift(newCustomer)
      console.log('✅ 고객사 생성 성공:', newCustomer.company_name)
      return true
    } catch (err: any) {
      error.value = err.message || '고객사 생성에 실패했습니다.'
      console.error('❌ 고객사 생성 실패:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * 고객사 수정
   */
  const updateCustomer = async (id: number, data: CustomerUpdate): Promise<boolean> => {
    loading.value = true
    error.value = null
    
    try {
      const updatedCustomer = await customerService.updateCustomer(id, data)
      
      // 목록에서 해당 고객사 업데이트
      const index = customers.value.findIndex(c => c.id === id)
      if (index !== -1) {
        customers.value[index] = updatedCustomer
      }
      
      // 현재 고객사가 수정된 고객사인 경우 업데이트
      if (currentCustomer.value?.id === id) {
        currentCustomer.value = updatedCustomer
      }
      
      console.log('✅ 고객사 수정 성공:', updatedCustomer.company_name)
      return true
    } catch (err: any) {
      error.value = err.message || '고객사 수정에 실패했습니다.'
      console.error('❌ 고객사 수정 실패:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * 고객사 삭제 (비활성화)
   */
  const deleteCustomer = async (id: number): Promise<boolean> => {
    loading.value = true
    error.value = null
    
    try {
      await customerService.deleteCustomer(id)
      
      // 목록에서 제거
      customers.value = customers.value.filter(c => c.id !== id)
      
      // 현재 고객사가 삭제된 고객사인 경우 초기화
      if (currentCustomer.value?.id === id) {
        currentCustomer.value = null
      }
      
      console.log('✅ 고객사 삭제 성공')
      return true
    } catch (err: any) {
      error.value = err.message || '고객사 삭제에 실패했습니다.'
      console.error('❌ 고객사 삭제 실패:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * 고객사 검색
   */
  const searchCustomers = async (query: string, activeOnly: boolean = false) => {
    loading.value = true
    error.value = null
    
    try {
      customers.value = await customerService.searchCustomers(query, activeOnly)
      console.log('✅ 고객사 검색 성공:', customers.value.length, '개')
    } catch (err: any) {
      error.value = err.message || '고객사 검색에 실패했습니다.'
      console.error('❌ 고객사 검색 실패:', err)
    } finally {
      loading.value = false
    }
  }

  /**
   * 계약 만료 예정 고객사 조회
   */
  const fetchExpiringCustomers = async (days: number = 30) => {
    loading.value = true
    error.value = null
    
    try {
      customers.value = await customerService.getExpiringCustomers(days)
      console.log('✅ 만료 예정 고객사 조회 성공:', customers.value.length, '개')
    } catch (err: any) {
      error.value = err.message || '만료 예정 고객사 조회에 실패했습니다.'
      console.error('❌ 만료 예정 고객사 조회 실패:', err)
    } finally {
      loading.value = false
    }
  }

  /**
   * 검색 필터 업데이트
   */
  const updateSearchParams = (params: Partial<CustomerSearchParams>) => {
    Object.assign(searchParams, params)
  }

  /**
   * 검색 필터 초기화
   */
  const resetSearchParams = () => {
    searchParams.q = ''
    searchParams.status = undefined
    searchParams.active_only = false
    searchParams.contract_type = undefined
    searchParams.skip = 0
    searchParams.limit = 20
  }

  /**
   * 페이지네이션 다음 페이지
   */
  const nextPage = async () => {
    if (pagination.skip + pagination.limit < pagination.total) {
      searchParams.skip = pagination.skip + pagination.limit
      await fetchCustomers()
    }
  }

  /**
   * 페이지네이션 이전 페이지
   */
  const prevPage = async () => {
    if (pagination.skip > 0) {
      searchParams.skip = Math.max(0, pagination.skip - pagination.limit)
      await fetchCustomers()
    }
  }

  return {
    // 상태
    customers,
    currentCustomer,
    loading,
    error,
    pagination,
    searchParams,
    
    // 계산된 속성
    hasCustomers,
    hasError,
    isLoading,
    
    // 메서드
    clearError,
    fetchCustomers,
    fetchCustomer,
    createCustomer,
    updateCustomer,
    deleteCustomer,
    searchCustomers,
    fetchExpiringCustomers,
    updateSearchParams,
    resetSearchParams,
    nextPage,
    prevPage
  }
}

export function useAssignment() {
  // 상태 관리
  const assignments = ref<Assignment[]>([])
  const currentAssignment = ref<Assignment | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // 계산된 속성
  const hasAssignments = computed(() => assignments.value.length > 0)
  const hasError = computed(() => !!error.value)
  const isLoading = computed(() => loading.value)

  /**
   * 팀원별 담당 고객사 조회
   */
  const fetchAssignmentsByMember = async (memberId: number, activeOnly: boolean = false) => {
    loading.value = true
    error.value = null
    
    try {
      assignments.value = await assignmentService.getAssignmentsByMember(memberId, activeOnly)
      console.log('✅ 팀원별 담당 고객사 조회 성공:', assignments.value.length, '개')
    } catch (err: any) {
      error.value = err.message || '담당 고객사 조회에 실패했습니다.'
      console.error('❌ 팀원별 담당 고객사 조회 실패:', err)
    } finally {
      loading.value = false
    }
  }

  /**
   * 고객사별 담당자 조회
   */
  const fetchAssignmentsByCustomer = async (customerId: number, activeOnly: boolean = false) => {
    loading.value = true
    error.value = null
    
    try {
      assignments.value = await assignmentService.getAssignmentsByCustomer(customerId, activeOnly)
      console.log('✅ 고객사별 담당자 조회 성공:', assignments.value.length, '개')
    } catch (err: any) {
      error.value = err.message || '담당자 조회에 실패했습니다.'
      console.error('❌ 고객사별 담당자 조회 실패:', err)
    } finally {
      loading.value = false
    }
  }

  /**
   * 담당자 배정 생성
   */
  const createAssignment = async (data: AssignmentCreate): Promise<boolean> => {
    loading.value = true
    error.value = null
    
    try {
      const newAssignment = await assignmentService.createAssignment(data)
      assignments.value.unshift(newAssignment)
      console.log('✅ 담당자 배정 성공')
      return true
    } catch (err: any) {
      error.value = err.message || '담당자 배정에 실패했습니다.'
      console.error('❌ 담당자 배정 실패:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    // 상태
    assignments,
    currentAssignment,
    loading,
    error,
    
    // 계산된 속성
    hasAssignments,
    hasError,
    isLoading,
    
    // 메서드
    fetchAssignmentsByMember,
    fetchAssignmentsByCustomer,
    createAssignment
  }
} 