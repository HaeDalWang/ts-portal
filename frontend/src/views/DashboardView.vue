<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 컴팩트 헤더 -->
    <div class="bg-white border-b border-gray-200 px-6 py-3">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-xl font-bold text-gray-900">팀 대시보드</h1>
          <p class="text-sm text-gray-500">TS팀 일정 관리</p>
        </div>
        
        <!-- 통계 카드 -->
        <StatsCards :stats="stats" />
      </div>
    </div>

    <div class="flex h-screen">
      <!-- 사이드바 필터 -->
      <SidebarFilters
        :current-view="currentView"
        :members="members"
        :is-all-selected="isAllSelected"
        :selected-members="selectedMembers"
        :is-all-parts-selected="isAllPartsSelected"
        :selected-parts="selectedParts"
        :get-member-color="getMemberColor"
        @view-change="handleViewChange"
        @toggle-all-members="toggleAllMembers"
        @toggle-member="toggleMember"
        @toggle-all-parts="toggleAllParts"
        @toggle-part="togglePart"
      />

      <!-- 달력 위젯 -->
      <CalendarWidget
        ref="calendarWidget"
        :current-view="currentView"
        :load-events="loadEvents"
        :members="members"
        :selected-members="selectedMembers"
        :is-all-selected="isAllSelected"
        :get-member-color="getMemberColor"
        @date-click="openEventModal"
      />
    </div>

    <!-- 이벤트 모달 -->
    <EventModal
      :show="showEventModal"
      :selected-date="selectedDate"
      :events="selectedDateEvents"
      :get-event-type-icon="getEventTypeIcon"
      :get-status-badge-class="getStatusBadgeClass"
      :get-status-text="getStatusText"
      :format-event-time="formatEventTime"
      :get-member-color="getMemberColor"
      @close="closeEventModal"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import StatsCards from '@/components/dashboard/StatsCards.vue'
import SidebarFilters from '@/components/dashboard/SidebarFilters.vue'
import CalendarWidget from '@/components/dashboard/CalendarWidget.vue'
import EventModal from '@/components/dashboard/EventModal.vue'
import { useDashboard } from '@/composables/useDashboard'
import '@/assets/styles/calendar.css'

// Composable 사용으로 로직 분리
const {
  // 상태
  loading,
  stats,
  members,
  currentView,
  selectedMembers,
  isAllSelected,
  selectedParts,
  isAllPartsSelected,
  showEventModal,
  selectedDate,
  selectedDateEvents,
  
  // 메서드
  loadEvents,
  getMemberColor,
  toggleMember,
  toggleAllMembers,
  togglePart,
  toggleAllParts,
  openEventModal,
  closeEventModal,
  getEventTypeIcon,
  getStatusBadgeClass,
  getStatusText,
  formatEventTime,
  refreshCalendar
} = useDashboard()

// 컴포넌트 참조
const calendarWidget = ref()

// 뷰 변경 핸들러
const handleViewChange = (view: string) => {
  currentView.value = view
}

// 달력 새로고침 (필터 변경 시)
const refreshEvents = () => {
  calendarWidget.value?.refreshEvents()
}

// 컴포넌트 마운트 시 초기화
onMounted(async () => {
  // 초기 데이터 로드는 composable에서 처리
})
</script> 