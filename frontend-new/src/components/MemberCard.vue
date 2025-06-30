<template>
  <div class="member-card" @click="$emit('click', member)">
    <!-- 프로필 이미지 -->
    <div class="member-avatar">
      <div class="avatar-placeholder">
        {{ member.name.charAt(0) }}
      </div>
    </div>

    <!-- 기본 정보 -->
    <div class="member-info">
      <h3 class="member-name">{{ member.name }}</h3>
      <p class="member-position">{{ member.position || '직책 없음' }}</p>
      <p class="member-team">{{ member.team }}</p>
    </div>

    <!-- 연락처 정보 -->
    <div class="member-contact">
      <div class="contact-item">
        <span class="contact-label">이메일</span>
        <span class="contact-value">{{ member.email }}</span>
      </div>
    </div>

    <!-- 권한 및 상태 -->
    <div class="member-status">
      <span class="role-badge" :class="getRoleClass(member.role)">
        {{ getRoleText(member.role) }}
      </span>
      <span class="status-badge" :class="member.is_active ? 'active' : 'inactive'">
        {{ member.is_active ? '활성' : '비활성' }}
      </span>
    </div>

    <!-- 추가 정보 -->
    <div v-if="member.skills" class="member-skills">
      <span class="skills-label">보유 기술</span>
      <div class="skills-list">
        <span
          v-for="skill in getSkillsList(member.skills)"
          :key="skill"
          class="skill-tag"
        >
          {{ skill }}
        </span>
      </div>
    </div>

    <!-- 마지막 로그인 -->
    <div v-if="member.last_login" class="member-last-login">
      <span class="last-login-label">마지막 로그인</span>
      <span class="last-login-value">{{ formatDate(member.last_login) }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Member } from '@/types/member'
import type { UserRole } from '@/types/auth'

// Props
interface Props {
  member: Member
}

defineProps<Props>()

// Emits
defineEmits<{
  click: [member: Member]
}>()

/**
 * 권한별 CSS 클래스 반환
 */
const getRoleClass = (role: UserRole): string => {
  const roleClasses = {
    admin: 'role-admin',
    power_user: 'role-power-user',
    user: 'role-user'
  }
  return roleClasses[role] || 'role-user'
}

/**
 * 권한별 텍스트 반환
 */
const getRoleText = (role: UserRole): string => {
  const roleTexts = {
    admin: '관리자',
    power_user: '파워유저',
    user: '일반유저'
  }
  return roleTexts[role] || '일반유저'
}

/**
 * 기술 목록 파싱
 */
const getSkillsList = (skills: string): string[] => {
  return skills.split(',').map(skill => skill.trim()).filter(skill => skill.length > 0)
}

/**
 * 날짜 포맷팅
 */
const formatDate = (dateString: string): string => {
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return '알 수 없음'
  }
}
</script>

<style scoped>
.member-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.member-card:hover {
  border-color: var(--color-primary);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.member-avatar {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}

.avatar-placeholder {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: var(--color-primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 600;
}

.member-info {
  text-align: center;
  margin-bottom: 1rem;
}

.member-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 0.25rem;
}

.member-position {
  font-size: 0.9rem;
  color: var(--color-primary);
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.member-team {
  font-size: 0.85rem;
  color: var(--color-text-secondary);
}

.member-contact {
  margin-bottom: 1rem;
  padding: 1rem 0;
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
}

.contact-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.contact-label {
  font-size: 0.8rem;
  color: var(--color-text-secondary);
  font-weight: 500;
}

.contact-value {
  font-size: 0.85rem;
  color: var(--color-text-primary);
  font-weight: 400;
}

.member-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.role-badge, .status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.role-admin {
  background: var(--color-error);
  color: white;
}

.role-power-user {
  background: var(--color-warning);
  color: white;
}

.role-user {
  background: var(--color-info);
  color: white;
}

.status-badge.active {
  background: var(--color-success);
  color: white;
}

.status-badge.inactive {
  background: var(--color-text-secondary);
  color: white;
}

.member-skills {
  margin-bottom: 1rem;
}

.skills-label {
  display: block;
  font-size: 0.8rem;
  color: var(--color-text-secondary);
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
}

.skill-tag {
  background: var(--color-background);
  border: 1px solid var(--color-border);
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.7rem;
  color: var(--color-text-primary);
}

.member-last-login {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.75rem;
}

.last-login-label {
  color: var(--color-text-secondary);
}

.last-login-value {
  color: var(--color-text-primary);
  font-weight: 500;
}

/* 반응형 */
@media (max-width: 768px) {
  .member-card {
    padding: 1rem;
  }
  
  .member-avatar {
    margin-bottom: 0.75rem;
  }
  
  .avatar-placeholder {
    width: 50px;
    height: 50px;
    font-size: 1.25rem;
  }
  
  .member-name {
    font-size: 1rem;
  }
  
  .member-status {
    flex-direction: column;
    gap: 0.5rem;
    align-items: stretch;
  }
  
  .role-badge, .status-badge {
    text-align: center;
  }
}
</style> 