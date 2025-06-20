"""
고객사 관련 Pydantic 스키마
"""

from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


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
    status: str = Field(default="Active", description="상태")


class CustomerUpdate(BaseModel):
    """고객사 수정 스키마"""
    company_name: Optional[str] = Field(None, min_length=1, max_length=100, description="고객사명")
    contact_person: Optional[str] = Field(None, max_length=50, description="담당자명")
    contact_email: Optional[str] = Field(None, description="담당자 이메일")
    contact_phone: Optional[str] = Field(None, max_length=20, description="담당자 전화번호")
    contract_type: Optional[str] = Field(None, max_length=50, description="계약 유형")
    contract_start: Optional[date] = Field(None, description="계약 시작일")
    contract_end: Optional[date] = Field(None, description="계약 종료일")
    status: Optional[str] = Field(None, description="상태")
    notes: Optional[str] = Field(None, description="특이사항 및 메모")


class CustomerResponse(CustomerBase):
    """고객사 응답 스키마"""
    id: int
    status: str
    is_active: bool = Field(description="계약 활성 상태")
    contract_days_remaining: Optional[int] = Field(description="계약 종료까지 남은 일수")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_with_calculated(cls, customer):
        """ORM 객체에서 계산된 필드 포함하여 변환"""
        data = {
            "id": customer.id,
            "company_name": customer.company_name,
            "contact_person": customer.contact_person,
            "contact_email": customer.contact_email,
            "contact_phone": customer.contact_phone,
            "contract_type": customer.contract_type,
            "contract_start": customer.contract_start,
            "contract_end": customer.contract_end,
            "status": customer.status,
            "notes": customer.notes,
            "is_active": customer.is_active,
            "contract_days_remaining": customer.contract_days_remaining,
            "created_at": customer.created_at,
            "updated_at": customer.updated_at
        }
        return cls(**data)


class CustomerListResponse(BaseModel):
    """고객사 목록 응답 스키마"""
    total: int
    customers: List[CustomerResponse] 