"""
Customer Service Pydantic 스키마 정의
"""

from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum

class CustomerStatusEnum(str, Enum):
    """고객사 상태 열거형"""
    active = "Active"
    pending = "Pending"
    expired = "Expired"
    suspended = "Suspended"

class AssignmentRoleEnum(str, Enum):
    """담당자 역할 열거형"""
    primary = "Primary"
    secondary = "Secondary"
    backup = "Backup"

# Customer 스키마들
class CustomerBase(BaseModel):
    """고객사 기본 스키마"""
    company_name: str = Field(..., min_length=1, max_length=100, description="고객사명")
    contact_person: Optional[str] = Field(None, max_length=50, description="담당자명")
    contact_email: Optional[str] = Field(None, description="담당자 이메일")
    contact_phone: Optional[str] = Field(None, max_length=20, description="담당자 전화번호")
    contract_type: Optional[str] = Field(None, max_length=50, description="계약 유형")
    contract_start: Optional[date] = Field(None, description="계약 시작일")
    contract_end: Optional[date] = Field(None, description="계약 종료일")
    notes: Optional[str] = Field(None, description="특이사항 및 메모")

class CustomerCreate(CustomerBase):
    """고객사 생성 스키마"""
    status: CustomerStatusEnum = Field(default=CustomerStatusEnum.active, description="상태")

class CustomerUpdate(BaseModel):
    """고객사 수정 스키마"""
    company_name: Optional[str] = Field(None, min_length=1, max_length=100, description="고객사명")
    contact_person: Optional[str] = Field(None, max_length=50, description="담당자명")
    contact_email: Optional[str] = Field(None, description="담당자 이메일")
    contact_phone: Optional[str] = Field(None, max_length=20, description="담당자 전화번호")
    contract_type: Optional[str] = Field(None, max_length=50, description="계약 유형")
    contract_start: Optional[date] = Field(None, description="계약 시작일")
    contract_end: Optional[date] = Field(None, description="계약 종료일")
    status: Optional[CustomerStatusEnum] = Field(None, description="상태")
    notes: Optional[str] = Field(None, description="특이사항 및 메모")

class CustomerResponse(CustomerBase):
    """고객사 응답 스키마"""
    id: int
    status: str
    is_active: bool = Field(description="계약 활성 상태")
    contract_days_remaining: Optional[int] = Field(description="계약 종료까지 남은 일수")
    created_at: datetime
    updated_at: datetime
    
    # 담당자 정보 (Assignment에서 조회)
    assignments: Optional[List["AssignmentResponse"]] = Field(default=[], description="담당자 배정 목록")

    class Config:
        from_attributes = True

class CustomerListResponse(BaseModel):
    """고객사 목록 응답 스키마"""
    total: int
    customers: List[CustomerResponse]

# Assignment 스키마들
class AssignmentBase(BaseModel):
    """담당 배정 기본 스키마"""
    member_id: int = Field(..., description="담당 팀원 ID")
    customer_id: int = Field(..., description="담당 고객사 ID")
    role: AssignmentRoleEnum = Field(default=AssignmentRoleEnum.primary, description="담당 역할")
    assigned_date: date = Field(default_factory=date.today, description="배정 시작일")
    end_date: Optional[date] = Field(None, description="배정 종료일")
    is_primary: bool = Field(default=True, description="주 담당자 여부")
    responsibilities: Optional[str] = Field(None, description="담당 업무 및 책임 사항")

class AssignmentCreate(AssignmentBase):
    """담당 배정 생성 스키마"""
    pass

class AssignmentUpdate(BaseModel):
    """담당 배정 수정 스키마"""
    role: Optional[AssignmentRoleEnum] = Field(None, description="담당 역할")
    assigned_date: Optional[date] = Field(None, description="배정 시작일")
    end_date: Optional[date] = Field(None, description="배정 종료일")
    is_primary: Optional[bool] = Field(None, description="주 담당자 여부")
    responsibilities: Optional[str] = Field(None, description="담당 업무 및 책임 사항")

class MemberInfo(BaseModel):
    """팀원 정보 (다른 서비스에서 가져온 정보)"""
    id: int
    name: str
    email: str
    position: Optional[str] = None
    team: Optional[str] = None

class AssignmentResponse(AssignmentBase):
    """담당 배정 응답 스키마"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    # 계산된 속성들
    is_active: bool = Field(description="배정 활성 상태")
    duration_days: int = Field(description="배정 기간 (일수)")
    
    # 관련 정보 (다른 서비스에서 조회)
    member: Optional[MemberInfo] = Field(None, description="팀원 정보")
    customer: Optional[CustomerResponse] = Field(None, description="고객사 정보")

    class Config:
        from_attributes = True

class AssignmentListResponse(BaseModel):
    """담당 배정 목록 응답 스키마"""
    total: int
    assignments: List[AssignmentResponse]

# 통계 스키마들
class CustomerStats(BaseModel):
    """고객사 통계 스키마"""
    total_customers: int
    active_customers: int
    inactive_customers: int
    expired_customers: int
    expiring_soon: int
    active_rate: float

class AssignmentStats(BaseModel):
    """담당 배정 통계 스키마"""
    total_assignments: int
    active_assignments: int
    primary_assignments: int
    secondary_assignments: int
    backup_assignments: int
    assignments_by_member: dict

# 검색 및 필터 스키마들
class CustomerSearchParams(BaseModel):
    """고객사 검색 파라미터"""
    q: Optional[str] = Field(None, description="검색 키워드")
    status: Optional[CustomerStatusEnum] = Field(None, description="상태 필터")
    active_only: bool = Field(default=False, description="활성 고객사만 조회")
    contract_type: Optional[str] = Field(None, description="계약 유형 필터")

class AssignmentSearchParams(BaseModel):
    """담당 배정 검색 파라미터"""
    member_id: Optional[int] = Field(None, description="팀원 ID 필터")
    customer_id: Optional[int] = Field(None, description="고객사 ID 필터")
    role: Optional[AssignmentRoleEnum] = Field(None, description="역할 필터")
    active_only: bool = Field(default=False, description="활성 배정만 조회")

class PaginationParams(BaseModel):
    """페이지네이션 파라미터"""
    skip: int = Field(default=0, ge=0, description="건너뛸 개수")
    limit: int = Field(default=100, ge=1, le=1000, description="가져올 개수")

# Forward reference 해결
CustomerResponse.model_rebuild() 