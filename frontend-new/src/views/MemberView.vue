<template>
  <div class="member-view">
    <!-- 헤더 -->
    <div class="page-header">
      <h1>팀원 관리</h1>
      <p>TS팀 구성원들을 관리합니다</p>
    </div>

    <!-- 검색 및 필터 -->
    <div class="search-section">
      <div class="search-controls">
        <input
          v-model="searchTerm"
          type="text"
          placeholder="이름 또는 이메일로 검색..."
          class="search-input"
          @input="handleSearch"
        >
        
        <select v-model="selectedTeam" @change="handleTeamFilter" class="filter-select">
          <option value="">전체 팀</option>
          <option value="TS팀">TS팀</option>
          <option value="Leaf팀">Leaf팀</option>
          <option value="Tiger팀">Tiger팀</option>
          <option value="Aqua팀">Aqua팀</option>
        </select>

        <select v-model="selectedPosition" @change="handlePositionFilter" class="filter-select">
          <option value="">전체 직책</option>
          <option value="상무">상무</option>
          <option value="선임매니저">선임매니저</option>
          <option value="매니저">매니저</option>
          <option value="시스템관리자">시스템관리자</option>
        </select>

        <button @click="resetFilters" class="btn btn-secondary">
          초기화
        </button>
      </div>

      <!-- 통계 정보 -->
      <div class="stats-section">
        <div class="stat-card">
          <span class="stat-label">전체 인원</span>
          <span class="stat-value">{{ totalCount }}</span>
        </div>
        <div class="stat-card">
          <span class="stat-label">활성 인원</span>
          <span class="stat-value">{{ activeMembers.length }}</span>
        </div>
      </div>
    </div>

    <!-- 로딩 상태 -->
    <div v-if="loading" class="loading-section">
      <div class="loading-spinner"></div>
      <p>팀원 정보를 불러오는 중...</p>
    </div>

    <!-- 에러 상태 -->
    <div v-else-if="error" class="error-section">
      <p class="error-message">{{ error }}</p>
      <button @click="handleRetry" class="btn btn-primary">다시 시도</button>
    </div>

    <!-- 빈 상태 -->
    <div v-else-if="isEmpty" class="empty-section">
      <p>조건에 맞는 팀원이 없습니다.</p>
    </div>

    <!-- 팀원 목록 -->
    <div v-else class="members-section">
      <!-- 팀별 그룹핑 -->
      <div v-if="isGroupByTeam" class="team-groups">
        <div v-for="(teamMembers, team) in membersByTeam" :key="team" class="team-group">
          <h3 class="team-title">{{ team }} ({{ teamMembers.length }}명)</h3>
          <div class="member-grid">
            <MemberCard
              v-for="member in teamMembers"
              :key="member.id"
              :member="member"
              @click="handleMemberClick(member)"
            />
          </div>
        </div>
      </div>

      <!-- 일반 목록 -->
      <div v-else class="member-grid">
        <MemberCard
          v-for="member in members"
          :key="member.id"
          :member="member"
          @click="handleMemberClick(member)"
        />
      </div>

      <!-- 페이지네이션 -->
      <div v-if="totalPages > 1" class="pagination-section">
        <button
          @click="changePage(currentPage - 1)"
          :disabled="currentPage <= 1"
          class="btn btn-secondary"
        >
          이전
        </button>
        
        <span class="page-info">
          {{ currentPage }} / {{ totalPages }}
        </span>
        
        <button
          @click="changePage(currentPage + 1)"
          :disabled="currentPage >= totalPages"
          class="btn btn-secondary"
        >
          다음
        </button>
      </div>
    </div>

    <!-- 뷰 옵션 -->
    <div class="view-options">
      <label class="checkbox-label">
        <input
          v-model="isGroupByTeam"
          type="checkbox"
        >
        팀별 그룹핑
      </label>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useMember } from '@/composables/useMember'
import MemberCard from '@/components/MemberCard.vue'
import type { Member } from '@/types/member'

// Member Service 상태 관리
const {
  members,
  loading,
  error,
  totalCount,
  currentPage,
  totalPages,
  isEmpty,
  membersByTeam,
  activeMembers,
  fetchMembers,
  changePage,
  clearError
} = useMember()

// 로컬 상태
const searchTerm = ref('')
const selectedTeam = ref('')
const selectedPosition = ref('')
const isGroupByTeam = ref(true)

// 검색 디바운스를 위한 타이머
let searchTimer: number

/**
 * 검색 처리
 */
const handleSearch = () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    fetchMembers({
      search: searchTerm.value || undefined,
      team: selectedTeam.value || undefined,
      position: selectedPosition.value || undefined,
      is_active: true
    })
  }, 300)
}

/**
 * 팀 필터 처리
 */
const handleTeamFilter = () => {
  fetchMembers({
    search: searchTerm.value || undefined,
    team: selectedTeam.value || undefined,
    position: selectedPosition.value || undefined,
    is_active: true
  })
}

/**
 * 직책 필터 처리
 */
const handlePositionFilter = () => {
  fetchMembers({
    search: searchTerm.value || undefined,
    team: selectedTeam.value || undefined,
    position: selectedPosition.value || undefined,
    is_active: true
  })
}

/**
 * 필터 초기화
 */
const resetFilters = () => {
  searchTerm.value = ''
  selectedTeam.value = ''
  selectedPosition.value = ''
  fetchMembers({ is_active: true })
}

/**
 * 재시도 처리
 */
const handleRetry = () => {
  clearError()
  fetchMembers({ is_active: true })
}

/**
 * 팀원 클릭 처리
 */
const handleMemberClick = (member: Member) => {
  console.log('팀원 클릭:', member.name)
  // TODO: 상세 모달 또는 상세 페이지로 이동
}

// 컴포넌트 마운트 시 데이터 로드
onMounted(() => {
  console.log('👥 MemberView 마운트됨')
  fetchMembers({ is_active: true })
})
</script>

<style scoped>
.member-view {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 0.5rem;
}

.page-header p {
  color: var(--color-text-secondary);
  font-size: 1.1rem;
}

.search-section {
  background: var(--color-surface);
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  border: 1px solid var(--color-border);
}

.search-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.search-input, .filter-select {
  padding: 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background: var(--color-background);
  color: var(--color-text-primary);
  font-size: 0.95rem;
}

.search-input {
  flex: 1;
  min-width: 200px;
}

.filter-select {
  min-width: 120px;
}

.stats-section {
  display: flex;
  gap: 1rem;
}

.stat-card {
  background: var(--color-primary);
  color: white;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
  min-width: 100px;
}

.stat-label {
  display: block;
  font-size: 0.85rem;
  opacity: 0.9;
  margin-bottom: 0.25rem;
}

.stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 600;
}

.loading-section, .error-section, .empty-section {
  text-align: center;
  padding: 3rem;
  color: var(--color-text-secondary);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--color-border);
  border-top: 3px solid var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  color: var(--color-error);
  margin-bottom: 1rem;
}

.team-groups {
  space-y: 2rem;
}

.team-group {
  margin-bottom: 2rem;
}

.team-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--color-primary);
}

.member-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.pagination-section {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid var(--color-border);
}

.page-info {
  font-weight: 500;
  color: var(--color-text-primary);
}

.view-options {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background: var(--color-surface);
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid var(--color-border);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: var(--color-text-primary);
  cursor: pointer;
}

.checkbox-label input {
  margin: 0;
}
</style> 