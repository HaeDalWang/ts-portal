"""
고객사 관련 API 라우터
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.customer_service import CustomerService
from ..schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    CustomerListResponse
)

# 라우터 생성
router = APIRouter(
    prefix="/customers",
    tags=["customers"],
    responses={404: {"description": "고객사를 찾을 수 없습니다"}}
)


def get_customer_service(db: Session = Depends(get_db)) -> CustomerService:
    """고객사 서비스 의존성 주입"""
    return CustomerService(db)


@router.get("/", response_model=CustomerListResponse, summary="고객사 목록 조회")
async def get_customers(
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
    limit: int = Query(100, ge=1, le=1000, description="가져올 개수"),
    active_only: bool = Query(False, description="활성 고객사만 조회"),
    service: CustomerService = Depends(get_customer_service)
):
    """
    고객사 목록을 조회합니다.
    
    - **skip**: 건너뛸 개수 (페이징용)
    - **limit**: 가져올 개수 (최대 1000)
    - **active_only**: True면 활성 고객사만, False면 전체 조회
    """
    customers = service.get_customers(skip=skip, limit=limit, active_only=active_only)
    total = service.get_customers_count(active_only=active_only)
    
    # 응답 데이터 변환
    customer_responses = [
        CustomerResponse.from_orm_with_calculated(customer) for customer in customers
    ]
    
    return CustomerListResponse(total=total, customers=customer_responses)


@router.get("/search", response_model=List[CustomerResponse], summary="고객사 검색")
async def search_customers(
    q: str = Query(..., min_length=1, description="검색어 (회사명, 담당자명, 담당자 이메일)"),
    active_only: bool = Query(False, description="활성 고객사만 검색"),
    service: CustomerService = Depends(get_customer_service)
):
    """
    고객사를 검색합니다.
    
    - **q**: 검색어 (회사명, 담당자명, 담당자 이메일에서 검색)
    - **active_only**: True면 활성 고객사만, False면 전체에서 검색
    """
    customers = service.search_customers(query=q, active_only=active_only)
    
    return [CustomerResponse.from_orm_with_calculated(customer) for customer in customers]


@router.get("/status/{status}", response_model=List[CustomerResponse], summary="상태별 고객사 조회")
async def get_customers_by_status(
    status: str,
    service: CustomerService = Depends(get_customer_service)
):
    """
    특정 상태의 고객사를 조회합니다.
    
    - **status**: 고객사 상태 (Active, Inactive, Expired 등)
    """
    customers = service.get_customers_by_status(status)
    
    return [CustomerResponse.from_orm_with_calculated(customer) for customer in customers]


@router.get("/expiring", response_model=List[CustomerResponse], summary="계약 만료 예정 고객사 조회")
async def get_expiring_customers(
    days: int = Query(30, ge=1, le=365, description="몇 일 이내 만료 고객사 조회"),
    service: CustomerService = Depends(get_customer_service)
):
    """
    계약 만료 예정 고객사를 조회합니다.
    
    - **days**: 몇 일 이내 만료 고객사를 조회할지 (기본값: 30일)
    """
    customers = service.get_expiring_customers(days=days)
    
    return [CustomerResponse.from_orm_with_calculated(customer) for customer in customers]


@router.get("/{customer_id}", response_model=CustomerResponse, summary="고객사 단일 조회")
async def get_customer(
    customer_id: int,
    service: CustomerService = Depends(get_customer_service)
):
    """
    특정 고객사의 상세 정보를 조회합니다.
    
    - **customer_id**: 고객사 ID
    """
    customer = service.get_customer(customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {customer_id}인 고객사를 찾을 수 없습니다."
        )
    
    return CustomerResponse.from_orm_with_calculated(customer)


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED, summary="고객사 생성")
async def create_customer(
    customer_data: CustomerCreate,
    service: CustomerService = Depends(get_customer_service)
):
    """
    새 고객사를 등록합니다.
    
    - **customer_data**: 고객사 정보
    """
    customer = service.create_customer(customer_data)
    return CustomerResponse.from_orm_with_calculated(customer)


@router.put("/{customer_id}", response_model=CustomerResponse, summary="고객사 정보 수정")
async def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    service: CustomerService = Depends(get_customer_service)
):
    """
    고객사 정보를 수정합니다.
    
    - **customer_id**: 고객사 ID
    - **customer_data**: 수정할 고객사 정보
    """
    customer = service.update_customer(customer_id, customer_data)
    return CustomerResponse.from_orm_with_calculated(customer)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT, summary="고객사 삭제")
async def delete_customer(
    customer_id: int,
    service: CustomerService = Depends(get_customer_service)
):
    """
    고객사를 삭제합니다. (상태를 Inactive로 변경)
    
    - **customer_id**: 고객사 ID
    """
    service.delete_customer(customer_id)


@router.patch("/{customer_id}/activate", response_model=CustomerResponse, summary="고객사 활성화")
async def activate_customer(
    customer_id: int,
    service: CustomerService = Depends(get_customer_service)
):
    """
    고객사를 활성화합니다. (상태를 Active로 변경)
    
    - **customer_id**: 고객사 ID
    """
    customer = service.activate_customer(customer_id)
    return CustomerResponse.from_orm_with_calculated(customer)


@router.get("/stats/summary", summary="고객사 통계")
async def get_customer_stats(
    service: CustomerService = Depends(get_customer_service)
):
    """
    고객사 관련 통계를 조회합니다.
    """
    total_customers = service.get_customers_count(active_only=False)
    active_customers = service.get_customers_count(active_only=True)
    inactive_customers = total_customers - active_customers
    
    # 상태별 통계
    active_list = service.get_customers_by_status("Active")
    inactive_list = service.get_customers_by_status("Inactive")
    expired_list = service.get_customers_by_status("Expired")
    
    # 만료 예정 고객사 (30일 이내)
    expiring_soon = service.get_expiring_customers(days=30)
    
    return {
        "total_customers": total_customers,
        "active_customers": len(active_list),
        "inactive_customers": len(inactive_list),
        "expired_customers": len(expired_list),
        "expiring_soon": len(expiring_soon),
        "active_rate": round((len(active_list) / total_customers * 100) if total_customers > 0 else 0, 2)
    } 