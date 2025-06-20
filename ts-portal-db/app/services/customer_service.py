"""
고객사 관련 서비스 레이어
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from ..models.customer import Customer
from ..schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    """고객사 관련 비즈니스 로직"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_customer(self, customer_id: int) -> Optional[Customer]:
        """고객사 단일 조회"""
        return self.db.query(Customer).filter(Customer.id == customer_id).first()
    
    def get_customer_by_name(self, company_name: str) -> Optional[Customer]:
        """회사명으로 고객사 조회"""
        return self.db.query(Customer).filter(Customer.company_name == company_name).first()
    
    def get_customers(self, skip: int = 0, limit: int = 100, active_only: bool = False) -> List[Customer]:
        """고객사 목록 조회"""
        query = self.db.query(Customer)
        
        if active_only:
            query = query.filter(Customer.status == "Active")
        
        return query.offset(skip).limit(limit).all()
    
    def get_customers_count(self, active_only: bool = False) -> int:
        """고객사 총 개수"""
        query = self.db.query(Customer)
        
        if active_only:
            query = query.filter(Customer.status == "Active")
        
        return query.count()
    
    def create_customer(self, customer_data: CustomerCreate) -> Customer:
        """고객사 생성"""
        # 회사명 중복 체크
        existing_customer = self.get_customer_by_name(customer_data.company_name)
        if existing_customer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"고객사명 '{customer_data.company_name}'은 이미 등록되어 있습니다."
            )
        
        try:
            # 새 고객사 생성
            db_customer = Customer(**customer_data.model_dump())
            self.db.add(db_customer)
            self.db.commit()
            self.db.refresh(db_customer)
            return db_customer
        
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="고객사 생성 중 데이터 무결성 오류가 발생했습니다."
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="고객사 생성 중 오류가 발생했습니다."
            )
    
    def update_customer(self, customer_id: int, customer_data: CustomerUpdate) -> Optional[Customer]:
        """고객사 정보 수정"""
        db_customer = self.get_customer(customer_id)
        if not db_customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ID {customer_id}인 고객사를 찾을 수 없습니다."
            )
        
        # 회사명 중복 체크 (본인 제외)
        if customer_data.company_name:
            existing_customer = self.get_customer_by_name(customer_data.company_name)
            if existing_customer and existing_customer.id != customer_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"고객사명 '{customer_data.company_name}'은 이미 등록되어 있습니다."
                )
        
        try:
            # 수정할 필드만 업데이트
            update_data = customer_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_customer, field, value)
            
            self.db.commit()
            self.db.refresh(db_customer)
            return db_customer
        
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="고객사 정보 수정 중 데이터 무결성 오류가 발생했습니다."
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="고객사 정보 수정 중 오류가 발생했습니다."
            )
    
    def delete_customer(self, customer_id: int) -> bool:
        """고객사 삭제 (상태를 Inactive로 변경)"""
        db_customer = self.get_customer(customer_id)
        if not db_customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ID {customer_id}인 고객사를 찾을 수 없습니다."
            )
        
        try:
            # 상태를 Inactive로 변경
            db_customer.status = "Inactive"
            self.db.commit()
            return True
        
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="고객사 삭제 중 오류가 발생했습니다."
            )
    
    def activate_customer(self, customer_id: int) -> Optional[Customer]:
        """고객사 활성화 (상태를 Active로 변경)"""
        db_customer = self.get_customer(customer_id)
        if not db_customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ID {customer_id}인 고객사를 찾을 수 없습니다."
            )
        
        try:
            db_customer.status = "Active"
            self.db.commit()
            self.db.refresh(db_customer)
            return db_customer
        
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="고객사 활성화 중 오류가 발생했습니다."
            )
    
    def search_customers(self, query: str, active_only: bool = False) -> List[Customer]:
        """고객사 검색 (회사명, 담당자명, 담당자 이메일로 검색)"""
        db_query = self.db.query(Customer)
        
        if active_only:
            db_query = db_query.filter(Customer.status == "Active")
        
        # 회사명, 담당자명, 담당자 이메일에서 검색
        search_filter = (
            Customer.company_name.contains(query) |
            Customer.contact_person.contains(query) |
            Customer.contact_email.contains(query)
        )
        
        return db_query.filter(search_filter).all()
    
    def get_customers_by_status(self, status: str) -> List[Customer]:
        """상태별 고객사 조회"""
        return self.db.query(Customer).filter(Customer.status == status).all()
    
    def get_expiring_customers(self, days: int = 30) -> List[Customer]:
        """계약 만료 예정 고객사 조회"""
        from datetime import date, timedelta
        
        expiry_date = date.today() + timedelta(days=days)
        
        return self.db.query(Customer).filter(
            Customer.contract_end.isnot(None),
            Customer.contract_end <= expiry_date,
            Customer.status == "Active"
        ).all() 