"""
Customer Service 비즈니스 로직
"""

from typing import List, Optional, Dict, Any
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_, func

from .models import Customer, Assignment
from .schemas import (
    CustomerCreate, CustomerUpdate, CustomerResponse, CustomerListResponse,
    AssignmentCreate, AssignmentUpdate, AssignmentResponse, AssignmentListResponse,
    CustomerStats, AssignmentStats, CustomerSearchParams, AssignmentSearchParams,
    PaginationParams, MemberInfo
)

class CustomerService:
    """고객사 관리 서비스"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # Customer 관련 메서드들
    def create_customer(self, customer_data: CustomerCreate) -> CustomerResponse:
        """고객사 생성"""
        existing = self.db.query(Customer).filter(
            Customer.company_name == customer_data.company_name
        ).first()
        
        if existing:
            raise ValueError(f"고객사명 '{customer_data.company_name}'은 이미 등록되어 있습니다.")
        
        customer_dict = customer_data.model_dump()
        if customer_dict.get('status') and hasattr(customer_dict['status'], 'value'):
            customer_dict['status'] = customer_dict['status'].value
        
        customer = Customer(**customer_dict)
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        
        return self._to_customer_response(customer)
    
    def get_customer(self, customer_id: int) -> Optional[CustomerResponse]:
        """고객사 단일 조회"""
        customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
        return self._to_customer_response(customer) if customer else None
    
    def get_customers(self, params: PaginationParams, search_params: Optional[CustomerSearchParams] = None) -> CustomerListResponse:
        """고객사 목록 조회"""
        query = self.db.query(Customer)
        
        if search_params:
            if search_params.q:
                search_term = f"%{search_params.q}%"
                query = query.filter(
                    or_(
                        Customer.company_name.ilike(search_term),
                        Customer.contact_person.ilike(search_term),
                        Customer.contact_email.ilike(search_term)
                    )
                )
            
            if search_params.status:
                query = query.filter(Customer.status == search_params.status.value)
            
            if search_params.active_only:
                query = query.filter(Customer.status == "Active")
            
            if search_params.contract_type:
                query = query.filter(Customer.contract_type == search_params.contract_type)
        
        query = query.order_by(Customer.company_name)
        total = query.count()
        customers = query.offset(params.skip).limit(params.limit).all()
        
        return CustomerListResponse(
            total=total,
            customers=[self._to_customer_response(customer) for customer in customers]
        )
    
    def update_customer(self, customer_id: int, customer_data: CustomerUpdate) -> Optional[CustomerResponse]:
        """고객사 수정"""
        customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            return None
        
        if customer_data.company_name:
            existing = self.db.query(Customer).filter(
                and_(
                    Customer.company_name == customer_data.company_name,
                    Customer.id != customer_id
                )
            ).first()
            
            if existing:
                raise ValueError(f"고객사명 '{customer_data.company_name}'은 이미 등록되어 있습니다.")
        
        update_data = customer_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "status" and value:
                setattr(customer, field, value.value)
            else:
                setattr(customer, field, value)
        
        self.db.commit()
        self.db.refresh(customer)
        return self._to_customer_response(customer)
    
    def delete_customer(self, customer_id: int) -> bool:
        """고객사 삭제"""
        customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            return False
        
        customer.status = "Inactive"
        self.db.commit()
        return True
    
    def search_customers(self, query_string: str, active_only: bool = False) -> List[CustomerResponse]:
        """고객사 검색"""
        query = self.db.query(Customer)
        
        if active_only:
            query = query.filter(Customer.status == "Active")
        
        search_term = f"%{query_string}%"
        query = query.filter(
            or_(
                Customer.company_name.ilike(search_term),
                Customer.contact_person.ilike(search_term),
                Customer.contact_email.ilike(search_term)
            )
        )
        
        customers = query.order_by(Customer.company_name).all()
        return [self._to_customer_response(customer) for customer in customers]
    
    def get_customers_by_status(self, status: str) -> List[CustomerResponse]:
        """상태별 고객사 조회"""
        customers = self.db.query(Customer).filter(
            Customer.status == status
        ).order_by(Customer.company_name).all()
        
        return [self._to_customer_response(customer) for customer in customers]
    
    def get_expiring_customers(self, days: int = 30) -> List[CustomerResponse]:
        """계약 만료 예정 고객사 조회"""
        expiry_date = date.today() + timedelta(days=days)
        
        customers = self.db.query(Customer).filter(
            and_(
                Customer.contract_end.isnot(None),
                Customer.contract_end <= expiry_date,
                Customer.status == "Active"
            )
        ).order_by(Customer.contract_end).all()
        
        return [self._to_customer_response(customer) for customer in customers]
    
    def get_customer_stats(self) -> CustomerStats:
        """고객사 통계"""
        total = self.db.query(Customer).count()
        active = self.db.query(Customer).filter(Customer.status == "Active").count()
        inactive = self.db.query(Customer).filter(Customer.status == "Inactive").count()
        expired = self.db.query(Customer).filter(Customer.status == "Expired").count()
        
        expiry_date = date.today() + timedelta(days=30)
        expiring_soon = self.db.query(Customer).filter(
            and_(
                Customer.contract_end.isnot(None),
                Customer.contract_end <= expiry_date,
                Customer.status == "Active"
            )
        ).count()
        
        active_rate = round((active / total * 100) if total > 0 else 0, 2)
        
        return CustomerStats(
            total_customers=total,
            active_customers=active,
            inactive_customers=inactive,
            expired_customers=expired,
            expiring_soon=expiring_soon,
            active_rate=active_rate
        )
    
    def _to_customer_response(self, customer: Customer) -> CustomerResponse:
        """Customer 모델을 CustomerResponse로 변환"""
        return CustomerResponse(
            id=customer.id,
            company_name=customer.company_name,
            contact_person=customer.contact_person,
            contact_email=customer.contact_email,
            contact_phone=customer.contact_phone,
            contract_type=customer.contract_type,
            contract_start=customer.contract_start,
            contract_end=customer.contract_end,
            status=customer.status,
            notes=customer.notes,
            is_active=customer.is_active,
            contract_days_remaining=customer.contract_days_remaining,
            created_at=customer.created_at,
            updated_at=customer.updated_at,
            assignments=[]
        )

class AssignmentService:
    """담당자 배정 관리 서비스"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_assignment(self, assignment_data: AssignmentCreate) -> AssignmentResponse:
        """담당자 배정 생성"""
        customer = self.db.query(Customer).filter(Customer.id == assignment_data.customer_id).first()
        if not customer:
            raise ValueError(f"고객사 ID {assignment_data.customer_id}를 찾을 수 없습니다.")
        
        if assignment_data.is_primary:
            existing_primary = self.db.query(Assignment).filter(
                and_(
                    Assignment.customer_id == assignment_data.customer_id,
                    Assignment.is_primary == True,
                    Assignment.end_date.is_(None)
                )
            ).first()
            
            if existing_primary:
                existing_primary.is_primary = False
                existing_primary.role = "Secondary"
        
        assignment_dict = assignment_data.model_dump()
        if assignment_dict.get('role') and hasattr(assignment_dict['role'], 'value'):
            assignment_dict['role'] = assignment_dict['role'].value
        
        assignment = Assignment(**assignment_dict)
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        
        return self._to_assignment_response(assignment)
    
    def get_assignment(self, assignment_id: int) -> Optional[AssignmentResponse]:
        """담당자 배정 단일 조회"""
        assignment = self.db.query(Assignment).filter(Assignment.id == assignment_id).first()
        return self._to_assignment_response(assignment) if assignment else None
    
    def get_assignments(self, params: PaginationParams, search_params: Optional[AssignmentSearchParams] = None) -> AssignmentListResponse:
        """담당자 배정 목록 조회"""
        query = self.db.query(Assignment)
        
        if search_params:
            if search_params.member_id:
                query = query.filter(Assignment.member_id == search_params.member_id)
            
            if search_params.customer_id:
                query = query.filter(Assignment.customer_id == search_params.customer_id)
            
            if search_params.role:
                query = query.filter(Assignment.role == search_params.role.value)
            
            if search_params.active_only:
                today = date.today()
                query = query.filter(
                    and_(
                        Assignment.assigned_date <= today,
                        or_(
                            Assignment.end_date.is_(None),
                            Assignment.end_date >= today
                        )
                    )
                )
        
        query = query.order_by(desc(Assignment.assigned_date))
        total = query.count()
        assignments = query.offset(params.skip).limit(params.limit).all()
        
        return AssignmentListResponse(
            total=total,
            assignments=[self._to_assignment_response(assignment) for assignment in assignments]
        )
    
    def get_assignments_by_member(self, member_id: int, active_only: bool = False) -> List[AssignmentResponse]:
        """특정 팀원의 담당 배정 조회"""
        query = self.db.query(Assignment).filter(Assignment.member_id == member_id)
        
        if active_only:
            today = date.today()
            query = query.filter(
                and_(
                    Assignment.assigned_date <= today,
                    or_(
                        Assignment.end_date.is_(None),
                        Assignment.end_date >= today
                    )
                )
            )
        
        assignments = query.order_by(desc(Assignment.assigned_date)).all()
        return [self._to_assignment_response(assignment) for assignment in assignments]
    
    def get_assignments_by_customer(self, customer_id: int, active_only: bool = False) -> List[AssignmentResponse]:
        """특정 고객사의 담당자 배정 조회"""
        query = self.db.query(Assignment).filter(Assignment.customer_id == customer_id)
        
        if active_only:
            today = date.today()
            query = query.filter(
                and_(
                    Assignment.assigned_date <= today,
                    or_(
                        Assignment.end_date.is_(None),
                        Assignment.end_date >= today
                    )
                )
            )
        
        assignments = query.order_by(Assignment.is_primary.desc(), Assignment.assigned_date.desc()).all()
        return [self._to_assignment_response(assignment) for assignment in assignments]
    
    def update_assignment(self, assignment_id: int, assignment_data: AssignmentUpdate) -> Optional[AssignmentResponse]:
        """담당자 배정 수정"""
        assignment = self.db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not assignment:
            return None
        
        if assignment_data.is_primary and assignment_data.is_primary != assignment.is_primary:
            existing_primary = self.db.query(Assignment).filter(
                and_(
                    Assignment.customer_id == assignment.customer_id,
                    Assignment.is_primary == True,
                    Assignment.id != assignment_id,
                    Assignment.end_date.is_(None)
                )
            ).first()
            
            if existing_primary:
                existing_primary.is_primary = False
                existing_primary.role = "Secondary"
        
        update_data = assignment_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "role" and value:
                setattr(assignment, field, value.value)
            else:
                setattr(assignment, field, value)
        
        self.db.commit()
        self.db.refresh(assignment)
        return self._to_assignment_response(assignment)
    
    def delete_assignment(self, assignment_id: int) -> bool:
        """담당자 배정 삭제"""
        assignment = self.db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not assignment:
            return False
        
        self.db.delete(assignment)
        self.db.commit()
        return True
    
    def get_assignment_stats(self) -> AssignmentStats:
        """담당자 배정 통계"""
        total_assignments = self.db.query(Assignment).count()
        
        # 활성 배정 (종료일이 없거나 미래인 것)
        today = date.today()
        active_assignments = self.db.query(Assignment).filter(
            and_(
                Assignment.assigned_date <= today,
                or_(
                    Assignment.end_date.is_(None),
                    Assignment.end_date >= today
                )
            )
        ).count()
        
        # 역할별 통계
        primary_assignments = self.db.query(Assignment).filter(Assignment.role == "Primary").count()
        secondary_assignments = self.db.query(Assignment).filter(Assignment.role == "Secondary").count()
        backup_assignments = self.db.query(Assignment).filter(Assignment.role == "Backup").count()
        
        # 팀원별 통계 (ID만 - 이름은 다른 서비스에서 조회)
        member_stats = self.db.query(
            Assignment.member_id,
            func.count(Assignment.id).label('count')
        ).group_by(Assignment.member_id).all()
        
        assignments_by_member = {
            f"member_{member_id}": count for member_id, count in member_stats
        }
        
        return AssignmentStats(
            total_assignments=total_assignments,
            active_assignments=active_assignments,
            primary_assignments=primary_assignments,
            secondary_assignments=secondary_assignments,
            backup_assignments=backup_assignments,
            assignments_by_member=assignments_by_member
        )
    
    def _to_assignment_response(self, assignment: Assignment) -> AssignmentResponse:
        """Assignment 모델을 AssignmentResponse로 변환"""
        return AssignmentResponse(
            id=assignment.id,
            member_id=assignment.member_id,
            customer_id=assignment.customer_id,
            role=assignment.role,
            assigned_date=assignment.assigned_date,
            end_date=assignment.end_date,
            is_primary=assignment.is_primary,
            responsibilities=assignment.responsibilities,
            created_at=assignment.created_at,
            updated_at=assignment.updated_at,
            is_active=assignment.is_active,
            duration_days=assignment.duration_days,
            member=None,
            customer=None
        ) 