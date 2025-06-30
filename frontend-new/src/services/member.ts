/**
 * Member Service API
 * Kong Gateway를 통한 팀원 관리 서비스 연동 (/api/members/*)
 */

import { kongApi } from './api'
import type { Member, MemberListResponse, MemberSearchParams, CreateMemberRequest, UpdateMemberRequest } from '@/types/member'

export class MemberService {
  private readonly basePath = '/api/members/'

  /**
   * 팀원 목록 조회
   */
  async getMembers(params?: MemberSearchParams): Promise<MemberListResponse> {
    const queryParams = new URLSearchParams()
    
    if (params?.team) queryParams.append('team', params.team)
    if (params?.position) queryParams.append('position', params.position)
    if (params?.role) queryParams.append('role', params.role)
    if (params?.is_active !== undefined) queryParams.append('is_active', params.is_active.toString())
    if (params?.search) queryParams.append('search', params.search)
    if (params?.page) queryParams.append('page', params.page.toString())
    if (params?.size) queryParams.append('size', params.size.toString())

    const query = queryParams.toString()
    const endpoint = query ? `${this.basePath}?${query}` : this.basePath

    return kongApi.get<MemberListResponse>(endpoint)
  }

  /**
   * 팀원 상세 정보 조회
   */
  async getMember(id: number): Promise<Member> {
    return kongApi.get<Member>(`${this.basePath}/${id}`)
  }

  /**
   * 팀원 정보 생성
   */
  async createMember(member: CreateMemberRequest): Promise<Member> {
    return kongApi.post<Member>(this.basePath, member)
  }

  /**
   * 팀원 정보 수정
   */
  async updateMember(id: number, member: UpdateMemberRequest): Promise<Member> {
    return kongApi.put<Member>(`${this.basePath}/${id}`, member)
  }

  /**
   * 팀원 정보 삭제 (비활성화)
   */
  async deleteMember(id: number): Promise<void> {
    return kongApi.delete(`${this.basePath}/${id}`)
  }

  /**
   * 팀 목록 조회
   */
  async getTeams(): Promise<string[]> {
    return kongApi.get<string[]>(`${this.basePath}/teams`)
  }

  /**
   * 직책 목록 조회
   */
  async getPositions(): Promise<string[]> {
    return kongApi.get<string[]>(`${this.basePath}/positions`)
  }

  /**
   * 팀별 통계 조회
   */
  async getTeamStats(): Promise<Record<string, number>> {
    return kongApi.get<Record<string, number>>(`${this.basePath}/stats/teams`)
  }

  /**
   * Member Service 상태 확인
   */
  async healthCheck(): Promise<boolean> {
    try {
      await kongApi.get(`${this.basePath}/health`)
      return true
    } catch {
      return false
    }
  }
}

// 싱글톤 인스턴스 생성
export const memberService = new MemberService()

// 기본 export
export default memberService 