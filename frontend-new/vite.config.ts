import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  
  // 개발 서버 설정
  server: {
    port: 5174, // 기존 프론트엔드와 포트 분리
    host: true,
    cors: true
  },

  // 빌드 최적화
  build: {
    target: 'esnext',
    minify: 'esbuild',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          'vue-vendor': ['vue', 'vue-router']
        }
      }
    }
  },

  // 경로 별칭
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '@/components': resolve(__dirname, 'src/components'),
      '@/services': resolve(__dirname, 'src/services'),
      '@/composables': resolve(__dirname, 'src/composables'),
      '@/utils': resolve(__dirname, 'src/utils'),
      '@/types': resolve(__dirname, 'src/types')
    }
  },

  // CSS 설정
  css: {
    modules: {
      localsConvention: 'camelCaseOnly'
    }
  }
}) 