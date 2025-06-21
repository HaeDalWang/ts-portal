<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 헤더 -->
    <div class="bg-gradient-to-r from-purple-500 to-blue-600 px-6 py-4 text-white rounded-b-xl">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-xl font-bold text-white">내 프로필</h1>
          <p class="text-sm text-purple-100">개인 정보 및 계정 설정</p>
        </div>
        <div class="flex items-center space-x-3">
          <div class="text-center">
            <div class="text-sm font-semibold text-white">{{ currentUser?.role || 'user' }}</div>
            <div class="text-xs text-purple-100">권한</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 메인 컨텐츠 -->
    <div class="p-6">
      <div class="max-w-4xl mx-auto">
        <!-- 프로필 카드 -->
        <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
          <!-- 프로필 헤더 -->
          <div class="bg-gradient-to-r from-purple-50 to-blue-50 px-6 py-6">
            <div class="flex items-center space-x-6">
              <!-- 프로필 이미지 -->
              <div class="relative">
                <div class="w-20 h-20 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center text-white text-2xl font-bold">
                  {{ userInitials }}
                </div>
              </div>
              
              <!-- 기본 정보 -->
              <div class="flex-1">
                <h2 class="text-xl font-bold text-gray-900">{{ currentUser?.name || '사용자' }}</h2>
                <p class="text-sm text-gray-600">{{ currentUser?.email || '' }}</p>
                <div class="flex items-center space-x-4 mt-2">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                    {{ currentUser?.team || 'TS팀' }}
                  </span>
                  <span class="text-xs text-gray-500">
                    가입일: {{ formatDate(currentUser?.created_at) }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- 탭 메뉴 -->
          <div class="border-b border-gray-200">
            <nav class="flex space-x-8 px-6">
              <button
                v-for="tab in tabs"
                :key="tab.id"
                @click="activeTab = tab.id"
                :class="[
                  'py-4 px-1 border-b-2 font-medium text-sm transition-colors',
                  activeTab === tab.id
                    ? 'border-purple-500 text-purple-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                ]"
              >
                {{ tab.name }}
              </button>
            </nav>
          </div>

          <!-- 탭 컨텐츠 -->
          <div class="p-6">
            <!-- 기본 정보 탭 -->
            <div v-if="activeTab === 'basic'" class="space-y-6">
              <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div class="flex">
                  <svg class="w-5 h-5 text-blue-400 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <div class="flex-1">
                    <h3 class="text-sm font-medium text-blue-800">프로필 정보</h3>
                    <p class="text-sm text-blue-700 mt-1">이메일, 연락처, 기술스택은 직접 수정할 수 있습니다. 다른 정보는 관리자에게 문의하세요.</p>
                  </div>
                  <button
                    @click="toggleEditMode"
                    :disabled="isLoading"
                    class="ml-4 px-3 py-1 text-xs font-medium rounded-md transition-colors disabled:opacity-50"
                    :class="isEditing ? 'bg-gray-200 text-gray-700 hover:bg-gray-300' : 'bg-blue-100 text-blue-700 hover:bg-blue-200'"
                  >
                    {{ isEditing ? '취소' : '편집' }}
                  </button>
                </div>
              </div>

              <form @submit.prevent="saveProfile" class="space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <!-- 이름 (읽기 전용) -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">이름</label>
                    <div class="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 text-sm text-gray-600">
                      {{ currentUser?.name || '정보 없음' }}
                    </div>
                  </div>

                  <!-- 이메일 (편집 가능) -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">
                      이메일
                      <span class="text-green-600 text-xs ml-1">✓ 편집 가능</span>
                    </label>
                    <input
                      v-if="isEditing"
                      v-model="profileForm.email"
                      type="email"
                      required
                      :disabled="isLoading"
                      class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent text-sm"
                    />
                    <div
                      v-else
                      class="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 text-sm text-gray-600"
                    >
                      {{ currentUser?.email || '정보 없음' }}
                    </div>
                  </div>

                  <!-- 연락처 (편집 가능) -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">
                      연락처
                      <span class="text-green-600 text-xs ml-1">✓ 편집 가능</span>
                    </label>
                    <input
                      v-if="isEditing"
                      v-model="profileForm.phone"
                      type="tel"
                      placeholder="010-1234-5678"
                      :disabled="isLoading"
                      class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent text-sm"
                    />
                    <div
                      v-else
                      class="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 text-sm text-gray-600"
                    >
                      {{ currentUser?.phone || '정보 없음' }}
                    </div>
                  </div>

                  <!-- 직급 (읽기 전용) -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">직급</label>
                    <div class="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 text-sm text-gray-600">
                      {{ currentUser?.position || '정보 없음' }}
                    </div>
                  </div>
                </div>

                <!-- 기술 스택 (편집 가능) -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    기술 스택
                    <span class="text-green-600 text-xs ml-1">✓ 편집 가능</span>
                  </label>
                  
                  <div v-if="isEditing" class="space-y-3">
                    <input
                      v-model="profileForm.skills"
                      type="text"
                      placeholder="AWS, Kubernetes, Python (쉼표로 구분)"
                      :disabled="isLoading"
                      class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent text-sm"
                    />
                    <p class="text-xs text-gray-500">쉼표(,)로 구분하여 입력해주세요. 예: AWS, Kubernetes, Python</p>
                  </div>
                  
                  <div v-else class="flex flex-wrap gap-2">
                    <span
                      v-for="skill in currentUser?.skills_list || []"
                      :key="skill"
                      class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800"
                    >
                      {{ skill }}
                    </span>
                    <span v-if="!currentUser?.skills_list?.length" class="text-sm text-gray-500">
                      등록된 기술 스택이 없습니다.
                    </span>
                  </div>
                </div>

                <!-- 저장 버튼 (편집 모드일 때만 표시) -->
                <div v-if="isEditing" class="flex justify-end space-x-3">
                  <button
                    type="button"
                    @click="cancelEdit"
                    :disabled="isLoading"
                    class="px-4 py-2 text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors text-sm font-medium disabled:opacity-50"
                  >
                    취소
                  </button>
                  <button
                    type="submit"
                    :disabled="isLoading || !isProfileFormValid"
                    class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-sm font-medium disabled:opacity-50"
                  >
                    <span v-if="isLoading">저장 중...</span>
                    <span v-else>저장</span>
                  </button>
                </div>
              </form>
            </div>

            <!-- 보안 설정 탭 -->
            <div v-if="activeTab === 'security'" class="space-y-6">
              <form @submit.prevent="changePassword" class="space-y-6">
                <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <div class="flex">
                    <svg class="w-5 h-5 text-yellow-400 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                    </svg>
                    <div>
                      <h3 class="text-sm font-medium text-yellow-800">비밀번호 변경</h3>
                      <p class="text-sm text-yellow-700 mt-1">보안을 위해 정기적으로 비밀번호를 변경해주세요.</p>
                    </div>
                  </div>
                </div>

                <div class="space-y-4">
                  <!-- 현재 비밀번호 -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">현재 비밀번호</label>
                    <input
                      v-model="passwordForm.currentPassword"
                      type="password"
                      class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent text-sm"
                      :disabled="isLoading"
                    />
                  </div>

                  <!-- 새 비밀번호 -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">새 비밀번호</label>
                    <input
                      v-model="passwordForm.newPassword"
                      type="password"
                      class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent text-sm"
                      :disabled="isLoading"
                    />
                    <p class="text-xs text-gray-500 mt-1">최소 6자 이상 입력해주세요.</p>
                  </div>

                  <!-- 새 비밀번호 확인 -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">새 비밀번호 확인</label>
                    <input
                      v-model="passwordForm.confirmPassword"
                      type="password"
                      class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent text-sm"
                      :disabled="isLoading"
                    />
                  </div>
                </div>

                <!-- 변경 버튼 -->
                <div class="flex justify-end">
                  <button
                    type="submit"
                    :disabled="isLoading || !isPasswordFormValid"
                    class="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-sm font-medium disabled:opacity-50"
                  >
                    <span v-if="isLoading">변경 중...</span>
                    <span v-else>비밀번호 변경</span>
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 성공/에러 메시지 -->
    <div
      v-if="message"
      :class="[
        'fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 transition-all duration-300',
        messageType === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
      ]"
    >
      {{ message }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
import authService from '@/services/authService'
import type { User } from '@/services/authService'

// 반응형 상태
const currentUser = ref<User | null>(null)
const isLoading = ref(false)
const isEditing = ref(false)
const activeTab = ref('basic')
const message = ref('')
const messageType = ref<'success' | 'error'>('success')

// 탭 정의
const tabs = [
  { id: 'basic', name: '기본 정보' },
  { id: 'security', name: '보안 설정' }
]

// 비밀번호 변경 폼
const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 기본 정보 폼
const profileForm = reactive({
  email: '',
  phone: '',
  skills: ''
})

// 계산된 속성
const userInitials = computed(() => {
  if (!currentUser.value?.name) return 'U'
  return currentUser.value.name
    .split(' ')
    .map(word => word.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2)
})

const isPasswordFormValid = computed(() => {
  return passwordForm.currentPassword &&
         passwordForm.newPassword &&
         passwordForm.confirmPassword &&
         passwordForm.newPassword === passwordForm.confirmPassword &&
         passwordForm.newPassword.length >= 6
})

const isProfileFormValid = computed(() => {
  return profileForm.email.trim() !== ''
})

// 메서드
const loadUserProfile = async () => {
  try {
    isLoading.value = true
    currentUser.value = await authService.getMyInfo()
    
    // 편집 폼에 현재 사용자 정보 설정
    if (currentUser.value) {
      profileForm.email = currentUser.value.email || ''
      profileForm.phone = currentUser.value.phone || ''
      profileForm.skills = currentUser.value.skills_list?.join(', ') || ''
    }
  } catch (error) {
    showMessage('프로필 정보를 불러올 수 없습니다.', 'error')
  } finally {
    isLoading.value = false
  }
}

const changePassword = async () => {
  try {
    isLoading.value = true
    await authService.changePassword(passwordForm.currentPassword, passwordForm.newPassword)
    
    // 폼 초기화
    passwordForm.currentPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
    
    showMessage('비밀번호가 성공적으로 변경되었습니다.', 'success')
  } catch (error) {
    showMessage('비밀번호 변경에 실패했습니다.', 'error')
  } finally {
    isLoading.value = false
  }
}

const formatDate = (dateString?: string) => {
  if (!dateString) return '정보 없음'
  return new Date(dateString).toLocaleDateString('ko-KR')
}

const showMessage = (text: string, type: 'success' | 'error') => {
  message.value = text
  messageType.value = type
  setTimeout(() => {
    message.value = ''
  }, 3000)
}

const toggleEditMode = () => {
  if (isEditing.value) {
    // 편집 모드 취소 시 원래 값으로 복원
    if (currentUser.value) {
      profileForm.email = currentUser.value.email || ''
      profileForm.phone = currentUser.value.phone || ''
      profileForm.skills = currentUser.value.skills_list?.join(', ') || ''
    }
  }
  isEditing.value = !isEditing.value
}

const saveProfile = async () => {
  try {
    isLoading.value = true
    
    // 기술스택을 배열로 변환 (쉼표로 분리하고 공백 제거)
    const skillsArray = profileForm.skills
      .split(',')
      .map(skill => skill.trim())
      .filter(skill => skill.length > 0)
    
    const updatedUser = await authService.updateMyInfo({
      email: profileForm.email,
      phone: profileForm.phone,
      skills: skillsArray
    })
    
    // 현재 사용자 정보 업데이트
    currentUser.value = updatedUser
    
    // 편집 모드 종료
    isEditing.value = false
    
    showMessage('프로필이 성공적으로 저장되었습니다.', 'success')
  } catch (error: any) {
    showMessage(error.message || '프로필 저장에 실패했습니다.', 'error')
  } finally {
    isLoading.value = false
  }
}

const cancelEdit = () => {
  // 편집 모드 취소
  toggleEditMode()
}

// 컴포넌트 마운트 시 실행
onMounted(() => {
  loadUserProfile()
})
</script> 