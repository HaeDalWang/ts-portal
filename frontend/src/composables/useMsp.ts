import { ref, computed, onMounted } from 'vue'
import { customerService, memberService } from '@/services'
import type { Customer, CustomerStats, CustomerCreate, CustomerUpdate, Member } from '@/types'

export function useMsp() {
  // 반응형 상태
  const customers = ref<Customer[]>([])
  const stats = ref<CustomerStats | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const searchQuery = ref('')
  const selectedStatus = ref('all')
  const viewMode = ref<'cards' | 'table'>('table')

  // 모달 상태
  const selectedCustomer = ref<Customer | null>(null)
  const showCustomerModal = ref(false)
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
    main_assignee_id: null,
    sub_assignee_id: null,
    contact_email: '',
    contact_phone: '',
    support_level: '',
    contract_start: '',
    contract_end: '',
    notes: '',
    status: 'Active'
  })

  const editForm = ref<CustomerUpdate>({
    company_name: '',
    contact_email: '',
    contact_phone: '',
    support_level: '',
    contract_start: '',
    contract_end: '',
    status: '',
    notes: ''
  })

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
        customer.contact_email?.toLowerCase().includes(query) ||
        customer.support_level?.toLowerCase().includes(query)
      )
    }

    return filtered
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
    selectedCustomer.value = customer
    showCustomerModal.value = true
  }

  // 고객사 모달 닫기
  const closeCustomerModal = () => {
    showCustomerModal.value = false
    selectedCustomer.value = null
  }

  // 새 고객사 추가 모달 열기
  const openCreateModal = () => {
    createForm.value = {
      company_name: '',
      main_assignee_id: null,
      sub_assignee_id: null,
      contact_email: '',
      contact_phone: '',
      support_level: '',
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
      contact_email: customer.contact_email || '',
      contact_phone: customer.contact_phone || '',
      support_level: customer.support_level || '',
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
      
      return { success: true, message: '새 고객사가 성공적으로 등록되었습니다.' }
    } catch (err: any) {
      error.value = err.message || '고객사 등록 중 오류가 발생했습니다.'
      return { success: false, message: err.message || '고객사 등록 중 오류가 발생했습니다.' }
    } finally {
      formLoading.value = false
    }
  }

  // 고객사 정보 수정
  const updateCustomer = async () => {
    if (!editingCustomer.value) return { success: false, message: '수정할 고객사가 선택되지 않았습니다.' }
    
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
      
      return { success: true, message: '고객사 정보가 성공적으로 수정되었습니다.' }
    } catch (err: any) {
      error.value = err.message || '고객사 수정 중 오류가 발생했습니다.'
      return { success: false, message: err.message || '고객사 수정 중 오류가 발생했습니다.' }
    } finally {
      formLoading.value = false
    }
  }

  // 담당팀원 할당
  const assignMember = async () => {
    if (!assigningCustomer.value || !selectedAssigneeId.value) return { success: false, message: '할당 정보가 부족합니다.' }
    
    try {
      formLoading.value = true
      error.value = null
      
      const selectedMember = availableMembers.value.find(m => m.id === selectedAssigneeId.value)
      if (!selectedMember) return { success: false, message: '선택된 팀원을 찾을 수 없습니다.' }
      
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
      
      return { success: true, message: `${selectedMember.name}님이 담당자로 할당되었습니다.` }
    } catch (err: any) {
      error.value = err.message || '담당팀원 할당 중 오류가 발생했습니다.'
      return { success: false, message: err.message || '담당팀원 할당 중 오류가 발생했습니다.' }
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

  // 컴포넌트 마운트 시 데이터 로딩
  onMounted(() => {
    loadCustomers()
  })

  return {
    // 상태
    customers,
    stats,
    loading,
    error,
    searchQuery,
    selectedStatus,
    viewMode,
    selectedCustomer,
    showCustomerModal,
    showCreateModal,
    showEditModal,
    showAssignModal,
    editingCustomer,
    assigningCustomer,
    availableMembers,
    selectedAssigneeId,
    formLoading,
    successMessage,
    createForm,
    editForm,
    filteredCustomers,
    
    // 메서드
    loadCustomers,
    loadMembers,
    showCustomerDetail,
    closeCustomerModal,
    openCreateModal,
    openEditModal,
    openAssignModal,
    createCustomer,
    updateCustomer,
    assignMember,
    closeCreateModal,
    closeEditModal,
    closeAssignModal
  }
} 