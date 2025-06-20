<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { memberService } from '../services'
import type { Member, MemberStats } from '../types'

// 반응형 상태
const members = ref<Member[]>([])
const stats = ref<MemberStats | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)
const searchQuery = ref('')
const showActiveOnly = ref(true)
const selectedMember = ref<Member | null>(null)
const showMemberModal = ref(false)
const viewMode = ref<'cards' | 'table'>('cards')

// 계산된 속성
const filteredMembers = computed(() => {
  let filtered = members.value

  // 활성 멤버만 표시 필터
  if (showActiveOnly.value) {
    filtered = filtered.filter(member => member.is_active)
  }

  // 검색 필터
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(member =>
      member.name.toLowerCase().includes(query) ||
      member.email.toLowerCase().includes(query) ||
      member.position?.toLowerCase().includes(query) ||
      member.skills_list.some(skill => skill.toLowerCase().includes(query))
    )
  }

  return filtered
})

// 데이터 로딩 함수
const loadMembers = async () => {
  try {
    loading.value = true
    error.value = null
    
    const [membersResponse, statsResponse] = await Promise.all([
      memberService.getMembers({ limit: 1000 }),
      memberService.getMemberStats()
    ])
    
    members.value = membersResponse.members
    stats.value = statsResponse
  } catch (err: any) {
    error.value = err.message || '데이터를 불러오는 중 오류가 발생했습니다.'
    console.error('팀원 데이터 로딩 오류:', err)
  } finally {
    loading.value = false
  }
}

// 멤버 상세 보기
const showMemberDetail = (member: Member) => {
  selectedMember.value = member
  showMemberModal.value = true
}

// 멤버 모달 닫기
const closeMemberModal = () => {
  showMemberModal.value = false
  selectedMember.value = null
}

// 직급별 색상 반환
const getPositionColor = (position?: string) => {
  if (!position) return 'bg-gray-100 text-gray-800'
  
  const colors: Record<string, string> = {
    '팀장': 'bg-purple-100 text-purple-800',
    '책임': 'bg-blue-100 text-blue-800',
    '선임': 'bg-green-100 text-green-800',
    '주임': 'bg-yellow-100 text-yellow-800',
    '인턴': 'bg-pink-100 text-pink-800'
  }
  
  return colors[position] || 'bg-gray-100 text-gray-800'
}

// 스킬 태그 색상 반환
const getSkillColor = (index: number) => {
  const colors = [
    'bg-red-100 text-red-800',
    'bg-orange-100 text-orange-800',
    'bg-amber-100 text-amber-800',
    'bg-yellow-100 text-yellow-800',
    'bg-lime-100 text-lime-800',
    'bg-green-100 text-green-800',
    'bg-emerald-100 text-emerald-800',
    'bg-teal-100 text-teal-800',
    'bg-cyan-100 text-cyan-800',
    'bg-sky-100 text-sky-800',
    'bg-blue-100 text-blue-800',
    'bg-indigo-100 text-indigo-800',
    'bg-violet-100 text-violet-800',
    'bg-purple-100 text-purple-800',
    'bg-fuchsia-100 text-fuchsia-800',
    'bg-pink-100 text-pink-800',
    'bg-rose-100 text-rose-800'
  ]
  return colors[index % colors.length]
}

// 컴포넌트 마운트 시 데이터 로딩
onMounted(() => {
  loadMembers()
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 컴팩트 헤더 -->
    <div class="bg-white border-b border-gray-200 px-6 py-3">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-xl font-bold text-gray-900">팀원 프로필</h1>
          <p class="text-sm text-gray-500">TS팀 멤버 관리</p>
        </div>
        
        <!-- 컴팩트 통계 및 컨트롤 -->
        <div class="flex items-center space-x-4">
          <!-- 통계 -->
          <div class="flex items-center space-x-3">
            <div class="text-center">
              <div class="text-sm font-semibold text-blue-600">{{ stats?.total_members || 0 }}</div>
              <div class="text-xs text-gray-500">전체</div>
            </div>
            <div class="text-center">
              <div class="text-sm font-semibold text-green-600">{{ stats?.active_members || 0 }}</div>
              <div class="text-xs text-gray-500">재직</div>
            </div>
            <div class="text-center">
              <div class="text-sm font-semibold text-purple-600">{{ stats?.active_rate || 0 }}%</div>
              <div class="text-xs text-gray-500">재직률</div>
            </div>
          </div>
          
          <!-- 구분선 -->
          <div class="h-8 w-px bg-gray-300"></div>
          
          <!-- 뷰 모드 전환 -->
          <div class="flex bg-gray-100 rounded-lg p-1">
            <button
              @click="viewMode = 'cards'"
              :class="`px-2 py-1 rounded-md text-xs font-medium transition-colors ${
                viewMode === 'cards' 
                  ? 'bg-white text-gray-900 shadow-sm' 
                  : 'text-gray-600 hover:text-gray-900'
              }`"
            >
              카드
            </button>
            <button
              @click="viewMode = 'table'"
              :class="`px-2 py-1 rounded-md text-xs font-medium transition-colors ${
                viewMode === 'table' 
                  ? 'bg-white text-gray-900 shadow-sm' 
                  : 'text-gray-600 hover:text-gray-900'
              }`"
            >
              테이블
            </button>
          </div>
          
          <button 
            @click="loadMembers"
            :disabled="loading"
            class="px-3 py-1.5 bg-purple-600 text-white rounded-md hover:bg-purple-700 disabled:opacity-50 transition-colors text-sm"
          >
            <svg v-if="loading" class="animate-spin -ml-1 mr-1 h-3 w-3 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            새로고침
          </button>
        </div>
      </div>
    </div>

    <!-- 메인 컨텐츠 -->
    <div class="p-6 space-y-6">

    <!-- 검색 및 필터 -->
    <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-4">
      <div class="flex flex-col md:flex-row gap-3">
        <div class="flex-1">
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="이름, 이메일, 직급, 기술 스택으로 검색..."
              class="block w-full pl-10 pr-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-purple-500 focus:border-purple-500"
            />
          </div>
        </div>
        <div class="flex items-center space-x-3">
          <label class="flex items-center">
            <input
              v-model="showActiveOnly"
              type="checkbox"
              class="rounded border-gray-300 text-purple-600 shadow-sm focus:border-purple-300 focus:ring focus:ring-purple-200 focus:ring-opacity-50"
            />
            <span class="ml-2 text-xs text-gray-700">재직자만 보기</span>
          </label>
          <div class="text-xs text-gray-500">
            {{ filteredMembers.length }}명 표시
          </div>
        </div>
      </div>
    </div>

    <!-- 에러 메시지 -->
    <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-3">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-4 w-4 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
        </div>
        <div class="ml-3">
          <p class="text-xs text-red-800">{{ error }}</p>
        </div>
      </div>
    </div>

    <!-- 로딩 상태 -->
    <div v-if="loading" class="bg-white rounded-xl shadow-lg border border-gray-200 p-8 text-center">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto mb-3"></div>
      <p class="text-xs text-gray-600">팀원 정보를 불러오는 중...</p>
    </div>

    <!-- 팀원 카드 그리드 -->
    <div v-else-if="filteredMembers.length > 0 && viewMode === 'cards'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="member in filteredMembers"
        :key="member.id"
        @click="showMemberDetail(member)"
        class="bg-white rounded-xl shadow-lg border border-gray-200 p-4 hover:shadow-xl transition-shadow cursor-pointer"
      >
        <div class="flex items-center space-x-3 mb-3">
          <div class="w-10 h-10 bg-gradient-to-br from-purple-400 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-sm">
            {{ member.name.charAt(0) }}
          </div>
          <div class="flex-1">
            <h3 class="text-sm font-semibold text-gray-900">{{ member.name }}</h3>
            <p class="text-xs text-gray-600">{{ member.email }}</p>
          </div>
          <div v-if="member.position" :class="`px-2 py-1 rounded-full text-xs font-medium ${getPositionColor(member.position)}`">
            {{ member.position }}
          </div>
        </div>

        <div class="space-y-1 mb-3">
          <div v-if="member.phone" class="flex items-center text-xs text-gray-600">
            <svg class="w-3 h-3 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
            </svg>
            {{ member.phone }}
          </div>
          <div class="flex items-center text-xs text-gray-600">
            <svg class="w-3 h-3 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-5 0H9m0 0H5m4 0v-5a1 1 0 011-1h4a1 1 0 011 1v5m-4 0v-2m0 0h2m-2 0v2" />
            </svg>
            {{ member.team }}
          </div>
          <div v-if="member.join_date" class="flex items-center text-xs text-gray-600">
            <svg class="w-3 h-3 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            {{ new Date(member.join_date).toLocaleDateString('ko-KR') }} 입사
          </div>
        </div>

        <div v-if="member.skills_list.length > 0" class="space-y-1">
          <p class="text-xs font-medium text-gray-700">기술 스택</p>
          <div class="flex flex-wrap gap-1">
            <span
              v-for="(skill, index) in member.skills_list.slice(0, 5)"
              :key="skill"
              :class="`px-2 py-1 rounded-full text-xs font-medium ${getSkillColor(index)}`"
            >
              {{ skill }}
            </span>
            <span
              v-if="member.skills_list.length > 5"
              class="px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-600"
            >
              +{{ member.skills_list.length - 5 }}
            </span>
          </div>
        </div>

        <div class="mt-3 flex items-center justify-between">
          <div :class="`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${member.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`">
            <div :class="`w-2 h-2 rounded-full mr-1 ${member.is_active ? 'bg-green-400' : 'bg-gray-400'}`"></div>
            {{ member.is_active ? '재직 중' : '퇴사' }}
          </div>
          <button class="text-purple-600 hover:text-purple-800 text-xs font-medium">
            자세히 보기 →
          </button>
        </div>
      </div>
    </div>

    <!-- 팀원 테이블 뷰 -->
    <div v-else-if="filteredMembers.length > 0 && viewMode === 'table'" class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-48">팀원</th>
              <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-20">팀</th>
              <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-16">직급</th>
              <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-52">연락처</th>
              <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-20">상태</th>
              <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">기술스택</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr 
              v-for="member in filteredMembers" 
              :key="member.id"
              @click="showMemberDetail(member)"
              class="hover:bg-gray-50 cursor-pointer transition-colors"
            >
              <td class="px-4 py-3">
                <div class="flex items-center">
                  <div class="w-8 h-8 bg-gradient-to-br from-purple-400 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-sm">
                    {{ member.name.charAt(0) }}
                  </div>
                  <div class="ml-3">
                    <div class="text-sm font-medium text-gray-900">{{ member.name }}</div>
                    <div class="text-xs text-gray-500">{{ member.join_date ? new Date(member.join_date).toLocaleDateString('ko-KR') + ' 입사' : '' }}</div>
                  </div>
                </div>
              </td>
              <td class="px-3 py-3 text-sm text-gray-900">{{ member.team.replace('파트', '') }}</td>
              <td class="px-3 py-3">
                <span v-if="member.position" :class="`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getPositionColor(member.position)}`">
                  {{ member.position }}
                </span>
                <span v-else class="text-xs text-gray-500">-</span>
              </td>
              <td class="px-3 py-3">
                <div class="space-y-1">
                  <div class="text-sm text-gray-900">{{ member.email }}</div>
                  <div class="text-xs text-gray-500">{{ member.phone || '-' }}</div>
                </div>
              </td>
              <td class="px-3 py-3">
                <span :class="`inline-flex items-center px-2 py-1 text-xs font-semibold rounded-full ${member.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`">
                  <div :class="`w-2 h-2 rounded-full mr-1 ${member.is_active ? 'bg-green-400' : 'bg-gray-400'}`"></div>
                  {{ member.is_active ? '재직' : '퇴사' }}
                </span>
              </td>
              <td class="px-3 py-3">
                <div class="flex flex-wrap gap-1">
                  <span
                    v-for="(skill, index) in member.skills_list.slice(0, 2)"
                    :key="skill"
                    :class="`px-2 py-1 rounded-full text-xs font-medium ${getSkillColor(index)}`"
                  >
                    {{ skill }}
                  </span>
                  <span
                    v-if="member.skills_list.length > 2"
                    class="px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-600"
                  >
                    +{{ member.skills_list.length - 2 }}
                  </span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 검색 결과 없음 -->
    <div v-else-if="!loading" class="bg-white rounded-xl shadow-lg border border-gray-200 p-12 text-center">
      <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
      </div>
      <h2 class="text-xl font-semibold text-gray-900 mb-2">팀원을 찾을 수 없습니다</h2>
      <p class="text-gray-600 mb-4">검색 조건을 변경하거나 필터를 확인해보세요.</p>
    </div>

    <!-- 팀원 상세 모달 -->
    <div v-if="showMemberModal && selectedMember" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50" @click="closeMemberModal">
      <div class="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto" @click.stop>
        <div class="p-6">
          <!-- 모달 헤더 -->
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-bold text-gray-900">팀원 상세 정보</h2>
            <button @click="closeMemberModal" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- 팀원 정보 -->
          <div class="space-y-6">
            <!-- 기본 정보 -->
            <div class="flex items-center space-x-6">
              <div class="w-20 h-20 bg-gradient-to-br from-purple-400 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-2xl">
                {{ selectedMember.name.charAt(0) }}
              </div>
              <div class="flex-1">
                <h3 class="text-2xl font-bold text-gray-900 mb-1">{{ selectedMember.name }}</h3>
                <div class="flex items-center space-x-3 mb-2">
                  <span v-if="selectedMember.position" :class="`px-3 py-1 rounded-full text-sm font-medium ${getPositionColor(selectedMember.position)}`">
                    {{ selectedMember.position }}
                  </span>
                  <span :class="`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${selectedMember.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`">
                    <div :class="`w-2 h-2 rounded-full mr-1 ${selectedMember.is_active ? 'bg-green-400' : 'bg-gray-400'}`"></div>
                    {{ selectedMember.is_active ? '재직 중' : '퇴사' }}
                  </span>
                </div>
                <p class="text-gray-600">{{ selectedMember.email }}</p>
              </div>
            </div>

            <!-- 연락처 정보 -->
            <div class="bg-gray-50 rounded-lg p-4">
              <h4 class="font-semibold text-gray-900 mb-3">연락처 정보</h4>
              <div class="space-y-2">
                <div class="flex items-center text-sm">
                  <svg class="w-4 h-4 mr-3 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                  </svg>
                  <span class="text-gray-600">이메일:</span>
                  <span class="ml-2 font-medium">{{ selectedMember.email }}</span>
                </div>
                <div v-if="selectedMember.phone" class="flex items-center text-sm">
                  <svg class="w-4 h-4 mr-3 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                  <span class="text-gray-600">전화번호:</span>
                  <span class="ml-2 font-medium">{{ selectedMember.phone }}</span>
                </div>
                <div class="flex items-center text-sm">
                  <svg class="w-4 h-4 mr-3 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-5 0H9m0 0H5m4 0v-5a1 1 0 011-1h4a1 1 0 011 1v5m-4 0v-2m0 0h2m-2 0v2" />
                  </svg>
                  <span class="text-gray-600">소속팀:</span>
                  <span class="ml-2 font-medium">{{ selectedMember.team }}</span>
                </div>
                <div v-if="selectedMember.join_date" class="flex items-center text-sm">
                  <svg class="w-4 h-4 mr-3 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span class="text-gray-600">입사일:</span>
                  <span class="ml-2 font-medium">{{ new Date(selectedMember.join_date).toLocaleDateString('ko-KR') }}</span>
                </div>
              </div>
            </div>

            <!-- 기술 스택 -->
            <div v-if="selectedMember.skills_list.length > 0">
              <h4 class="font-semibold text-gray-900 mb-3">기술 스택</h4>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="(skill, index) in selectedMember.skills_list"
                  :key="skill"
                  :class="`px-3 py-1 rounded-full text-sm font-medium ${getSkillColor(index)}`"
                >
                  {{ skill }}
                </span>
              </div>
            </div>
          </div>

          <!-- 모달 푸터 -->
          <div class="mt-8 flex justify-end">
            <button
              @click="closeMemberModal"
              class="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
            >
              닫기
            </button>
          </div>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<style scoped>
/* 추가 애니메이션 및 스타일 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style> 