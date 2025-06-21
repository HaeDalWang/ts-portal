<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 헤더 -->
    <div class="bg-gradient-to-r from-red-500 to-orange-600 px-6 py-4 text-white rounded-b-xl">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-xl font-bold text-white">🔧 관리자 페이지</h1>
          <p class="text-sm text-red-100">팀원 관리 및 시스템 설정</p>
        </div>
        <div class="flex items-center space-x-6">
          <div class="text-center">
            <div class="text-lg font-bold text-white">{{ totalMembers }}</div>
            <div class="text-xs text-red-100">전체 팀원</div>
          </div>
          <div class="text-center">
            <div class="text-lg font-bold text-white">{{ activeMembers }}</div>
            <div class="text-xs text-red-100">활성 팀원</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 메인 컨텐츠 -->
    <div class="p-6">
      <div class="max-w-7xl mx-auto">
        <!-- 액션 버튼들 -->
        <div class="mb-6 flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <!-- 팀원 추가 버튼 (관리자만) -->
            <button
              v-if="canUserCreateMembers"
              @click="showCreateModal = true"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium flex items-center space-x-2"
            >
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              <span>팀원 추가</span>
            </button>
            
            <button
              @click="loadMembers"
              :disabled="isLoading"
              class="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors text-sm font-medium flex items-center space-x-2 disabled:opacity-50"
            >
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <span>새로고침</span>
            </button>
          </div>

          <!-- 검색 -->
          <div class="flex items-center space-x-4">
            <div class="relative">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="이름 또는 이메일로 검색..."
                class="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm w-64"
              />
              <svg class="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- 팀원 목록 테이블 -->
        <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">팀원 정보</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">연락처</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">직급/팀</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">권한</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">상태</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">액션</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="member in filteredMembers" :key="member.id" class="hover:bg-gray-50">
                  <!-- 팀원 정보 -->
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white text-sm font-bold">
                        {{ getUserInitials(member.name) }}
                      </div>
                      <div class="ml-4">
                        <div class="text-sm font-medium text-gray-900">{{ member.name }}</div>
                        <div class="text-sm text-gray-500">{{ member.email }}</div>
                      </div>
                    </div>
                  </td>
                  
                  <!-- 연락처 -->
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900">{{ member.phone || '-' }}</div>
                  </td>
                  
                  <!-- 직급/팀 -->
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900">{{ member.position || '-' }}</div>
                    <div class="text-sm text-gray-500">{{ member.team }}</div>
                  </td>
                  
                  <!-- 권한 -->
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="[
                      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                      member.role === 'admin' ? 'bg-red-100 text-red-800' :
                      member.role === 'power_user' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    ]">
                      {{ getRoleDisplayName(member.role) }}
                    </span>
                  </td>
                  
                  <!-- 상태 -->
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="[
                      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                      member.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                    ]">
                      {{ member.is_active ? '활성' : '비활성' }}
                    </span>
                  </td>
                  
                  <!-- 액션 -->
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div class="flex items-center space-x-2">
                      <!-- 수정 버튼 (권한에 따라 표시) -->
                      <button
                        v-if="canEditMember(currentUser, member.id)"
                        @click="editMember(member)"
                        class="text-blue-600 hover:text-blue-900 p-1 rounded"
                        title="수정"
                      >
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </button>
                      
                      <!-- 비밀번호 초기화 버튼 (관리자만) -->
                      <button
                        v-if="isAdmin(currentUser) && member.id !== currentUser?.id"
                        @click="resetPassword(member)"
                        class="text-yellow-600 hover:text-yellow-900 p-1 rounded"
                        title="비밀번호 초기화"
                      >
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v-2L4.257 10.257a6 6 0 0111.186-3.743L16 8a2 2 0 011-1.732M15 7a2 2 0 00-2 2m2-2v2a2 2 0 01-2 2m2-2a2 2 0 012 2z" />
                        </svg>
                      </button>
                      
                      <!-- 삭제 버튼 (관리자만, 자기 자신은 제외) -->
                      <button
                        v-if="canDeleteMember(currentUser, member.id)"
                        @click="deleteMember(member)"
                        class="text-red-600 hover:text-red-900 p-1 rounded"
                        title="삭제"
                      >
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <!-- 로딩 상태 -->
          <div v-if="isLoading" class="p-8 text-center">
            <div class="inline-flex items-center space-x-2 text-gray-500">
              <svg class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>로딩 중...</span>
            </div>
          </div>
          
          <!-- 데이터 없음 -->
          <div v-else-if="filteredMembers.length === 0" class="p-8 text-center text-gray-500">
            검색 결과가 없습니다.
          </div>
        </div>
      </div>
    </div>

    <!-- 팀원 생성/수정 모달 -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">
              {{ showCreateModal ? '새 팀원 추가' : '팀원 정보 수정' }}
            </h3>
            <button
              @click="closeModal"
              class="text-gray-400 hover:text-gray-600"
            >
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form @submit.prevent="saveMember" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- 이름 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">이름 *</label>
                <input
                  v-model="memberForm.name"
                  type="text"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                />
              </div>

              <!-- 이메일 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">이메일 *</label>
                <input
                  v-model="memberForm.email"
                  type="email"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                />
              </div>

              <!-- 연락처 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">연락처</label>
                <input
                  v-model="memberForm.phone"
                  type="tel"
                  placeholder="010-1234-5678"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                />
              </div>

              <!-- 직급 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">직급</label>
                <input
                  v-model="memberForm.position"
                  type="text"
                  placeholder="예: 선임, 책임, 수석"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                />
              </div>

              <!-- 팀 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">팀</label>
                <input
                  v-model="memberForm.team"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                />
              </div>

              <!-- 권한 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">권한 *</label>
                <select
                  v-model="memberForm.role"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                >
                  <option value="user">일반 사용자</option>
                  <option value="power_user">파워 사용자</option>
                  <option value="admin">관리자</option>
                </select>
              </div>
            </div>

            <!-- 비밀번호 (생성 시에만) -->
            <div v-if="showCreateModal">
              <label class="block text-sm font-medium text-gray-700 mb-2">비밀번호 *</label>
              <input
                v-model="memberForm.password"
                type="password"
                required
                minlength="6"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
              />
              <p class="text-xs text-gray-500 mt-1">최소 6자 이상 입력해주세요.</p>
            </div>

            <!-- 기술 스택 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">기술 스택</label>
              <input
                v-model="memberForm.skills"
                type="text"
                placeholder="AWS, Kubernetes, Python (쉼표로 구분)"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
              />
            </div>

            <!-- 활성 상태 -->
            <div class="flex items-center">
              <input
                v-model="memberForm.is_active"
                type="checkbox"
                id="is_active"
                class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
              />
              <label for="is_active" class="ml-2 text-sm font-medium text-gray-700">활성 상태</label>
            </div>

            <!-- 버튼들 -->
            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="closeModal"
                class="px-4 py-2 text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors text-sm"
              >
                취소
              </button>
              <button
                type="submit"
                :disabled="isSubmitting"
                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm disabled:opacity-50"
              >
                {{ isSubmitting ? '저장 중...' : (showCreateModal ? '추가' : '수정') }}
              </button>
            </div>
          </form>
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
import { api } from '@/services/api'
import authService from '@/services/authService'
import { 
  canDeleteMember, 
  canEditMember, 
  getAllowedMemberFields,
  isAdmin,
  isPowerUserOrAbove 
} from '@/utils/permissions'
import type { Member } from '@/types'

// 반응형 상태
const members = ref<Member[]>([])
const isLoading = ref(false)
const isSubmitting = ref(false)
const searchQuery = ref('')
const showCreateModal = ref(false)
const showEditModal = ref(false)
const editingMember = ref<Member | null>(null)
const message = ref('')
const messageType = ref<'success' | 'error'>('success')

// 현재 사용자
const currentUser = computed(() => authService.getUser())

// 권한별 기능 제어
const canUserDeleteMembers = computed(() => isAdmin(currentUser.value))
const canUserEditAllFields = computed(() => isAdmin(currentUser.value))
const canUserCreateMembers = computed(() => isAdmin(currentUser.value))

// 팀원 폼
const memberForm = reactive({
  name: '',
  email: '',
  phone: '',
  position: '',
  team: 'TS팀',
  role: 'user',
  password: '',
  skills: '',
  is_active: true
})

// 계산된 속성
const filteredMembers = computed(() => {
  if (!searchQuery.value) return members.value
  
  const query = searchQuery.value.toLowerCase()
  return members.value.filter(member =>
    member.name.toLowerCase().includes(query) ||
    member.email.toLowerCase().includes(query)
  )
})

const totalMembers = computed(() => members.value.length)
const activeMembers = computed(() => members.value.filter(m => m.is_active).length)

// 메서드
const loadMembers = async () => {
  try {
    isLoading.value = true
    const response: any = await api.get('/members/', {
      params: { exclude_admin: false } // 관리자 페이지에서는 모든 팀원 표시
    })
    
    // 응답 구조에 따라 처리
    if (response.members) {
      members.value = response.members
    } else if (Array.isArray(response)) {
      members.value = response
    } else {
      members.value = []
    }
  } catch (error: any) {
    console.error('팀원 목록 로드 에러:', error)
    showMessage('팀원 목록을 불러올 수 없습니다.', 'error')
  } finally {
    isLoading.value = false
  }
}

const getUserInitials = (name: string) => {
  return name
    .split(' ')
    .map(word => word.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const getRoleDisplayName = (role: string) => {
  const roleNames: Record<string, string> = {
    admin: '관리자',
    power_user: '파워유저',
    user: '일반유저'
  }
  return roleNames[role] || role
}

const editMember = (member: Member) => {
  editingMember.value = member
  memberForm.name = member.name
  memberForm.email = member.email
  memberForm.phone = member.phone || ''
  memberForm.position = member.position || ''
  memberForm.team = member.team
  memberForm.role = member.role
  memberForm.skills = member.skills || ''
  memberForm.is_active = member.is_active
  showEditModal.value = true
}

const saveMember = async () => {
  try {
    isSubmitting.value = true
    
    if (showCreateModal.value) {
      // 새 팀원 생성
      await api.post('/members/', memberForm)
      showMessage('팀원이 성공적으로 추가되었습니다.', 'success')
    } else if (showEditModal.value && editingMember.value) {
      // 팀원 정보 수정
      const updateData = { ...memberForm }
      if ('password' in updateData) {
        delete (updateData as any).password // 수정 시에는 비밀번호 제외
      }
      await api.put(`/members/${editingMember.value.id}`, updateData)
      showMessage('팀원 정보가 성공적으로 수정되었습니다.', 'success')
    }
    
    closeModal()
    await loadMembers()
  } catch (error: any) {
    console.error('팀원 저장 에러:', error)
    showMessage(error.response?.data?.detail || '작업에 실패했습니다.', 'error')
  } finally {
    isSubmitting.value = false
  }
}

const resetPassword = async (member: Member) => {
  if (!confirm(`${member.name}님의 비밀번호를 초기화하시겠습니까?`)) return
  
  try {
    const newPassword = prompt('새 비밀번호를 입력하세요 (최소 6자):')
    if (!newPassword || newPassword.length < 6) {
      showMessage('유효한 비밀번호를 입력해주세요.', 'error')
      return
    }
    
    await api.post(`/members/${member.id}/reset-password`, { password: newPassword })
    showMessage(`${member.name}님의 비밀번호가 초기화되었습니다.`, 'success')
  } catch (error: any) {
    console.error('비밀번호 초기화 에러:', error)
    showMessage(error.response?.data?.detail || '비밀번호 초기화에 실패했습니다.', 'error')
  }
}

const deleteMember = async (member: Member) => {
  if (!confirm(`정말로 ${member.name}님을 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.`)) return
  
  try {
    await api.delete(`/members/${member.id}`)
    showMessage(`${member.name}님이 삭제되었습니다.`, 'success')
    await loadMembers()
  } catch (error: any) {
    console.error('팀원 삭제 에러:', error)
    showMessage(error.response?.data?.detail || '팀원 삭제에 실패했습니다.', 'error')
  }
}

const closeModal = () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingMember.value = null
  
  // 폼 초기화
  Object.assign(memberForm, {
    name: '',
    email: '',
    phone: '',
    position: '',
    team: 'TS팀',
    role: 'user',
    password: '',
    skills: '',
    is_active: true
  })
}

const showMessage = (text: string, type: 'success' | 'error') => {
  message.value = text
  messageType.value = type
  setTimeout(() => {
    message.value = ''
  }, 3000)
}

// 컴포넌트 마운트 시 실행
onMounted(() => {
  loadMembers()
})
</script> 