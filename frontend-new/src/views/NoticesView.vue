<template>
  <div class="notices-view">
    <!-- 헤더 -->
    <div class="notices-header">
      <div class="header-content">
        <h1 class="page-title">
          <span class="icon">📋</span>
          공지사항
        </h1>
        <p class="page-subtitle">중요한 소식과 공지사항을 확인하세요</p>
      </div>
      
      <!-- 컨트롤 -->
      <div class="notices-controls">
        <div class="search-box">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="공지사항 검색..."
            class="search-input"
            @keyup.enter="handleSearch"
          />
          <span class="search-icon">🔍</span>
        </div>
        
        <button
          @click="refresh"
          :disabled="loading"
          class="refresh-btn"
          :class="{ loading }"
        >
          <span class="refresh-icon">🔄</span>
          새로고침
        </button>
        
        <button
          @click="showCreateModal = true"
          class="create-btn"
        >
          <span class="create-icon">➕</span>
          새 공지사항
        </button>
      </div>
    </div>

    <!-- 에러 메시지 -->
    <div v-if="error" class="error-message">
      <span class="error-icon">❌</span>
      {{ error }}
      <button @click="clearError" class="error-close">×</button>
    </div>

    <!-- 고정 공지사항 -->
    <div v-if="hasPinnedNotices" class="pinned-section">
      <h2 class="section-title">
        <span class="pin-icon">📌</span>
        고정 공지사항
      </h2>
      <div class="pinned-notices">
        <NoticeItem
          v-for="notice in pinnedNotices"
          :key="`pinned-${notice.id}`"
          :notice="notice"
          :pinned="true"
          @edit="handleEdit"
          @delete="handleDelete"
        />
      </div>
    </div>

    <!-- 일반 공지사항 -->
    <div class="notices-section">
      <div class="section-header">
        <h2 class="section-title">전체 공지사항</h2>
        <div class="filter-controls">
          <select v-model="priorityFilter" @change="handleSearch" class="priority-filter">
            <option value="">모든 우선순위</option>
            <option 
              v-for="priority in priorities" 
              :key="priority.value" 
              :value="priority.value"
            >
              {{ priority.icon }} {{ priority.label }}
            </option>
          </select>
        </div>
      </div>

      <!-- 로딩 상태 -->
      <div v-if="loading && !hasNotices" class="loading-state">
        <div class="loading-spinner">⏳</div>
        <p>공지사항을 가져오는 중...</p>
      </div>

      <!-- 공지사항 목록 -->
      <div v-else-if="hasNotices" class="notices-list">
        <NoticeItem
          v-for="notice in notices"
          :key="notice.id"
          :notice="notice"
          @edit="handleEdit"
          @delete="handleDelete"
        />
      </div>

      <!-- 빈 상태 -->
      <div v-else class="empty-state">
        <span class="empty-icon">📭</span>
        <p>등록된 공지사항이 없습니다.</p>
        <button @click="showCreateModal = true" class="create-empty-btn">
          첫 번째 공지사항 작성하기
        </button>
      </div>
    </div>

    <!-- 페이지네이션 -->
    <div v-if="totalPages > 1" class="pagination">
      <button
        v-for="page in displayedPages"
        :key="page"
        @click="goToPage(page)"
        :class="['page-btn', { active: currentPage === page }]"
        :disabled="loading"
      >
        {{ page }}
      </button>
    </div>

    <!-- 생성/수정 모달 -->
    <NoticeModal
      v-if="showCreateModal || showEditModal"
      :notice="editingNotice"
      :priorities="priorities"
      @save="handleSave"
      @close="handleCloseModal"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useNotices } from '@/composables/useNotices'
import { NoticePriority } from '@/types/notices'
import type { NoticeResponse, NoticeCreate, NoticeUpdate } from '@/types/notices'
import NoticeItem from '@/components/notices/NoticeItem.vue'
import NoticeModal from '@/components/notices/NoticeModal.vue'

// Composable 사용
const {
  notices,
  pinnedNotices,
  priorities,
  loading,
  error,
  total,
  hasNotices,
  hasPinnedNotices,
  totalPages,
  loadNotices,
  searchNotices,
  loadPinnedNotices,
  loadPriorities,
  createNotice,
  updateNotice,
  deleteNotice,
  canDeleteNotice,
  formatDate,
  clearError,
  refresh
} = useNotices()

// 로컬 상태
const searchQuery = ref('')
const priorityFilter = ref('')
const currentPage = ref(1)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const editingNotice = ref<NoticeResponse | null>(null)

// 페이지네이션
const displayedPages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, start + 4)
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

// 검색 처리
const handleSearch = async () => {
  currentPage.value = 1
  const searchParams = {
    q: searchQuery.value || undefined,
    priority: priorityFilter.value ? priorityFilter.value as NoticePriority : undefined,
    active_only: true
  }
  
  const pagination = {
    skip: 0,
    limit: 20
  }
  
  if (searchQuery.value || priorityFilter.value) {
    await searchNotices(searchParams, pagination)
  } else {
    await loadNotices(0, 20)
  }
}

// 페이지 이동
const goToPage = async (page: number) => {
  currentPage.value = page
  const skip = (page - 1) * 20
  
  if (searchQuery.value || priorityFilter.value) {
    const searchParams = {
      q: searchQuery.value || undefined,
      priority: priorityFilter.value ? priorityFilter.value as NoticePriority : undefined,
      active_only: true
    }
    await searchNotices(searchParams, { skip, limit: 20 })
  } else {
    await loadNotices(skip, 20)
  }
}

// 수정 처리
const handleEdit = (notice: NoticeResponse) => {
  editingNotice.value = notice
  showEditModal.value = true
}

// 삭제 처리
const handleDelete = async (notice: NoticeResponse) => {
  if (!canDeleteNotice(notice)) {
    alert('이 공지사항을 삭제할 권한이 없습니다.')
    return
  }
  
  if (confirm(`"${notice.title}" 공지사항을 삭제하시겠습니까?`)) {
    const success = await deleteNotice(notice.id)
    if (success) {
      // 현재 페이지에 남은 공지사항이 없으면 이전 페이지로
      if (notices.value.length === 1 && currentPage.value > 1) {
        await goToPage(currentPage.value - 1)
      }
    }
  }
}

// 저장 처리
const handleSave = async (noticeData: NoticeCreate | NoticeUpdate) => {
  let success = false
  
  if (editingNotice.value) {
    // 수정
    success = await updateNotice(editingNotice.value.id, noticeData as NoticeUpdate)
  } else {
    // 생성
    const newNotice = await createNotice(noticeData as NoticeCreate)
    success = !!newNotice
  }
  
  if (success) {
    handleCloseModal()
    // 고정 공지사항 새로고침
    await loadPinnedNotices()
  }
}

// 모달 닫기
const handleCloseModal = () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingNotice.value = null
}

// 컴포넌트 마운트 시 초기 로드
onMounted(async () => {
  console.log('📋 공지사항 뷰 마운트됨')
  await Promise.all([
    loadNotices(),
    loadPinnedNotices(),
    loadPriorities()
  ])
})

// 검색어 변경 시 디바운스 검색
let searchTimeout: number
watch(searchQuery, () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    if (searchQuery.value.length === 0 || searchQuery.value.length >= 2) {
      handleSearch()
    }
  }, 500)
})
</script>

<style scoped>
.notices-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

/* 헤더 */
.notices-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  gap: 2rem;
}

.header-content {
  flex: 1;
}

.page-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.page-subtitle {
  font-size: 1.1rem;
  color: #718096;
  margin: 0;
}

.notices-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.search-box {
  position: relative;
}

.search-input {
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 1rem;
  width: 250px;
  outline: none;
  transition: border-color 0.2s;
}

.search-input:focus {
  border-color: #3182ce;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #a0aec0;
}

.refresh-btn, .create-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
}

.refresh-btn {
  background: #6b7280;
  color: white;
}

.refresh-btn:hover:not(:disabled) {
  background: #4b5563;
}

.create-btn {
  background: #3182ce;
  color: white;
}

.create-btn:hover {
  background: #2c5aa0;
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.refresh-btn.loading .refresh-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 에러 메시지 */
.error-message {
  background: #fed7d7;
  color: #c53030;
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.error-close {
  margin-left: auto;
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  color: #c53030;
}

/* 섹션 */
.pinned-section, .notices-section {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #1a202c;
  margin: 0 0 1rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.filter-controls {
  display: flex;
  gap: 1rem;
}

.priority-filter {
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  background: white;
  cursor: pointer;
}

/* 공지사항 목록 */
.pinned-notices, .notices-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* 로딩 상태 */
.loading-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #718096;
}

.loading-spinner {
  font-size: 2rem;
  margin-bottom: 1rem;
  animation: spin 2s linear infinite;
}

/* 빈 상태 */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #718096;
}

.empty-icon {
  font-size: 4rem;
  display: block;
  margin-bottom: 1rem;
}

.create-empty-btn {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: #3182ce;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.2s;
}

.create-empty-btn:hover {
  background: #2c5aa0;
}

/* 페이지네이션 */
.pagination {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 2rem;
}

.page-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #e2e8f0;
  background: white;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  border-color: #3182ce;
}

.page-btn.active {
  background: #3182ce;
  color: white;
  border-color: #3182ce;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 반응형 */
@media (max-width: 768px) {
  .notices-view {
    padding: 1rem;
  }
  
  .notices-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .notices-controls {
    width: 100%;
    justify-content: stretch;
  }
  
  .search-input {
    width: 100%;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}
</style> 