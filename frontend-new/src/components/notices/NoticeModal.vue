<template>
  <div class="modal-overlay" @click.self="handleClose">
    <div class="modal-container">
      <!-- 모달 헤더 -->
      <div class="modal-header">
        <h2 class="modal-title">
          <span class="modal-icon">{{ isEdit ? '✏️' : '➕' }}</span>
          {{ isEdit ? '공지사항 수정' : '새 공지사항 작성' }}
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
            제목 <span class="required">*</span>
          </label>
          <input
            id="title"
            v-model="form.title"
            type="text"
            class="form-input"
            :class="{ error: errors.title }"
            placeholder="공지사항 제목을 입력하세요"
            maxlength="200"
            required
          />
          <div v-if="errors.title" class="error-message">{{ errors.title }}</div>
          <div class="input-help">{{ form.title.length }}/200자</div>
        </div>

        <!-- 내용 -->
        <div class="form-group">
          <label for="content" class="form-label">
            내용 <span class="required">*</span>
          </label>
          <textarea
            id="content"
            v-model="form.content"
            class="form-textarea"
            :class="{ error: errors.content }"
            placeholder="공지사항 내용을 입력하세요"
            rows="8"
            maxlength="5000"
            required
          ></textarea>
          <div v-if="errors.content" class="error-message">{{ errors.content }}</div>
          <div class="input-help">{{ form.content.length }}/5000자</div>
        </div>

        <!-- 우선순위 -->
        <div class="form-group">
          <label for="priority" class="form-label">
            우선순위 <span class="required">*</span>
          </label>
          <select
            id="priority"
            v-model="form.priority"
            class="form-select"
            :class="{ error: errors.priority }"
            required
          >
            <option value="">우선순위를 선택하세요</option>
            <option
              v-for="priority in availablePriorities"
              :key="priority.value"
              :value="priority.value"
            >
              {{ priority.icon }} {{ priority.label }}
            </option>
          </select>
          <div v-if="errors.priority" class="error-message">{{ errors.priority }}</div>
          <div class="priority-help">
            <div class="help-item">
              <span class="help-icon">ℹ️</span>
              <span class="help-text">일반: 누구나 생성 가능</span>
            </div>
            <div class="help-item">
              <span class="help-icon">⚠️</span>
              <span class="help-text">Warning: Power User 이상</span>
            </div>
            <div class="help-item">
              <span class="help-icon">🚨</span>
              <span class="help-text">긴급: 관리자 전용</span>
            </div>
          </div>
        </div>

        <!-- 고정 옵션 -->
        <div class="form-group">
          <label class="checkbox-label">
            <input
              v-model="form.is_pinned"
              type="checkbox"
              class="form-checkbox"
            />
            <span class="checkbox-text">
              📌 이 공지사항을 상단에 고정
            </span>
          </label>
          <div class="checkbox-help">
            고정된 공지사항은 목록 상단에 항상 표시됩니다.
          </div>
        </div>

        <!-- 활성화 옵션 -->
        <div class="form-group">
          <label class="checkbox-label">
            <input
              v-model="form.is_active"
              type="checkbox"
              class="form-checkbox"
            />
            <span class="checkbox-text">
              ✅ 공지사항 활성화
            </span>
          </label>
          <div class="checkbox-help">
            비활성화된 공지사항은 목록에 표시되지 않습니다.
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
            {{ submitting ? '저장 중...' : (isEdit ? '수정하기' : '작성하기') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useAuth } from '@/composables/useAuth'
import { NoticePriority } from '@/types/notices'
import type { NoticeResponse, NoticeCreate, NoticeUpdate, PriorityInfo } from '@/types/notices'

// Props 정의
interface Props {
  notice?: NoticeResponse | null
  priorities: PriorityInfo[]
}

const props = withDefaults(defineProps<Props>(), {
  notice: null
})

// Events 정의
const emit = defineEmits<{
  save: [data: NoticeCreate | NoticeUpdate]
  close: []
}>()

// 상태
const submitting = ref(false)
const formError = ref('')

// 폼 데이터
const form = ref({
  title: '',
  content: '',
  priority: '' as NoticePriority | '',
  is_pinned: false,
  is_active: true
})

// 폼 검증 에러
const errors = ref({
  title: '',
  content: '',
  priority: ''
})

// Composables
const { user } = useAuth()

// 계산된 속성
const isEdit = computed(() => !!props.notice)

const availablePriorities = computed(() => {
  if (!user.value) return []

  return props.priorities.filter(priority => {
    switch (priority.value) {
      case NoticePriority.NORMAL:
        return true // 누구나 가능
      case NoticePriority.CAUTION:
        return ['power_user', 'admin'].includes(user.value!.role.toLowerCase())
      case NoticePriority.IMPORTANT:
        return user.value!.role.toLowerCase() === 'admin'
      default:
        return false
    }
  })
})

const isFormValid = computed(() => {
  return form.value.title.trim() && 
         form.value.content.trim() && 
         form.value.priority &&
         !Object.values(errors.value).some(error => error)
})

// 메서드
const validateForm = () => {
  errors.value = {
    title: '',
    content: '',
    priority: ''
  }

  if (!form.value.title.trim()) {
    errors.value.title = '제목을 입력해주세요.'
  } else if (form.value.title.length > 200) {
    errors.value.title = '제목은 200자 이하로 입력해주세요.'
  }

  if (!form.value.content.trim()) {
    errors.value.content = '내용을 입력해주세요.'
  } else if (form.value.content.length > 5000) {
    errors.value.content = '내용은 5000자 이하로 입력해주세요.'
  }

  if (!form.value.priority) {
    errors.value.priority = '우선순위를 선택해주세요.'
  } else {
    // 권한 체크
    const priority = form.value.priority
    const userRole = user.value?.role.toLowerCase()
    
    if (priority === NoticePriority.CAUTION && !['power_user', 'admin'].includes(userRole || '')) {
      errors.value.priority = 'Warning 공지사항은 Power User 이상만 생성할 수 있습니다.'
    } else if (priority === NoticePriority.IMPORTANT && userRole !== 'admin') {
      errors.value.priority = '긴급 공지사항은 관리자만 생성할 수 있습니다.'
    }
  }

  return !Object.values(errors.value).some(error => error)
}

const handleSubmit = async () => {
  if (!validateForm()) return

  submitting.value = true
  formError.value = ''

  try {
    const data = {
      title: form.value.title.trim(),
      content: form.value.content.trim(),
      priority: form.value.priority as NoticePriority,
      is_pinned: form.value.is_pinned,
      is_active: form.value.is_active
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
  if (props.notice) {
    // 수정 모드
    form.value = {
      title: props.notice.title,
      content: props.notice.content,
      priority: props.notice.priority,
      is_pinned: props.notice.is_pinned,
      is_active: props.notice.is_active
    }
  } else {
    // 생성 모드
    form.value = {
      title: '',
      content: '',
      priority: '',
      is_pinned: false,
      is_active: true
    }
  }
  
  errors.value = {
    title: '',
    content: '',
    priority: ''
  }
  formError.value = ''
}

// 폼 필드 변경 시 실시간 검증
watch([() => form.value.title, () => form.value.content, () => form.value.priority], () => {
  // 에러가 있던 필드만 다시 검증
  if (errors.value.title && form.value.title.trim()) {
    errors.value.title = form.value.title.length > 200 ? '제목은 200자 이하로 입력해주세요.' : ''
  }
  if (errors.value.content && form.value.content.trim()) {
    errors.value.content = form.value.content.length > 5000 ? '내용은 5000자 이하로 입력해주세요.' : ''
  }
  if (errors.value.priority && form.value.priority) {
    validateForm() // 우선순위는 권한 체크가 필요하므로 전체 검증
  }
})

// 컴포넌트 마운트 시 초기화
onMounted(() => {
  initializeForm()
})

// ESC 키로 모달 닫기
const handleKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Escape' && !submitting.value) {
    handleClose()
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeyDown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown)
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
  min-height: 120px;
}

.input-help {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.25rem;
  text-align: right;
}

.error-message {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

/* 우선순위 도움말 */
.priority-help {
  margin-top: 0.5rem;
  padding: 0.75rem;
  background: #f8fafc;
  border-radius: 0.5rem;
  border: 1px solid #e2e8f0;
}

.help-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #4b5563;
  margin-bottom: 0.25rem;
}

.help-item:last-child {
  margin-bottom: 0;
}

/* 체크박스 */
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

.checkbox-help {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.5rem;
  margin-left: 2rem;
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
  background: #3b82f6;
  color: white;
}

.submit-btn:hover:not(:disabled) {
  background: #2563eb;
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

  .modal-actions {
    flex-direction: column-reverse;
  }

  .action-btn {
    width: 100%;
    justify-content: center;
  }

  .checkbox-help {
    margin-left: 0;
  }
}
</style> 