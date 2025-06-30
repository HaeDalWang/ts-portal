<template>
  <div class="calendar-view">
    <div class="container">
      <header class="page-header">
        <h1>일정 관리</h1>
        <p class="page-subtitle">Calendar Service 연동</p>
      </header>
      <div class="page-content">
        <div class="card">
          <h2>📅 일정 관리</h2>
          <p>Calendar Service API 연동 예정</p>
          <p class="text-secondary">Kong Gateway → Calendar Service (8003)</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Calendar Service 연동 예정
</script>

<style scoped>
.calendar-view {
  min-height: 100vh;
  background-color: var(--color-background-secondary);
  padding: var(--spacing-xl) 0;
}
.page-header { text-align: center; margin-bottom: var(--spacing-xl); }
.page-header h1 { font-size: var(--font-size-3xl); font-weight: var(--font-weight-bold); color: var(--color-text-primary); margin-bottom: var(--spacing-sm); }
.page-subtitle { font-size: var(--font-size-md); color: var(--color-text-secondary); }
.page-content .card { text-align: center; padding: var(--spacing-2xl); }
.page-content h2 { font-size: var(--font-size-2xl); margin-bottom: var(--spacing-md); }
</style> 