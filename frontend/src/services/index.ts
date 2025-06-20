/**
 * 서비스 레이어 인덱스
 */

export { api } from './api'
export { default as memberService } from './memberService'
export { default as customerService } from './customerService'

// 모든 서비스들을 하나의 객체로 내보내기
export const services = {
  memberService: () => import('./memberService').then(m => m.default),
  customerService: () => import('./customerService').then(m => m.default),
}

export default services 