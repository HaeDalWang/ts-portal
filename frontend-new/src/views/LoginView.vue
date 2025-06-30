<template>
  <div class="login-container">
    <div class="login-card">
      <!-- 헤더 -->
      <div class="login-header">
        <h1 class="login-title">TS Portal v2.0</h1>
        <p class="login-subtitle">MSA 서비스 연동 최우선 설계</p>
      </div>

      <!-- 로그인 폼 -->
      <form @submit.prevent="handleLogin" class="login-form">
        <!-- 아이디 입력 -->
        <div class="form-group">
          <label for="username" class="form-label">아이디</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            class="form-input"
            placeholder="아이디를 입력하세요"
            required
            :disabled="loading"
          >
        </div>

        <!-- 비밀번호 입력 -->
        <div class="form-group">
          <label for="password" class="form-label">비밀번호</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            class="form-input"
            placeholder="비밀번호를 입력하세요"
            required
            :disabled="loading"
          >
        </div>

        <!-- 에러 메시지 -->
        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <!-- 로그인 버튼 -->
        <button
          type="submit"
          class="btn btn-primary btn-lg login-button"
          :disabled="loading || !form.username || !form.password"
        >
          <span v-if="loading" class="loading">로그인 중...</span>
          <span v-else>로그인</span>
        </button>
      </form>

      <!-- 개발용 정보 -->
      <div class="dev-info">
        <p class="text-sm text-secondary">개발용 계정: admin / admin</p>
        <p class="text-xs text-tertiary">Kong Gateway: localhost:8080</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * 로그인 페이지
 * Kong Gateway를 통한 Auth Service 연동
 */

import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '@/composables/useAuth'

// 라우터
const router = useRouter()
const route = useRoute()

// 인증 상태 관리
const { login, loading, error, clearError, isAuthenticated } = useAuth()

// 폼 데이터
const form = ref({
  username: '',
  password: ''
})

/**
 * 로그인 처리
 */
const handleLogin = async (): Promise<void> => {
  clearError()
  
  const success = await login({
    username: form.value.username,
    password: form.value.password
  })

  if (success) {
    // 로그인 성공 시 리디렉션
    const redirectPath = (route.query.redirect as string) || '/dashboard'
    console.log('🔐 로그인 성공, 리디렉션:', redirectPath)
    await router.push(redirectPath)
  }
}

/**
 * 컴포넌트 마운트 시
 */
onMounted(() => {
  // 이미 로그인된 경우 대시보드로 리디렉션
  if (isAuthenticated.value) {
    router.push('/dashboard')
  }
  
  // 개발용 기본값 설정
  if (import.meta.env.DEV) {
    form.value.username = 'admin'
    form.value.password = 'admin'
  }
})
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--color-background-secondary) 0%, var(--color-background-tertiary) 100%);
  padding: var(--spacing-md);
}

.login-card {
  background: var(--color-background);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  padding: var(--spacing-2xl);
  width: 100%;
  max-width: 400px;
  border: 1px solid var(--color-border);
}

.login-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.login-title {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
}

.login-subtitle {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin: 0;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.form-label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-primary);
}

.form-input {
  width: 100%;
  padding: var(--spacing-md);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: var(--font-size-md);
  transition: all var(--transition-fast);
}

.form-input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input:disabled {
  background-color: var(--color-background-secondary);
  cursor: not-allowed;
  opacity: 0.6;
}

.error-message {
  background-color: rgba(239, 68, 68, 0.1);
  color: var(--color-error);
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  border: 1px solid rgba(239, 68, 68, 0.2);
  font-size: var(--font-size-sm);
  text-align: center;
}

.login-button {
  width: 100%;
  padding: var(--spacing-md);
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
}

.dev-info {
  margin-top: var(--spacing-xl);
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--color-border);
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

/* 반응형 디자인 */
@media (max-width: 480px) {
  .login-container {
    padding: var(--spacing-sm);
  }
  
  .login-card {
    padding: var(--spacing-xl);
  }
  
  .login-title {
    font-size: var(--font-size-2xl);
  }
}
</style> 