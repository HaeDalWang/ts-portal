/**
 * Customer Service API 클라이언트
 * Kong Gateway를 통한 고객사 관리 API 연동
 */

import { kongApi } from './api'
import type {
  Customer,
  CustomerCreate,
  CustomerUpdate,
  CustomerListResponse,
  CustomerSearchParams,
  Assignment,
  AssignmentCreate,
  AssignmentUpdate,
  AssignmentListResponse,
  CustomerStats,
  AssignmentStats
} from '@/types/customer'

export class CustomerService {
  private readonly basePath = '/api/customers'

  /**
   * 고객사 목록 조회
   */
  async getCustomers(params?: CustomerSearchParams): Promise<CustomerListResponse> {
    const queryParams = new URLSearchParams()
    
    if (params?.skip !== undefined) queryParams.set('skip', params.skip.toString())
    if (params?.limit !== undefined) queryParams.set('limit', params.limit.toString())
    if (params?.q) queryParams.set('q', params.q)
    if (params?.status) queryParams.set('status', params.status)
    if (params?.active_only) queryParams.set('active_only', 'true')
    if (params?.contract_type) queryParams.set('contract_type', params.contract_type)

    const url = queryParams.toString() ? `${this.basePath}?${queryParams}` : this.basePath
    return await kongApi.get<CustomerListResponse>(url)
  }

  /**
   * 고객사 상세 조회
   */
  async getCustomer(id: number): Promise<Customer> {
    return await kongApi.get<Customer>(`${this.basePath}/${id}`)
  }

  /**
   * 고객사 생성
   */
  async createCustomer(data: CustomerCreate): Promise<Customer> {
    return await kongApi.post<Customer>(this.basePath, data)
  }

  /**
   * 고객사 수정
   */
  async updateCustomer(id: number, data: CustomerUpdate): Promise<Customer> {
    return await kongApi.put<Customer>(`${this.basePath}/${id}`, data)
  }

  /**
   * 고객사 삭제 (비활성화)
   */
  async deleteCustomer(id: number): Promise<{ message: string }> {
    return await kongApi.delete<{ message: string }>(`${this.basePath}/${id}`)
  }

  /**
   * 고객사 검색
   */
  async searchCustomers(query: string, activeOnly: boolean = false): Promise<Customer[]> {
    const params = new URLSearchParams({
      q: query,
      active_only: activeOnly.toString()
    })
    return await kongApi.get<Customer[]>(`${this.basePath}/search?${params}`)
  }

  /**
   * 계약 만료 예정 고객사 조회
   */
  async getExpiringCustomers(days: number = 30): Promise<Customer[]> {
    return await kongApi.get<Customer[]>(`${this.basePath}/expiring?days=${days}`)
  }

  /**
   * 고객사 통계
   */
  async getCustomerStats(): Promise<CustomerStats> {
    return await kongApi.get<CustomerStats>(`${this.basePath}/stats`)
  }
}

export class AssignmentService {
  private readonly basePath = '/api/assignments'

  /**
   * 담당자 배정 생성
   */
  async createAssignment(data: AssignmentCreate): Promise<Assignment> {
    return await kongApi.post<Assignment>(this.basePath, data)
  }

  /**
   * 담당자 배정 조회
   */
  async getAssignment(id: number): Promise<Assignment> {
    return await kongApi.get<Assignment>(`${this.basePath}/${id}`)
  }

  /**
   * 담당자 배정 수정
   */
  async updateAssignment(id: number, data: AssignmentUpdate): Promise<Assignment> {
    return await kongApi.put<Assignment>(`${this.basePath}/${id}`, data)
  }

  /**
   * 담당자 배정 삭제
   */
  async deleteAssignment(id: number): Promise<{ message: string }> {
    return await kongApi.delete<{ message: string }>(`${this.basePath}/${id}`)
  }

  /**
   * 팀원별 담당 고객사 조회
   */
  async getAssignmentsByMember(memberId: number, activeOnly: boolean = false): Promise<Assignment[]> {
    const params = activeOnly ? '?active_only=true' : ''
    return await kongApi.get<Assignment[]>(`${this.basePath}/member/${memberId}${params}`)
  }

  /**
   * 고객사별 담당자 조회
   */
  async getAssignmentsByCustomer(customerId: number, activeOnly: boolean = false): Promise<Assignment[]> {
    const params = activeOnly ? '?active_only=true' : ''
    return await kongApi.get<Assignment[]>(`${this.basePath}/customer/${customerId}${params}`)
  }

  /**
   * 담당자 배정 통계
   */
  async getAssignmentStats(): Promise<AssignmentStats> {
    return await kongApi.get<AssignmentStats>(`${this.basePath}/stats`)
  }
}

// 싱글톤 인스턴스 생성
export const customerService = new CustomerService()
export const assignmentService = new AssignmentService()

// 기본 export
export default customerService 