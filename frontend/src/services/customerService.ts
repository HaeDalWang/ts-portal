/**
 * 고객사 관련 API 서비스
 */

import { api } from './api'
import type {
  Customer,
  CustomerCreate,
  CustomerUpdate,
  CustomerListResponse,
  CustomerStats,
  SearchParams,
  PaginationParams
} from '../types'

export const customerService = {
  // 고객사 목록 조회
  async getCustomers(params: PaginationParams = {}): Promise<CustomerListResponse> {
    const queryParams = {
      skip: params.skip || 0,
      limit: params.limit || 100,
      active_only: params.active_only || false
    }
    return api.get<CustomerListResponse>('/customers/', queryParams)
  },

  // 고객사 단일 조회
  async getCustomer(id: number): Promise<Customer> {
    return api.get<Customer>(`/customers/${id}`)
  },

  // 고객사 검색
  async searchCustomers(params: SearchParams): Promise<Customer[]> {
    const queryParams = {
      q: params.q,
      active_only: params.active_only || false
    }
    return api.get<Customer[]>('/customers/search', queryParams)
  },

  // 상태별 고객사 조회
  async getCustomersByStatus(status: string): Promise<Customer[]> {
    return api.get<Customer[]>(`/customers/status/${status}`)
  },

  // 계약 만료 예정 고객사 조회
  async getExpiringCustomers(days: number = 30): Promise<Customer[]> {
    return api.get<Customer[]>('/customers/expiring', { days })
  },

  // 고객사 생성
  async createCustomer(customerData: CustomerCreate): Promise<Customer> {
    return api.post<Customer>('/customers/', customerData)
  },

  // 고객사 수정
  async updateCustomer(id: number, customerData: CustomerUpdate): Promise<Customer> {
    return api.put<Customer>(`/customers/${id}`, customerData)
  },

  // 고객사 삭제 (상태 변경)
  async deleteCustomer(id: number): Promise<void> {
    return api.delete(`/customers/${id}`)
  },

  // 고객사 활성화
  async activateCustomer(id: number): Promise<Customer> {
    return api.patch<Customer>(`/customers/${id}/activate`)
  },

  // 고객사 통계
  async getCustomerStats(): Promise<CustomerStats> {
    return api.get<CustomerStats>('/customers/stats/summary')
  },

  // 활성 고객사만 조회 (간편 함수)
  async getActiveCustomers(): Promise<Customer[]> {
    const response = await this.getCustomers({ active_only: true })
    return response.customers
  },

  // 고객사명으로 검색 (간편 함수)
  async searchCustomersByName(companyName: string): Promise<Customer[]> {
    return this.searchCustomers({ q: companyName, active_only: true })
  },

  // MSP 고객사만 조회 (간편 함수)
  async getMspCustomers(): Promise<Customer[]> {
    const allCustomers = await this.getActiveCustomers()
    return allCustomers.filter(customer => 
      customer.support_level?.toLowerCase().includes('msp')
    )
  },

  // 컨설팅 고객사만 조회 (간편 함수)
  async getConsultingCustomers(): Promise<Customer[]> {
    const allCustomers = await this.getActiveCustomers()
    return allCustomers.filter(customer => 
      customer.support_level?.toLowerCase().includes('consulting')
    )
  }
}

export default customerService 