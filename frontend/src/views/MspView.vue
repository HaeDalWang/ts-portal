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

    <!-- 헤더 -->
    <MspHeader
      :stats="stats"
      :view-mode="viewMode"
      :loading="loading"
      @view-mode-change="viewMode = $event"
      @create-customer="openCreateModal"
      @refresh="loadCustomers"
    />

    <!-- 메인 컨텐츠 -->
    <div class="p-6 space-y-6">
      <!-- 검색 및 필터 -->
      <MspSearchFilter
        v-model:search-query="searchQuery"
        v-model:selected-status="selectedStatus"
        :filtered-count="filteredCustomers.length"
      />

      <!-- 에러 메시지 -->
      <ErrorMessage
        v-if="error"
        :message="error"
        :show-retry="true"
        @retry="loadCustomers"
      />

      <!-- 로딩 상태 -->
      <LoadingState
        v-if="loading"
        message="고객사 정보를 불러오는 중..."
      />

      <!-- 카드 뷰 -->
      <MspCardView
        v-else-if="viewMode === 'cards' && filteredCustomers.length > 0"
        :customers="filteredCustomers"
        @customer-detail="showCustomerDetail"
        @edit-customer="openEditModal"
        @assign-customer="openAssignModal"
      />

      <!-- 테이블 뷰 -->
      <MspTableView
        v-else-if="viewMode === 'table' && filteredCustomers.length > 0"
        :customers="filteredCustomers"
        @customer-detail="showCustomerDetail"
        @edit-customer="openEditModal"
        @assign-customer="openAssignModal"
      />

      <!-- 빈 상태 -->
      <EmptyState
        v-else-if="!loading && !error && filteredCustomers.length === 0"
        icon="folder"
        title="고객사를 찾을 수 없습니다"
        description="검색 조건을 변경하거나 필터를 확인해보세요."
      >
        <template #actions>
          <button 
            @click="openCreateModal"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            첫 번째 고객사 추가하기
          </button>
        </template>
      </EmptyState>
    </div>

    <!-- 고객사 상세 모달 -->
    <CustomerDetailModal
      :show="showCustomerModal"
      :customer="selectedCustomer"
      @close="closeCustomerModal"
    />

    <!-- 고객사 생성 모달 -->
    <CustomerFormModal
      :show="showCreateModal"
      :is-edit="false"
      v-model:form-data="createForm"
      :loading="formLoading"
      @close="closeCreateModal"
      @submit="handleCreateCustomer"
    />

    <!-- 고객사 편집 모달 -->
    <CustomerFormModal
      :show="showEditModal"
      :is-edit="true"
      v-model:form-data="editForm"
      :loading="formLoading"
      @close="closeEditModal"
      @submit="handleUpdateCustomer"
    />

    <!-- 담당자 할당 모달 -->
    <CustomerAssignModal
      :show="showAssignModal"
      :customer="assigningCustomer"
      :members="availableMembers"
      :selected-assignee-id="selectedAssigneeId"
      :loading="formLoading"
      @close="closeAssignModal"
      @assign="handleAssignMember"
      @update:selected-assignee-id="selectedAssigneeId = $event"
    />
  </div>
</template>

<script setup lang="ts">
import { useMsp } from '@/composables/useMsp'
import {
  LoadingState,
  ErrorMessage,
  EmptyState
} from '@/components/common'
import MspHeader from '@/components/msp/MspHeader.vue'
import MspSearchFilter from '@/components/msp/MspSearchFilter.vue'
import MspCardView from '@/components/msp/MspCardView.vue'
import MspTableView from '@/components/msp/MspTableView.vue'
import CustomerDetailModal from '@/components/msp/CustomerDetailModal.vue'
import CustomerFormModal from '@/components/msp/CustomerFormModal.vue'
import CustomerAssignModal from '@/components/msp/CustomerAssignModal.vue'

// useMsp composable 사용
const {
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
} = useMsp()

// 이벤트 핸들러
const handleCreateCustomer = async () => {
  const result = await createCustomer()
  if (!result.success) {
    alert(result.message)
  }
}

const handleUpdateCustomer = async () => {
  const result = await updateCustomer()
  if (!result.success) {
    alert(result.message)
  }
}

const handleAssignMember = async () => {
  const result = await assignMember()
  if (!result.success) {
    alert(result.message)
  }
}
</script> 