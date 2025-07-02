<template>
  <div class="modal-overlay" @click.self="handleClose">
    <div class="modal-container">
      <!-- 모달 헤더 -->
      <div class="modal-header">
        <h2 class="modal-title">
          <span class="modal-icon">{{ isEdit ? '✏️' : '➕' }}</span>
          {{ isEdit ? '일정 수정' : '새 일정 등록' }}
        </h2>
        <button @click="handleClose" class="close-btn" title="닫기">
          ×
        </button>
      </div>

      <!-- 모달 내용 -->
      <form @submit.prevent="handleSubmit" class="modal-content">
        <!-- 제목 -->
        <div class="form-group">
          <label for="title" class="form-label">
            일정 제목 <span class="required">*</span>
          </label>
          <input
            id="title"
            v-model="form.title"
            type="text"
            class="form-input"
            :class="{ error: errors.title }"
            placeholder="일정 제목을 입력하세요"
            maxlength="200"
            required
          />
          <div v-if="errors.title" class="error-message">{{ errors.title }}</div>
        </div>

        <!-- 일정 타입 -->
        <div class="form-group">
          <label for="event_type" class="form-label">
            일정 타입 <span class="required">*</span>
          </label>
          <select
            id="event_type"
            v-model="form.event_type"
            class="form-select"
            :class="{ error: errors.event_type }"
            required
          >
            <option value="">일정 타입을 선택하세요</option>
            <option
              v-for="type in eventTypes"
              :key="type.value"
              :value="type.value"
            >
              {{ type.icon }} {{ type.label }}
            </option>
          </select>
          <div v-if="errors.event_type" class="error-message">{{ errors.event_type }}</div>
        </div>

        <!-- 날짜 및 시간 -->
        <div class="form-group">
          <div class="checkbox-wrapper">
            <label class="checkbox-label">
              <input
                v-model="form.all_day"
                type="checkbox"
                class="form-checkbox"
              />
              <span class="checkbox-text">📅 종일 일정</span>
            </label>
          </div>
        </div>

        <div class="datetime-grid">
          <!-- 시작 날짜 -->
          <div class="form-group">
            <label for="start_date" class="form-label">
              시작 날짜 <span class="required">*</span>
            </label>
            <input
              id="start_date"
              v-model="form.start_date"
              type="date"
              class="form-input"
              :class="{ error: errors.start_date }"
              required
            />
            <div v-if="errors.start_date" class="error-message">{{ errors.start_date }}</div>
          </div>

          <!-- 시작 시간 -->
          <div v-if="!form.all_day" class="form-group">
            <label for="start_time" class="form-label">
              시작 시간 <span class="required">*</span>
            </label>
            <input
              id="start_time"
              v-model="form.start_time"
              type="time"
              class="form-input"
              :class="{ error: errors.start_time }"
              required
            />
            <div v-if="errors.start_time" class="error-message">{{ errors.start_time }}</div>
          </div>

          <!-- 종료 날짜 -->
          <div class="form-group">
            <label for="end_date" class="form-label">종료 날짜</label>
            <input
              id="end_date"
              v-model="form.end_date"
              type="date"
              class="form-input"
              :min="form.start_date"
            />
          </div>

          <!-- 종료 시간 -->
          <div v-if="!form.all_day" class="form-group">
            <label for="end_time" class="form-label">종료 시간</label>
            <input
              id="end_time"
              v-model="form.end_time"
              type="time"
              class="form-input"
            />
          </div>
        </div>

        <!-- 설명 -->
        <div class="form-group">
          <label for="description" class="form-label">설명</label>
          <textarea
            id="description"
            v-model="form.description"
            class="form-textarea"
            placeholder="일정에 대한 설명을 입력하세요"
            rows="4"
            maxlength="1000"
          ></textarea>
          <div class="input-help">{{ form.description.length }}/1000자</div>
        </div>

        <!-- 장소 -->
        <div class="form-group">
          <label for="location" class="form-label">
            📍 장소
          </label>
          <input
            id="location"
            v-model="form.location"
            type="text"
            class="form-input"
            placeholder="장소를 입력하세요"
            maxlength="200"
          />
        </div>

        <!-- 참가자 -->
        <div class="form-group">
          <label for="participants" class="form-label">
            👥 참가자
          </label>
          <input
            id="participants"
            v-model="form.participants"
            type="text"
            class="form-input"
            placeholder="참가자를 입력하세요 (쉼표로 구분)"
            maxlength="500"
          />
          <div class="input-help">쉼표(,)로 구분하여 여러 명 입력 가능</div>
        </div>

        <!-- 색상 -->
        <div class="form-group">
          <label for="color" class="form-label">🎨 색상</label>
          <div class="color-picker">
            <input
              id="color"
              v-model="form.color"
              type="color"
              class="color-input"
            />
            <span class="color-preview" :style="{ backgroundColor: form.color }"></span>
            <span class="color-text">{{ form.color }}</span>
          </div>
        </div>

        <!-- 반복 일정 -->
        <div class="form-group">
          <div class="checkbox-wrapper">
            <label class="checkbox-label">
              <input
                v-model="form.is_recurring"
                type="checkbox"
                class="form-checkbox"
              />
              <span class="checkbox-text">🔄 반복 일정</span>
            </label>
          </div>
          
          <div v-if="form.is_recurring" class="recurrence-options">
            <select v-model="form.recurrence_rule" class="form-select">
              <option value="">반복 규칙 선택</option>
              <option value="daily">매일</option>
              <option value="weekly">매주</option>
              <option value="monthly">매월</option>
              <option value="yearly">매년</option>
            </select>
          </div>
        </div>

        <!-- 에러 메시지 -->
        <div v-if="formError" class="form-error">
          <span class="error-icon">❌</span>
          {{ formError }}
        </div>

        <!-- 액션 버튼 -->
        <div class="modal-actions">
          <button
            type="button"
            @click="handleClose"
            class="action-btn cancel-btn"
            :disabled="submitting"
          >
            취소
          </button>
          
          <button
            type="submit"
            class="action-btn submit-btn"
            :disabled="submitting || !isFormValid"
            :class="{ loading: submitting }"
          >
            <span v-if="submitting" class="loading-spinner">⏳</span>
            <span v-else class="submit-icon">{{ isEdit ? '💾' : '➕' }}</span>
            {{ submitting ? '저장 중...' : (isEdit ? '수정하기' : '등록하기') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { EventType } from '@/types/calendar'
import type { EventResponse, EventCreate, EventUpdate, EventTypeInfo } from '@/types/calendar'

// Props 정의
interface Props {
  event?: EventResponse | null
  eventTypes: EventTypeInfo[]
}

const props = withDefaults(defineProps<Props>(), {
  event: null
})

// Events 정의
const emit = defineEmits<{
  save: [data: EventCreate | EventUpdate]
  close: []
}>()

// 상태
const submitting = ref(false)
const formError = ref('')

// 폼 데이터
const form = ref({
  title: '',
  description: '',
  event_type: '' as EventType | '',
  start_date: '',
  start_time: '09:00',
  end_date: '',
  end_time: '10:00',
  all_day: false,
  location: '',
  participants: '',
  is_recurring: false,
  recurrence_rule: '',
  color: '#3B82F6'
})

// 폼 검증 에러
const errors = ref({
  title: '',
  event_type: '',
  start_date: '',
  start_time: ''
})

// 계산된 속성
const isEdit = computed(() => !!props.event)

const isFormValid = computed(() => {
  return form.value.title.trim() && 
         form.value.event_type &&
         form.value.start_date &&
         (form.value.all_day || form.value.start_time) &&
         !Object.values(errors.value).some(error => error)
})

// 메서드
const validateForm = () => {
  errors.value = {
    title: '',
    event_type: '',
    start_date: '',
    start_time: ''
  }

  if (!form.value.title.trim()) {
    errors.value.title = '제목을 입력해주세요.'
  } else if (form.value.title.length > 200) {
    errors.value.title = '제목은 200자 이하로 입력해주세요.'
  }

  if (!form.value.event_type) {
    errors.value.event_type = '일정 타입을 선택해주세요.'
  }

  if (!form.value.start_date) {
    errors.value.start_date = '시작 날짜를 선택해주세요.'
  }

  if (!form.value.all_day && !form.value.start_time) {
    errors.value.start_time = '시작 시간을 선택해주세요.'
  }

  // 종료 날짜가 시작 날짜보다 이른 경우 체크
  if (form.value.end_date && form.value.end_date < form.value.start_date) {
    errors.value.start_date = '종료 날짜는 시작 날짜보다 이후여야 합니다.'
  }

  return !Object.values(errors.value).some(error => error)
}

const handleSubmit = async () => {
  if (!validateForm()) return

  submitting.value = true
  formError.value = ''

  try {
    // ISO 형식으로 변환
    let start_time: string
    let end_time: string | undefined

    if (form.value.all_day) {
      start_time = `${form.value.start_date}T00:00:00`
      end_time = form.value.end_date ? `${form.value.end_date}T23:59:59` : undefined
    } else {
      start_time = `${form.value.start_date}T${form.value.start_time}:00`
      end_time = form.value.end_date && form.value.end_time 
        ? `${form.value.end_date}T${form.value.end_time}:00` 
        : undefined
    }

    const data = {
      title: form.value.title.trim(),
      description: form.value.description.trim() || undefined,
      event_type: form.value.event_type as EventType,
      start_time,
      end_time,
      all_day: form.value.all_day,
      location: form.value.location.trim() || undefined,
      participants: form.value.participants.trim() || undefined,
      is_recurring: form.value.is_recurring,
      recurrence_rule: form.value.is_recurring ? form.value.recurrence_rule || undefined : undefined,
      color: form.value.color || undefined
    }

    emit('save', data)
  } catch (error) {
    console.error('폼 제출 에러:', error)
    formError.value = '저장 중 오류가 발생했습니다. 다시 시도해주세요.'
  } finally {
    submitting.value = false
  }
}

const handleClose = () => {
  if (submitting.value) return
  emit('close')
}

const initializeForm = () => {
  if (props.event) {
    // 수정 모드
    const startDate = new Date(props.event.start_time)
    const endDate = props.event.end_time ? new Date(props.event.end_time) : null

    form.value = {
      title: props.event.title,
      description: props.event.description || '',
      event_type: props.event.event_type,
      start_date: startDate.toISOString().split('T')[0],
      start_time: startDate.toTimeString().slice(0, 5),
      end_date: endDate ? endDate.toISOString().split('T')[0] : '',
      end_time: endDate ? endDate.toTimeString().slice(0, 5) : '10:00',
      all_day: props.event.all_day,
      location: props.event.location || '',
      participants: props.event.participants || '',
      is_recurring: props.event.is_recurring,
      recurrence_rule: props.event.recurrence_rule || '',
      color: props.event.color || '#3B82F6'
    }
  } else {
    // 생성 모드 - 오늘 날짜로 초기화
    const today = new Date().toISOString().split('T')[0]
    
    form.value = {
      title: '',
      description: '',
      event_type: '',
      start_date: today,
      start_time: '09:00',
      end_date: '',
      end_time: '10:00',
      all_day: false,
      location: '',
      participants: '',
      is_recurring: false,
      recurrence_rule: '',
      color: '#3B82F6'
    }
  }
  
  errors.value = {
    title: '',
    event_type: '',
    start_date: '',
    start_time: ''
  }
  formError.value = ''
}

// 종일 일정 토글 시 기본 시간 설정
watch(() => form.value.all_day, (isAllDay) => {
  if (isAllDay) {
    form.value.start_time = '00:00'
    form.value.end_time = '23:59'
  } else {
    form.value.start_time = '09:00'
    form.value.end_time = '10:00'
  }
})

// 시작 날짜 변경 시 종료 날짜 자동 조정
watch(() => form.value.start_date, (newDate) => {
  if (!form.value.end_date || form.value.end_date < newDate) {
    form.value.end_date = newDate
  }
})

// 컴포넌트 마운트 시 초기화
onMounted(() => {
  initializeForm()
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-container {
  background: white;
  border-radius: 1rem;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

/* 모달 헤더 */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  background: #f9fafb;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.close-btn {
  width: 2rem;
  height: 2rem;
  border: none;
  background: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  border-radius: 0.375rem;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #e5e7eb;
  color: #374151;
}

/* 모달 내용 */
.modal-content {
  padding: 1.5rem;
  max-height: calc(90vh - 120px);
  overflow-y: auto;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.required {
  color: #ef4444;
}

.form-input, .form-textarea, .form-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.2s;
  outline: none;
}

.form-input:focus, .form-textarea:focus, .form-select:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input.error, .form-textarea.error, .form-select.error {
  border-color: #ef4444;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.input-help {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.error-message {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

/* 날짜/시간 그리드 */
.datetime-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

/* 체크박스 */
.checkbox-wrapper {
  margin-bottom: 1rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
}

.form-checkbox {
  width: 1.25rem;
  height: 1.25rem;
  cursor: pointer;
}

.checkbox-text {
  font-weight: 500;
  color: #374151;
}

/* 색상 선택기 */
.color-picker {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.color-input {
  width: 3rem;
  height: 3rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  cursor: pointer;
}

.color-preview {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  border: 1px solid #d1d5db;
}

.color-text {
  font-family: monospace;
  font-size: 0.875rem;
  color: #6b7280;
}

/* 반복 옵션 */
.recurrence-options {
  margin-top: 0.75rem;
}

/* 폼 에러 */
.form-error {
  background: #fef2f2;
  color: #dc2626;
  padding: 1rem;
  border-radius: 0.5rem;
  border: 1px solid #fecaca;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* 액션 버튼 */
.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.action-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cancel-btn {
  background: #6b7280;
  color: white;
}

.cancel-btn:hover:not(:disabled) {
  background: #4b5563;
}

.submit-btn {
  background: #10b981;
  color: white;
}

.submit-btn:hover:not(:disabled) {
  background: #059669;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.submit-btn.loading {
  background: #6b7280;
}

.loading-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 반응형 */
@media (max-width: 768px) {
  .modal-overlay {
    padding: 0.5rem;
  }

  .modal-container {
    max-height: 95vh;
  }

  .modal-header {
    padding: 1rem;
  }

  .modal-title {
    font-size: 1.25rem;
  }

  .modal-content {
    padding: 1rem;
  }

  .datetime-grid {
    grid-template-columns: 1fr;
  }

  .modal-actions {
    flex-direction: column-reverse;
  }

  .action-btn {
    width: 100%;
    justify-content: center;
  }

  .color-picker {
    flex-wrap: wrap;
  }
}
</style> 