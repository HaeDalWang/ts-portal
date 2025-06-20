/**
 * 팀원 관련 API 서비스
 */

import { api } from './api'
import type {
  Member,
  MemberCreate,
  MemberUpdate,
  MemberListResponse,
  MemberStats,
  SearchParams,
  PaginationParams
} from '../types'

export const memberService = {
  // 팀원 목록 조회
  async getMembers(params: PaginationParams = {}): Promise<MemberListResponse> {
    const queryParams = {
      skip: params.skip || 0,
      limit: params.limit || 100,
      active_only: params.active_only || false
    }
    return api.get<MemberListResponse>('/members/', queryParams)
  },

  // 팀원 단일 조회
  async getMember(id: number): Promise<Member> {
    return api.get<Member>(`/members/${id}`)
  },

  // 팀원 검색
  async searchMembers(params: SearchParams): Promise<Member[]> {
    const queryParams = {
      q: params.q,
      active_only: params.active_only || false
    }
    return api.get<Member[]>('/members/search', queryParams)
  },

  // 팀원 생성
  async createMember(memberData: MemberCreate): Promise<Member> {
    return api.post<Member>('/members/', memberData)
  },

  // 팀원 수정
  async updateMember(id: number, memberData: MemberUpdate): Promise<Member> {
    return api.put<Member>(`/members/${id}`, memberData)
  },

  // 팀원 삭제 (소프트 삭제)
  async deleteMember(id: number): Promise<void> {
    return api.delete(`/members/${id}`)
  },

  // 팀원 복구
  async restoreMember(id: number): Promise<Member> {
    return api.patch<Member>(`/members/${id}/restore`)
  },

  // 팀원 통계
  async getMemberStats(): Promise<MemberStats> {
    return api.get<MemberStats>('/members/stats/summary')
  },

  // 활성 팀원만 조회 (간편 함수)
  async getActiveMembers(): Promise<Member[]> {
    const response = await this.getMembers({ active_only: true })
    return response.members
  },

  // 팀원 이름으로 검색 (간편 함수)
  async searchMembersByName(name: string): Promise<Member[]> {
    return this.searchMembers({ q: name, active_only: true })
  }
}

export default memberService 