<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 헤더 -->
    <NoticesHeader
      :stats="stats"
      :view-mode="viewMode"
      :loading="loading"
      @view-mode-change="viewMode = $event"
      @create-notice="showCreateModal = true"
      @refresh="loadNotices"
    />

    <!-- 메인 컨텐츠 -->
    <div class="p-6 space-y-6">
      <!-- 검색 및 필터 -->
      <NoticesSearchFilter
        v-model:search-query="searchQuery"
        v-model:selected-priority="selectedPriority"
        v-model:show-pinned-only="showPinnedOnly"
      />

      <!-- 로딩 상태 -->
      <LoadingState
        v-if="loading"
        message="공지사항을 불러오는 중..."
      />

      <!-- 에러 상태 -->
      <ErrorMessage
        v-else-if="error"
        :message="error"
        :show-retry="true"
        @retry="loadNotices"
      />

      <!-- 카드 뷰 -->
      <NoticesCardView
        v-else-if="viewMode === 'cards'"
        :notices="filteredNotices"
        :members="members"
        @notice-click="showNoticeDetail"
        @edit-notice="editNoticeDetail"
        @delete-notice="handleDeleteNotice"
      />

      <!-- 테이블 뷰 -->
      <NoticesTableView
        v-else
        :notices="filteredNotices"
        :members="members"
        @notice-click="showNoticeDetail"
        @edit-notice="editNoticeDetail"
        @delete-notice="handleDeleteNotice"
      />

      <!-- 빈 상태 -->
      <EmptyState
        v-if="!loading && !error && filteredNotices.length === 0"
        icon="document"
        title="공지사항이 없습니다"
        :description="searchQuery || selectedPriority !== 'all' || showPinnedOnly 
          ? '검색 조건에 맞는 공지사항이 없습니다.' 
          : '새로운 공지사항을 작성해보세요.'"
      >
        <template #actions>
          <div class="space-x-3">
            <button
              v-if="searchQuery || selectedPriority !== 'all' || showPinnedOnly"
              @click="resetFilters"
              class="text-blue-600 hover:text-blue-700 transition-colors"
            >
              필터 초기화
            </button>
            <button
              @click="showCreateModal = true"
              class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              새 공지사항 작성
            </button>
          </div>
        </template>
      </EmptyState>
    </div>

    <!-- 공지사항 상세 모달 -->
    <NoticeDetailModal
      :show="showNoticeModal"
      :notice="selectedNotice"
      :members="members"
      @close="closeModals"
      @edit="(notice: any) => notice && editNoticeDetail(notice)"
      @delete="handleDeleteNotice"
    />

    <!-- 공지사항 생성 모달 -->
    <NoticeFormModal
      :show="showCreateModal"
      :is-edit="false"
      v-model:form-data="newNotice"
      @close="closeModals"
      @submit="handleCreateNotice"
    />

    <!-- 공지사항 편집 모달 -->
    <NoticeFormModal
      :show="showEditModal"
      :is-edit="true"
      v-model:form-data="editNotice"
      @close="closeModals"
      @submit="handleUpdateNotice"
    />
  </div>
</template>

<script setup lang="ts">
import { useNotices } from '@/composables/useNotices'
import {
  LoadingState,
  ErrorMessage,
  EmptyState
} from '@/components/common'
import NoticesHeader from '@/components/notices/NoticesHeader.vue'
import NoticesSearchFilter from '@/components/notices/NoticesSearchFilter.vue'
import NoticesCardView from '@/components/notices/NoticesCardView.vue'
import NoticesTableView from '@/components/notices/NoticesTableView.vue'
import NoticeDetailModal from '@/components/notices/NoticeDetailModal.vue'
import NoticeFormModal from '@/components/notices/NoticeFormModal.vue'

// useNotices composable 사용
const {
  // 상태
  stats,
  loading,
  error,
  searchQuery,
  selectedPriority,
  showPinnedOnly,
  viewMode,
  selectedNotice,
  showNoticeModal,
  showCreateModal,
  showEditModal,
  newNotice,
  editNotice,
  filteredNotices,
  members,
  
  // 메서드
  loadNotices,
  showNoticeDetail,
  editNoticeDetail,
  closeModals,
  createNotice,
  updateNotice,
  deleteNotice,
  resetFilters
} = useNotices()

// 이벤트 핸들러
const handleCreateNotice = async () => {
  const result = await createNotice()
  if (result.success) {
    // 성공 처리 (토스트 알림 등)
    console.log(result.message)
  } else {
    // 에러 처리
    alert(result.message)
  }
}

const handleUpdateNotice = async () => {
  const result = await updateNotice()
  if (result.success) {
    // 성공 처리
    console.log(result.message)
  } else {
    // 에러 처리
    alert(result.message)
  }
}

const handleDeleteNotice = async (noticeId: number | undefined) => {
  if (!noticeId) return
  
  if (!confirm('정말로 이 공지사항을 삭제하시겠습니까?')) return
  
  const result = await deleteNotice(noticeId)
  if (result.success) {
    // 성공 처리
    console.log(result.message)
    closeModals() // 모달이 열려있다면 닫기
  } else {
    // 에러 처리
    alert(result.message)
  }
}
</script> 