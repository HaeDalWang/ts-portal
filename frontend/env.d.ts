/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  readonly VITE_HONEYBOX_API_URL: string
  readonly VITE_DB_API_URL: string
  readonly VITE_APP_ENV: string
  // 필요시 다른 환경변수들도 여기에 추가
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
