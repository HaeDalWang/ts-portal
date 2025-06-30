<template>
  <div class="not-found-view">
    <div class="container">
      <div class="not-found-content">
        <div class="error-code">404</div>
        <h1>페이지를 찾을 수 없습니다</h1>
        <p>요청하신 페이지가 존재하지 않거나 이동되었습니다.</p>
        <router-link to="/dashboard" class="btn btn-primary">
          대시보드로 돌아가기
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 404 페이지
</script>

<style scoped>
.not-found-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-background-secondary);
}

.not-found-content {
  text-align: center;
  padding: var(--spacing-2xl);
}

.error-code {
  font-size: 8rem;
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
  line-height: 1;
  margin-bottom: var(--spacing-lg);
}

.not-found-content h1 {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
}

.not-found-content p {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-xl);
}
</style> 