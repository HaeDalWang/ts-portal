/**
 * Notice Service 타입 정의
 * 공지사항 관리 시스템
 */

// 공지사항 우선순위
export enum NoticePriority {
  NORMAL = 'normal',
  CAUTION = 'caution',    // Warning (Power User 이상)
  IMPORTANT = 'important' // 긴급 (Admin만)
}

// 작성자 정보
export interface AuthorInfo {
  id: number
  name: string
  email: string
  position?: string
  team?: string
}

// 공지사항 기본 타입
export interface NoticeBase {
  title: string
  content: string
  priority: NoticePriority
  is_pinned: boolean
}

// 공지사항 생성 요청
export interface NoticeCreate extends NoticeBase {
  // author_id는 헤더에서 자동 추출됨
}

// 공지사항 수정 요청
export interface NoticeUpdate {
  title?: string
  content?: string
  priority?: NoticePriority
  is_pinned?: boolean
}

// 공지사항 응답
export interface NoticeResponse extends NoticeBase {
  id: number
  author_id: number
  author?: AuthorInfo
  is_active: boolean
  created_at: string
  updated_at: string
  priority_display: string
  priority_color: string
  priority_icon: string
}

// 공지사항 목록 응답
export interface NoticeListResponse {
  total: number
  notices: NoticeResponse[]
}

// 공지사항 통계
export interface NoticeStats {
  total_notices: number
  active_notices: number
  pinned_notices: number
  notices_by_priority: Record<string, number>
  recent_notices: number
}

// 검색 파라미터
export interface SearchParams {
  q?: string
  priority?: NoticePriority
  author_id?: number
  is_pinned?: boolean
  active_only?: boolean
}

// 페이지네이션 파라미터
export interface PaginationParams {
  skip: number
  limit: number
}

// 우선순위 정보
export interface PriorityInfo {
  value: string
  label: string
  icon: string
  color: string
  description: string
}

// 공지사항 상태
export interface NoticeState {
  notices: NoticeResponse[]
  pinnedNotices: NoticeResponse[]
  recentNotices: NoticeResponse[]
  loading: boolean
  error: string | null
  stats: NoticeStats | null
  priorities: PriorityInfo[]
} 