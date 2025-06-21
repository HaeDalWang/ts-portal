<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="text-center">
        <!-- 404 아이콘 -->
        <div class="mx-auto h-24 w-24 text-gray-400">
          <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-full h-full">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0118 12c0-4.418-3.582-8-8-8s-8 3.582-8 8c0 2.152.851 4.103 2.233 5.535z" />
          </svg>
        </div>
        
        <!-- 404 텍스트 -->
        <h1 class="mt-6 text-6xl font-bold text-gray-900">404</h1>
        <h2 class="mt-2 text-xl font-semibold text-gray-700">페이지를 찾을 수 없습니다</h2>
        <p class="mt-2 text-sm text-gray-500">
          요청하신 페이지가 존재하지 않거나 이동되었을 수 있습니다.
        </p>
        
        <!-- 액션 버튼들 -->
        <div class="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
          <router-link
            to="/"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
          >
            <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
            홈으로 돌아가기
          </router-link>
          
          <button
            @click="goBack"
            class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
          >
            <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            이전 페이지
          </button>
        </div>
        
        <!-- 도움말 링크들 -->
        <div class="mt-8">
          <p class="text-sm text-gray-500 mb-4">또는 다음 페이지들을 방문해보세요:</p>
          <div class="flex flex-wrap justify-center gap-4 text-sm">
            <router-link to="/team" class="text-blue-600 hover:text-blue-800 hover:underline">팀원 프로필</router-link>
            <router-link to="/dashboard" class="text-blue-600 hover:text-blue-800 hover:underline">팀 대시보드</router-link>
            <router-link to="/msp" class="text-blue-600 hover:text-blue-800 hover:underline">MSP 관리</router-link>
            <router-link to="/aws-tips" class="text-blue-600 hover:text-blue-800 hover:underline">AWS 소식</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  if (window.history.length > 1) {
    router.go(-1)
  } else {
    router.push('/')
  }
}
</script> 