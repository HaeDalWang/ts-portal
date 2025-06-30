<template>
  <div class="customer-view">
    <div class="container">
      <header class="page-header">
        <h1>고객사 관리</h1>
        <p class="page-subtitle">Customer Service 연동</p>
      </header>
      <div class="page-content">
        <div class="card">
          <h2>🏢 고객사 관리</h2>
          <p>Customer Service API 연동 예정</p>
          <p class="text-secondary">Kong Gateway → Customer Service (8002)</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Customer Service 연동 예정
</script>

<style scoped>
.customer-view {
  min-height: 100vh;
  background-color: var(--color-background-secondary);
  padding: var(--spacing-xl) 0;
}
.page-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}
.page-header h1 {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
}
.page-subtitle {
  font-size: var(--font-size-md);
  color: var(--color-text-secondary);
}
.page-content .card {
  text-align: center;
  padding: var(--spacing-2xl);
}
.page-content h2 {
  font-size: var(--font-size-2xl);
  margin-bottom: var(--spacing-md);
}
</style> 