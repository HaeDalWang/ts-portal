"""
Customer Service API 라우터
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Header, status
from sqlalchemy.orm import Session

from .database import get_db
from .service import CustomerService, AssignmentService
from .schemas import (
    CustomerCreate, CustomerUpdate, CustomerResponse, CustomerListResponse,
    AssignmentCreate, AssignmentUpdate, AssignmentResponse, AssignmentListResponse,
    CustomerStats, AssignmentStats, CustomerSearchParams, AssignmentSearchParams,
    PaginationParams, CustomerStatusEnum, AssignmentRoleEnum
)

# Customer 라우터
customers_router = APIRouter(prefix="/customers", tags=["customers"])

def get_customer_service(db: Session = Depends(get_db)) -> CustomerService:
    return CustomerService(db)

def get_current_user_id(x_user_id: int = Header(..., alias="X-User-ID")) -> int:
    return x_user_id

def get_current_user_role(x_user_role: str = Header(..., alias="X-User-Role")) -> str:
    return x_user_role

@customers_router.post("/", response_model=CustomerResponse, summary="고객사 생성")
async def create_customer(
    customer_data: CustomerCreate,
    service: CustomerService = Depends(get_customer_service),
    current_user_role: str = Depends(get_current_user_role)
):
    # 권한 체크 (관리자 또는 파워유저만)
    if current_user_role not in ["admin", "power_user"]:
        raise HTTPException(status_code=403, detail="고객사 생성 권한이 없습니다.")
    
    try:
        return service.create_customer(customer_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@customers_router.get("/", response_model=CustomerListResponse, summary="고객사 목록 조회")
async def get_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    q: str = Query(None),
    status: CustomerStatusEnum = Query(None),
    active_only: bool = Query(False),
    contract_type: str = Query(None),
    service: CustomerService = Depends(get_customer_service)
):
    pagination = PaginationParams(skip=skip, limit=limit)
    search_params = None
    
    if any([q, status, active_only, contract_type]):
        search_params = CustomerSearchParams(
            q=q, status=status, active_only=active_only, contract_type=contract_type
        )
    
    return service.get_customers(pagination, search_params)

@customers_router.get("/search", response_model=List[CustomerResponse], summary="고객사 검색")
async def search_customers(
    q: str = Query(..., min_length=1),
    active_only: bool = Query(False),
    service: CustomerService = Depends(get_customer_service)
):
    return service.search_customers(q, active_only)

@customers_router.get("/expiring", response_model=List[CustomerResponse], summary="계약 만료 예정")
async def get_expiring_customers(
    days: int = Query(30, ge=1, le=365),
    service: CustomerService = Depends(get_customer_service)
):
    return service.get_expiring_customers(days)

@customers_router.get("/stats", response_model=CustomerStats, summary="고객사 통계")
async def get_customer_stats(service: CustomerService = Depends(get_customer_service)):
    return service.get_customer_stats()

@customers_router.get("/{customer_id}", response_model=CustomerResponse, summary="고객사 조회")
async def get_customer(
    customer_id: int,
    service: CustomerService = Depends(get_customer_service)
):
    customer = service.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="고객사를 찾을 수 없습니다.")
    return customer

@customers_router.put("/{customer_id}", response_model=CustomerResponse, summary="고객사 수정")
async def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    service: CustomerService = Depends(get_customer_service),
    current_user_role: str = Depends(get_current_user_role)
):
    if current_user_role not in ["admin", "power_user"]:
        raise HTTPException(status_code=403, detail="고객사 수정 권한이 없습니다.")
    
    try:
        customer = service.update_customer(customer_id, customer_data)
        if not customer:
            raise HTTPException(status_code=404, detail="고객사를 찾을 수 없습니다.")
        return customer
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@customers_router.delete("/{customer_id}", summary="고객사 삭제")
async def delete_customer(
    customer_id: int,
    service: CustomerService = Depends(get_customer_service),
    current_user_role: str = Depends(get_current_user_role)
):
    if current_user_role != "admin":
        raise HTTPException(status_code=403, detail="고객사 삭제 권한이 없습니다.")
    
    success = service.delete_customer(customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="고객사를 찾을 수 없습니다.")
    return {"message": "고객사가 비활성화되었습니다."}

# Assignment 라우터
assignments_router = APIRouter(prefix="/assignments", tags=["assignments"])

def get_assignment_service(db: Session = Depends(get_db)) -> AssignmentService:
    return AssignmentService(db)

@assignments_router.post("/", response_model=AssignmentResponse, summary="담당자 배정")
async def create_assignment(
    assignment_data: AssignmentCreate,
    service: AssignmentService = Depends(get_assignment_service),
    current_user_role: str = Depends(get_current_user_role)
):
    if current_user_role not in ["admin", "power_user"]:
        raise HTTPException(status_code=403, detail="담당자 배정 권한이 없습니다.")
    
    try:
        return service.create_assignment(assignment_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@assignments_router.get("/member/{member_id}", response_model=List[AssignmentResponse], summary="팀원별 담당 고객사")
async def get_assignments_by_member(
    member_id: int,
    active_only: bool = Query(False),
    service: AssignmentService = Depends(get_assignment_service)
):
    return service.get_assignments_by_member(member_id, active_only)

@assignments_router.get("/customer/{customer_id}", response_model=List[AssignmentResponse], summary="고객사별 담당자")
async def get_assignments_by_customer(
    customer_id: int,
    active_only: bool = Query(False),
    service: AssignmentService = Depends(get_assignment_service)
):
    return service.get_assignments_by_customer(customer_id, active_only)

@assignments_router.get("/{assignment_id}", response_model=AssignmentResponse, summary="담당 배정 조회")
async def get_assignment(
    assignment_id: int,
    service: AssignmentService = Depends(get_assignment_service)
):
    assignment = service.get_assignment(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="담당 배정을 찾을 수 없습니다.")
    return assignment

@assignments_router.put("/{assignment_id}", response_model=AssignmentResponse, summary="담당 배정 수정")
async def update_assignment(
    assignment_id: int,
    assignment_data: AssignmentUpdate,
    service: AssignmentService = Depends(get_assignment_service),
    current_user_role: str = Depends(get_current_user_role)
):
    if current_user_role not in ["admin", "power_user"]:
        raise HTTPException(status_code=403, detail="담당 배정 수정 권한이 없습니다.")
    
    assignment = service.update_assignment(assignment_id, assignment_data)
    if not assignment:
        raise HTTPException(status_code=404, detail="담당 배정을 찾을 수 없습니다.")
    return assignment

@assignments_router.delete("/{assignment_id}", summary="담당 배정 삭제")
async def delete_assignment(
    assignment_id: int,
    service: AssignmentService = Depends(get_assignment_service),
    current_user_role: str = Depends(get_current_user_role)
):
    if current_user_role not in ["admin", "power_user"]:
        raise HTTPException(status_code=403, detail="담당 배정 삭제 권한이 없습니다.")
    
    success = service.delete_assignment(assignment_id)
    if not success:
        raise HTTPException(status_code=404, detail="담당 배정을 찾을 수 없습니다.")
    return {"message": "담당 배정이 삭제되었습니다."} 