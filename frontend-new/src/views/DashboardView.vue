<template>
  <div class="dashboard">
    <!-- 헤더 -->
    <header class="dashboard-header">
      <div class="container">
        <div class="header-content">
          <h1 class="dashboard-title">TS Portal v2.0</h1>
          <div class="user-info">
            <span v-if="user" class="welcome-text">
              안녕하세요, {{ user.name }}님!
            </span>
            <button @click="handleLogout" class="btn btn-secondary">
              로그아웃
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- 메인 콘텐츠 -->
    <main class="dashboard-main">
      <div class="container">
        <!-- 로딩 상태 -->
        <div v-if="loading" class="loading-state">
          <div class="loading">사용자 정보를 불러오는 중...</div>
        </div>

        <!-- 에러 상태 -->
        <div v-else-if="error" class="error-state">
          <div class="error-message">{{ error }}</div>
          <button @click="refreshUser" class="btn btn-primary">
            다시 시도
          </button>
        </div>

        <!-- 대시보드 콘텐츠 -->
        <div v-else class="dashboard-content">
          <!-- 환영 메시지 -->
          <section class="welcome-section">
            <div class="card">
              <h2>환영합니다! 🎉</h2>
              <p>TS Portal v2.0에 오신 것을 환영합니다.</p>
              <p class="text-secondary">
                MSA 서비스 연동 최우선 설계로 구축된 새로운 프론트엔드입니다.
              </p>
            </div>
          </section>

          <!-- 서비스 카드들 -->
          <section class="services-section">
            <h3 class="section-title">서비스 메뉴</h3>
            <div class="services-grid">
              <router-link to="/members" class="service-card">
                <div class="service-icon">👥</div>
                <h4>팀원 관리</h4>
                <p>팀원 정보 및 프로필 관리</p>
              </router-link>

              <router-link to="/customers" class="service-card">
                <div class="service-icon">🏢</div>
                <h4>고객사 관리</h4>
                <p>고객사 정보 및 담당자 배정</p>
              </router-link>

              <router-link to="/calendar" class="service-card">
                <div class="service-icon">📅</div>
                <h4>일정 관리</h4>
                <p>팀 일정 및 캘린더</p>
              </router-link>

              <router-link to="/notices" class="service-card">
                <div class="service-icon">📢</div>
                <h4>공지사항</h4>
                <p>팀 공지사항 관리</p>
              </router-link>

              <router-link to="/feeds" class="service-card">
                <div class="service-icon">📰</div>
                <h4>AWS 피드</h4>
                <p>AWS 최신 소식</p>
              </router-link>
            </div>
          </section>

          <!-- 시스템 정보 -->
          <section class="system-info">
            <div class="card">
              <h3>시스템 정보</h3>
              <div class="info-grid">
                <div class="info-item">
                  <span class="info-label">Kong Gateway:</span>
                  <span class="info-value">localhost:8000</span>
                </div>
                <div class="info-item">
                  <span class="info-label">Frontend:</span>
                  <span class="info-value">localhost:5174</span>
                </div>
                <div class="info-item">
                  <span class="info-label">사용자 권한:</span>
                  <span class="info-value">{{ user?.role || 'Unknown' }}</span>
                </div>
              </div>
            </div>
          </section>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
/**
 * 대시보드 페이지
 * 메인 랜딩 페이지 및 서비스 네비게이션
 */

import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'

// 라우터
const router = useRouter()

// 인증 상태 관리
const { user, loading, error, logout, refreshUser } = useAuth()

/**
 * 로그아웃 처리
 */
const handleLogout = async (): Promise<void> => {
  await logout()
  router.push('/login')
}

/**
 * 컴포넌트 마운트 시
 */
onMounted(() => {
  // 사용자 정보 새로고침
  refreshUser()
})
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background-color: var(--color-background-secondary);
}

.dashboard-header {
  background-color: var(--color-background);
  border-bottom: 1px solid var(--color-border);
  padding: var(--spacing-lg) 0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dashboard-title {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.welcome-text {
  font-size: var(--font-size-md);
  color: var(--color-text-secondary);
}

.dashboard-main {
  padding: var(--spacing-xl) 0;
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
}

.welcome-section .card {
  text-align: center;
  padding: var(--spacing-xl);
}

.welcome-section h2 {
  font-size: var(--font-size-2xl);
  margin-bottom: var(--spacing-md);
  color: var(--color-text-primary);
}

.welcome-section p {
  margin-bottom: var(--spacing-sm);
}

.services-section {
  margin-top: var(--spacing-xl);
}

.section-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-lg);
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--spacing-lg);
}

.service-card {
  background: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
  text-decoration: none;
  color: inherit;
  transition: all var(--transition-fast);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.service-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--color-primary);
}

.service-icon {
  font-size: 3rem;
  margin-bottom: var(--spacing-md);
}

.service-card h4 {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
}

.service-card p {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin: 0;
}

.system-info .card {
  padding: var(--spacing-lg);
}

.system-info h3 {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm);
  background-color: var(--color-background-secondary);
  border-radius: var(--radius-md);
}

.info-label {
  font-weight: var(--font-weight-medium);
  color: var(--color-text-secondary);
}

.info-value {
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
}

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-2xl);
  text-align: center;
}

.error-state {
  gap: var(--spacing-lg);
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: var(--spacing-md);
    text-align: center;
  }
  
  .services-grid {
    grid-template-columns: 1fr;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style> 