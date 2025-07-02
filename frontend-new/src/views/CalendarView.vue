<template>
  <div class="calendar-view">
    <!-- 헤더 -->
    <div class="calendar-header">
      <div class="header-content">
        <h1 class="page-title">
          <span class="icon">📅</span>
          일정 관리
        </h1>
        <p class="page-subtitle">팀원들의 일정을 관리하고 확인하세요</p>
      </div>
      
      <!-- 컨트롤 -->
      <div class="calendar-controls">
        <div class="view-toggle">
          <button
            v-for="view in viewOptions"
            :key="view.value"
            @click="setCurrentView(view.value as 'month' | 'week' | 'day' | 'list')"
            :class="['view-btn', { active: currentView === view.value }]"
          >
            <span class="view-icon">{{ view.icon }}</span>
            {{ view.label }}
          </button>
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
          새 일정
        </button>
      </div>
    </div>

    <!-- 에러 메시지 -->
    <div v-if="error" class="error-message">
      <span class="error-icon">❌</span>
      {{ error }}
      <button @click="clearError" class="error-close">×</button>
    </div>

    <!-- 통계 대시보드 -->
    <div v-if="stats" class="stats-dashboard">
      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-content">
          <div class="stat-number">{{ stats.total_events }}</div>
          <div class="stat-label">전체 일정</div>
        </div>
      </div>
      
      <div class="stat-card today">
        <div class="stat-icon">📋</div>
        <div class="stat-content">
          <div class="stat-number">{{ stats.today_events }}</div>
          <div class="stat-label">오늘 일정</div>
        </div>
      </div>
      
      <div class="stat-card upcoming">
        <div class="stat-icon">⏰</div>
        <div class="stat-content">
          <div class="stat-number">{{ stats.upcoming_events }}</div>
          <div class="stat-label">다가오는 일정</div>
        </div>
      </div>
      
      <div class="stat-card ongoing">
        <div class="stat-icon">🔄</div>
        <div class="stat-content">
          <div class="stat-number">{{ stats.ongoing_events }}</div>
          <div class="stat-label">진행중인 일정</div>
        </div>
      </div>
    </div>

    <!-- 오늘 일정 -->
    <div v-if="hasTodayEvents" class="today-section">
      <h2 class="section-title">
        <span class="section-icon">📋</span>
        오늘 일정
      </h2>
      <div class="today-events">
        <EventCard
          v-for="event in todayEvents"
          :key="`today-${event.id}`"
          :event="event"
          :compact="true"
          @edit="handleEdit"
          @delete="handleDelete"
        />
      </div>
    </div>

    <!-- 메인 컨텐츠 -->
    <div class="main-content">
      <!-- 검색 및 필터 -->
      <div class="search-filter-section">
        <div class="search-box">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="일정 검색..."
            class="search-input"
            @keyup.enter="handleSearch"
          />
          <span class="search-icon">🔍</span>
        </div>
        
        <div class="filter-controls">
          <select v-model="eventTypeFilter" @change="handleSearch" class="filter-select">
            <option value="">모든 타입</option>
            <option 
              v-for="type in eventTypes" 
              :key="type.value" 
              :value="type.value"
            >
              {{ type.icon }} {{ type.label }}
            </option>
          </select>
          
          <input
            v-model="startDateFilter"
            type="date"
            class="date-input"
            @change="handleSearch"
            placeholder="시작일"
          />
          
          <input
            v-model="endDateFilter"
            type="date"
            class="date-input"
            @change="handleSearch"
            placeholder="종료일"
          />
        </div>
      </div>

      <!-- 일정 목록 (List View) -->
      <div v-if="currentView === 'list'" class="list-view">
        <!-- 로딩 상태 -->
        <div v-if="loading && !hasEvents" class="loading-state">
          <div class="loading-spinner">⏳</div>
          <p>일정을 가져오는 중...</p>
        </div>

        <!-- 일정 목록 -->
        <div v-else-if="hasEvents" class="events-list">
          <EventCard
            v-for="event in events"
            :key="event.id"
            :event="event"
            @edit="handleEdit"
            @delete="handleDelete"
          />
        </div>

        <!-- 빈 상태 -->
        <div v-else class="empty-state">
          <span class="empty-icon">📭</span>
          <p>등록된 일정이 없습니다.</p>
          <button @click="showCreateModal = true" class="create-empty-btn">
            첫 번째 일정 만들기
          </button>
        </div>
      </div>

      <!-- 간단한 달력 뷰 (Month View) -->
      <div v-else-if="currentView === 'month'" class="month-view">
        <div class="month-header">
          <button @click="previousMonth" class="month-nav-btn">‹</button>
          <h3 class="month-title">{{ currentMonthTitle }}</h3>
          <button @click="nextMonth" class="month-nav-btn">›</button>
        </div>
        
        <div class="calendar-grid">
          <div class="weekdays">
            <div v-for="day in weekdays" :key="day" class="weekday">{{ day }}</div>
          </div>
          
          <div class="days-grid">
            <div
              v-for="day in calendarDays"
              :key="day.date"
              :class="['day-cell', { 
                'other-month': day.otherMonth,
                'today': day.isToday,
                'selected': day.isSelected,
                'has-events': day.events.length > 0
              }]"
              @click="selectDate(day.date)"
            >
              <div class="day-number">{{ day.day }}</div>
              <div v-if="day.events.length > 0" class="day-events">
                <div
                  v-for="event in day.events.slice(0, 3)"
                  :key="event.id"
                  class="day-event"
                  :style="{ backgroundColor: event.color || getEventTypeColor(event.event_type) }"
                  @click.stop="handleEdit(event)"
                >
                  {{ event.title }}
                </div>
                <div v-if="day.events.length > 3" class="more-events">
                  +{{ day.events.length - 3 }}개 더
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 페이지네이션 -->
    <div v-if="currentView === 'list' && totalPages > 1" class="pagination">
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
    <EventModal
      v-if="showCreateModal || showEditModal"
      :event="editingEvent"
      :eventTypes="eventTypes"
      @save="handleSave"
      @close="handleCloseModal"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useCalendar } from '@/composables/useCalendar'
import { EventType } from '@/types/calendar'
import type { EventResponse, EventCreate, EventUpdate } from '@/types/calendar'
import EventCard from '@/components/calendar/EventCard.vue'
import EventModal from '@/components/calendar/EventModal.vue'

// Composable 사용
const {
  events,
  todayEvents,
  stats,
  eventTypes,
  loading,
  error,
  total,
  currentView,
  hasEvents,
  hasTodayEvents,
  totalPages,
  loadEvents,
  loadTodayEvents,
  loadStats,
  loadEventTypes,
  createEvent,
  updateEvent,
  deleteEvent,
  searchEvents,
  setCurrentView,
  clearError,
  refresh
} = useCalendar()

// 로컬 상태
const searchQuery = ref('')
const eventTypeFilter = ref('')
const startDateFilter = ref('')
const endDateFilter = ref('')
const currentPage = ref(1)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const editingEvent = ref<EventResponse | null>(null)
const currentDate = ref(new Date())
const selectedDate = ref<string | null>(null)

// 보기 옵션
const viewOptions = [
  { value: 'list', label: '목록', icon: '📋' },
  { value: 'month', label: '월간', icon: '📅' },
]

// 요일
const weekdays = ['일', '월', '화', '수', '목', '금', '토']

// 계산된 속성
const displayedPages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, start + 4)
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

const currentMonthTitle = computed(() => {
  return currentDate.value.toLocaleDateString('ko-KR', { 
    year: 'numeric', 
    month: 'long' 
  })
})

const calendarDays = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth()
  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)
  const startDate = new Date(firstDay)
  startDate.setDate(startDate.getDate() - firstDay.getDay())
  
  const days = []
  const today = new Date()
  
  for (let i = 0; i < 42; i++) { // 6주 * 7일
    const date = new Date(startDate)
    date.setDate(startDate.getDate() + i)
    
    const dateStr = date.toISOString().split('T')[0]
    const dayEvents = events.value.filter(event => {
      const eventDate = new Date(event.start_time).toISOString().split('T')[0]
      return eventDate === dateStr
    })
    
    days.push({
      date: dateStr,
      day: date.getDate(),
      otherMonth: date.getMonth() !== month,
      isToday: date.toDateString() === today.toDateString(),
      isSelected: dateStr === selectedDate.value,
      events: dayEvents
    })
  }
  
  return days
})

// 메서드
const handleSearch = async () => {
  currentPage.value = 1
  const searchParams = {
    q: searchQuery.value || undefined,
    event_type: eventTypeFilter.value ? eventTypeFilter.value as EventType : undefined,
    start_date: startDateFilter.value || undefined,
    end_date: endDateFilter.value || undefined
  }
  
  const pagination = {
    skip: 0,
    limit: 50
  }
  
  if (Object.values(searchParams).some(v => v !== undefined)) {
    await searchEvents(searchParams, pagination)
  } else {
    await loadEvents(0, 50)
  }
}

const goToPage = async (page: number) => {
  currentPage.value = page
  const skip = (page - 1) * 50
  
  if (searchQuery.value || eventTypeFilter.value || startDateFilter.value || endDateFilter.value) {
    const searchParams = {
      q: searchQuery.value || undefined,
      event_type: eventTypeFilter.value ? eventTypeFilter.value as EventType : undefined,
      start_date: startDateFilter.value || undefined,
      end_date: endDateFilter.value || undefined
    }
    await searchEvents(searchParams, { skip, limit: 50 })
  } else {
    await loadEvents(skip, 50)
  }
}

const handleEdit = (event: EventResponse) => {
  editingEvent.value = event
  showEditModal.value = true
}

const handleDelete = async (event: EventResponse) => {
  if (confirm(`"${event.title}" 일정을 삭제하시겠습니까?`)) {
    const success = await deleteEvent(event.id)
    if (success) {
      // 현재 페이지에 남은 이벤트가 없으면 이전 페이지로
      if (events.value.length === 1 && currentPage.value > 1) {
        await goToPage(currentPage.value - 1)
      }
    }
  }
}

const handleSave = async (eventData: EventCreate | EventUpdate) => {
  let success = false
  
  if (editingEvent.value) {
    // 수정
    success = await updateEvent(editingEvent.value.id, eventData as EventUpdate)
  } else {
    // 생성
    const newEvent = await createEvent(eventData as EventCreate)
    success = !!newEvent
  }
  
  if (success) {
    handleCloseModal()
    // 오늘 일정 새로고침
    await loadTodayEvents()
  }
}

const handleCloseModal = () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingEvent.value = null
}

const previousMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() - 1, 1)
}

const nextMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() + 1, 1)
}

const selectDate = (date: string) => {
  selectedDate.value = selectedDate.value === date ? null : date
}

const getEventTypeColor = (eventType: EventType): string => {
  const typeInfo = eventTypes.value.find(type => type.value === eventType)
  return typeInfo?.color || '#6B7280'
}

// 컴포넌트 마운트 시 초기 로드
onMounted(async () => {
  console.log('📅 일정 관리 뷰 마운트됨')
  await Promise.all([
    loadEvents(),
    loadTodayEvents(),
    loadStats(),
    loadEventTypes()
  ])
})

// 보기 변경 시 필요한 데이터 로드
watch(currentView, async (newView) => {
  if (newView === 'month') {
    // 월간 보기에서는 현재 월의 이벤트만 로드
    const year = currentDate.value.getFullYear()
    const month = currentDate.value.getMonth()
    const startDate = new Date(year, month, 1).toISOString().split('T')[0]
    const endDate = new Date(year, month + 1, 0).toISOString().split('T')[0]
    
    await searchEvents({
      start_date: startDate,
      end_date: endDate
    }, { skip: 0, limit: 1000 })
  }
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
.calendar-view {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

/* 헤더 */
.calendar-header {
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

.calendar-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.view-toggle {
  display: flex;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  overflow: hidden;
}

.view-btn {
  padding: 0.75rem 1rem;
  border: none;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
}

.view-btn:hover {
  background: #f7fafc;
}

.view-btn.active {
  background: #3182ce;
  color: white;
}

.refresh-btn, .create-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
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
  background: #10b981;
  color: white;
}

.create-btn:hover {
  background: #059669;
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

/* 통계 대시보드 */
.stats-dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.2s;
}

.stat-card:hover {
  border-color: #cbd5e0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stat-card.today {
  border-color: #3182ce;
  background: linear-gradient(135deg, #ebf8ff 0%, #ffffff 100%);
}

.stat-card.upcoming {
  border-color: #f59e0b;
  background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%);
}

.stat-card.ongoing {
  border-color: #10b981;
  background: linear-gradient(135deg, #f0fff4 0%, #ffffff 100%);
}

.stat-icon {
  font-size: 2rem;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #1a202c;
}

.stat-label {
  color: #718096;
  font-size: 0.875rem;
}

/* 섹션 */
.today-section {
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

.today-events {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

/* 검색 및 필터 */
.search-filter-section {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 250px;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 1rem;
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

.filter-controls {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.filter-select, .date-input {
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  background: white;
  cursor: pointer;
  outline: none;
  transition: border-color 0.2s;
}

.filter-select:focus, .date-input:focus {
  border-color: #3182ce;
}

/* 리스트 뷰 */
.list-view {
  min-height: 400px;
}

.events-list {
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
  background: #10b981;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.2s;
}

.create-empty-btn:hover {
  background: #059669;
}

/* 월간 뷰 */
.month-view {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  overflow: hidden;
}

.month-header {
  display: flex;
  justify-content: between;
  align-items: center;
  padding: 1rem;
  background: #f7fafc;
  border-bottom: 1px solid #e2e8f0;
}

.month-nav-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.375rem;
  transition: background 0.2s;
}

.month-nav-btn:hover {
  background: #edf2f7;
}

.month-title {
  flex: 1;
  text-align: center;
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.calendar-grid {
  display: flex;
  flex-direction: column;
}

.weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  background: #f7fafc;
  border-bottom: 1px solid #e2e8f0;
}

.weekday {
  padding: 1rem;
  text-align: center;
  font-weight: 600;
  color: #4a5568;
}

.days-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
}

.day-cell {
  min-height: 120px;
  border-right: 1px solid #e2e8f0;
  border-bottom: 1px solid #e2e8f0;
  padding: 0.5rem;
  cursor: pointer;
  transition: background 0.2s;
}

.day-cell:hover {
  background: #f7fafc;
}

.day-cell.other-month {
  color: #a0aec0;
  background: #fafafa;
}

.day-cell.today {
  background: #ebf8ff;
}

.day-cell.selected {
  background: #e6fffa;
  border-color: #319795;
}

.day-cell.has-events {
  background: #f0fff4;
}

.day-number {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.day-events {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.day-event {
  padding: 0.125rem 0.25rem;
  border-radius: 0.125rem;
  font-size: 0.75rem;
  color: white;
  cursor: pointer;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.more-events {
  font-size: 0.625rem;
  color: #6b7280;
  text-align: center;
  margin-top: 0.125rem;
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
  .calendar-view {
    padding: 1rem;
  }
  
  .calendar-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .calendar-controls {
    width: 100%;
    justify-content: stretch;
  }
  
  .search-filter-section {
    flex-direction: column;
  }
  
  .filter-controls {
    justify-content: stretch;
  }
  
  .filter-select, .date-input {
    flex: 1;
  }
  
  .stats-dashboard {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .today-events {
    grid-template-columns: 1fr;
  }
  
  .day-cell {
    min-height: 80px;
  }
}
</style> 