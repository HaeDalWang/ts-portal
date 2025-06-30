<template>
  <div id="app">
    <!-- 라우터 뷰 -->
    <RouterView />
  </div>
</template>

<script setup lang="ts">
/**
 * 루트 Vue 컴포넌트
 * 최소한의 구조로 RouterView만 포함
 */

// 필요한 경우 글로벌 상태나 설정을 여기서 초기화
</script>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style> 