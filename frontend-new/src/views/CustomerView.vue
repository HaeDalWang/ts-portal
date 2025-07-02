<template>
  <div class="customer-view">
    <div class="container">
      <header class="page-header">
        <h1>🏢 고객사 관리</h1>
        <p class="page-subtitle">Customer Service API 연동 테스트</p>
      </header>
      
      <!-- 검색 및 필터 -->
      <div class="search-section">
        <div class="search-controls">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="고객사명 검색..." 
            @keyup.enter="handleSearch"
            class="search-input"
          />
          <button @click="handleSearch" :disabled="isLoading" class="btn-search">
            검색
          </button>
          <button @click="showCreateForm = true" class="btn-create">
            + 새 고객사
          </button>
        </div>
        
        <div class="filter-controls">
          <select v-model="selectedStatus" @change="handleSearch" class="filter-select">
            <option value="">전체 상태</option>
            <option value="Active">활성</option>
            <option value="Pending">대기</option>
            <option value="Expired">만료</option>
            <option value="Suspended">중단</option>
          </select>
          
          <label class="filter-checkbox">
            <input type="checkbox" v-model="activeOnly" @change="handleSearch" />
            활성 고객사만
          </label>
        </div>
      </div>

      <!-- 로딩 상태 -->
      <div v-if="isLoading" class="loading-section">
        <p>🔄 고객사 정보를 불러오는 중...</p>
      </div>

      <!-- 에러 상태 -->
      <div v-if="hasError" class="error-section">
        <p>❌ {{ error }}</p>
        <button @click="clearError" class="btn-clear">확인</button>
      </div>

      <!-- 고객사 목록 -->
      <div v-if="!isLoading && hasCustomers" class="customer-list">
        <div class="list-header">
          <h2>고객사 목록 ({{ pagination.total }}개)</h2>
        </div>
        
        <div class="customer-table">
          <div class="table-header">
            <div class="col-company">고객사명</div>
            <div class="col-contact">담당자</div>
            <div class="col-status">상태</div>
            <div class="col-contract">계약기간</div>
            <div class="col-actions">작업</div>
          </div>
          
          <div 
            v-for="customer in customers" 
            :key="customer.id" 
            class="table-row"
          >
            <div class="col-company">
              <strong>{{ customer.company_name }}</strong>
              <small v-if="customer.contact_email">{{ customer.contact_email }}</small>
            </div>
            <div class="col-contact">
              {{ customer.contact_person || '-' }}
            </div>
            <div class="col-status">
              <span :class="['status-badge', `status-${customer.status?.toLowerCase()}`]">
                {{ customer.status }}
              </span>
            </div>
            <div class="col-contract">
              <div v-if="customer.contract_start && customer.contract_end">
                {{ formatDate(customer.contract_start) }} ~ {{ formatDate(customer.contract_end) }}
              </div>
              <div v-else>-</div>
            </div>
            <div class="col-actions">
              <button @click="viewCustomer(customer)" class="btn-action">보기</button>
              <button @click="editCustomer(customer)" class="btn-action">수정</button>
              <button @click="deleteCustomerConfirm(customer)" class="btn-danger">삭제</button>
            </div>
          </div>
        </div>

        <!-- 페이지네이션 -->
        <div class="pagination" v-if="pagination.total > pagination.limit">
          <button @click="prevPage" :disabled="pagination.skip === 0" class="btn-page">이전</button>
          <span class="page-info">
            {{ pagination.skip + 1 }} - {{ Math.min(pagination.skip + pagination.limit, pagination.total) }} 
            / {{ pagination.total }}
          </span>
          <button @click="nextPage" :disabled="pagination.skip + pagination.limit >= pagination.total" class="btn-page">다음</button>
        </div>
      </div>

      <!-- 고객사 없음 -->
      <div v-if="!isLoading && !hasCustomers && !hasError" class="empty-section">
        <p>📭 등록된 고객사가 없습니다.</p>
        <button @click="showCreateForm = true" class="btn-create">첫 고객사 등록하기</button>
      </div>

      <!-- 고객사 생성 폼 (간단한 모달) -->
      <div v-if="showCreateForm" class="modal-overlay" @click.self="showCreateForm = false">
        <div class="modal-content">
          <h3>새 고객사 등록</h3>
          <form @submit.prevent="handleCreateCustomer" class="create-form">
            <div class="form-group">
              <label>고객사명 *</label>
              <input v-model="newCustomer.company_name" type="text" required class="form-input" />
            </div>
            <div class="form-group">
              <label>담당자명</label>
              <input v-model="newCustomer.contact_person" type="text" class="form-input" />
            </div>
            <div class="form-group">
              <label>담당자 이메일</label>
              <input v-model="newCustomer.contact_email" type="email" class="form-input" />
            </div>
            <div class="form-group">
              <label>담당자 전화번호</label>
              <input v-model="newCustomer.contact_phone" type="tel" class="form-input" />
            </div>
            <div class="form-group">
              <label>계약 유형</label>
              <input v-model="newCustomer.contract_type" type="text" class="form-input" />
            </div>
            <div class="form-group">
              <label>메모</label>
              <textarea v-model="newCustomer.notes" class="form-textarea"></textarea>
            </div>
            <div class="form-actions">
              <button type="button" @click="showCreateForm = false" class="btn-cancel">취소</button>
              <button type="submit" :disabled="isLoading" class="btn-submit">등록</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useCustomer } from '@/composables/useCustomer'
import type { Customer, CustomerCreate, CustomerStatus } from '@/types/customer'

// Customer composable 사용
const {
  customers,
  loading,
  error,
  pagination,
  searchParams,
  hasCustomers,
  hasError,
  isLoading,
  clearError,
  fetchCustomers,
  createCustomer,
  deleteCustomer,
  updateSearchParams,
  resetSearchParams,
  nextPage,
  prevPage
} = useCustomer()

// 로컬 상태
const searchQuery = ref('')
const selectedStatus = ref('')
const activeOnly = ref(false)
const showCreateForm = ref(false)

// 새 고객사 폼 데이터
const newCustomer = reactive<CustomerCreate>({
  company_name: '',
  contact_person: '',
  contact_email: '',
  contact_phone: '',
  contract_type: undefined,
  notes: ''
})

// 검색 처리
const handleSearch = async () => {
  updateSearchParams({
    q: searchQuery.value,
    status: (selectedStatus.value as CustomerStatus) || undefined,
    active_only: activeOnly.value,
    skip: 0 // 검색 시 첫 페이지로
  })
  await fetchCustomers()
}

// 고객사 생성 처리
const handleCreateCustomer = async () => {
  if (!newCustomer.company_name.trim()) return
  
  const success = await createCustomer({ ...newCustomer })
  if (success) {
    showCreateForm.value = false
    // 폼 초기화
    Object.assign(newCustomer, {
      company_name: '',
      contact_person: '',
      contact_email: '',
      contact_phone: '',
      contract_type: undefined,
      notes: ''
    })
    // 목록 새로고침
    await fetchCustomers()
  }
}

// 고객사 보기 (임시)
const viewCustomer = (customer: Customer) => {
  alert(`고객사 상세보기: ${customer.company_name}\nID: ${customer.id}`)
}

// 고객사 수정 (임시)
const editCustomer = (customer: Customer) => {
  alert(`고객사 수정: ${customer.company_name}\n(아직 구현되지 않음)`)
}

// 고객사 삭제 확인
const deleteCustomerConfirm = async (customer: Customer) => {
  if (confirm(`정말로 "${customer.company_name}"을(를) 삭제하시겠습니까?`)) {
    await deleteCustomer(customer.id)
  }
}

// 날짜 포맷팅
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('ko-KR')
}

// 컴포넌트 마운트 시 데이터 로드
onMounted(async () => {
  console.log('🏢 CustomerView 마운트됨 - 고객사 목록 로드 중...')
  await fetchCustomers()
})
</script>

<style scoped>
.customer-view {
  min-height: 100vh;
  background-color: #f8f9fa;
  padding: 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.page-subtitle {
  font-size: 1rem;
  color: #666;
}

/* 검색 및 필터 */
.search-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.search-controls {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.search-input {
  flex: 1;
  min-width: 200px;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.btn-search, .btn-create {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.btn-search {
  background: #007bff;
  color: white;
}

.btn-create {
  background: #28a745;
  color: white;
}

.filter-controls {
  display: flex;
  gap: 15px;
  align-items: center;
  flex-wrap: wrap;
}

.filter-select {
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.filter-checkbox {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
}

/* 로딩, 에러, 빈 상태 */
.loading-section, .error-section, .empty-section {
  text-align: center;
  padding: 40px;
  background: white;
  border-radius: 8px;
  margin: 20px 0;
}

.error-section {
  background: #f8d7da;
  color: #721c24;
}

.btn-clear {
  margin-left: 10px;
  padding: 4px 8px;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

/* 고객사 목록 */
.customer-list {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.list-header {
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.list-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

/* 테이블 스타일 */
.customer-table {
  display: table;
  width: 100%;
}

.table-header {
  display: table-row;
  background: #f8f9fa;
  font-weight: bold;
}

.table-row {
  display: table-row;
  border-bottom: 1px solid #eee;
}

.table-row:hover {
  background: #f8f9fa;
}

.table-header > div,
.table-row > div {
  display: table-cell;
  padding: 12px 15px;
  vertical-align: middle;
}

.col-company {
  width: 25%;
}

.col-company strong {
  display: block;
  color: #333;
}

.col-company small {
  display: block;
  color: #666;
  font-size: 0.9em;
}

.col-contact {
  width: 15%;
}

.col-status {
  width: 15%;
}

.col-contract {
  width: 25%;
}

.col-actions {
  width: 20%;
}

/* 상태 배지 */
.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8em;
  font-weight: 500;
}

.status-active {
  background: #d4edda;
  color: #155724;
}

.status-pending {
  background: #fff3cd;
  color: #856404;
}

.status-expired {
  background: #f8d7da;
  color: #721c24;
}

.status-suspended {
  background: #f8d7da;
  color: #721c24;
}

/* 액션 버튼 */
.btn-action, .btn-danger {
  padding: 4px 8px;
  margin: 0 2px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8em;
}

.btn-action {
  background: #007bff;
  color: white;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

/* 페이지네이션 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  padding: 20px;
  border-top: 1px solid #eee;
}

.btn-page {
  padding: 6px 12px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}

.btn-page:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: #666;
}

/* 모달 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-content h3 {
  margin: 0 0 20px 0;
  font-size: 1.5rem;
  color: #333;
}

/* 폼 스타일 */
.create-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-group label {
  font-weight: 500;
  color: #333;
}

.form-input, .form-textarea {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: inherit;
}

.form-textarea {
  min-height: 80px;
  resize: vertical;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}

.btn-cancel {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}

.btn-submit {
  padding: 8px 16px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style> 