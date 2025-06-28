"""
Customer Service 모델 정의
"""

from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Customer(Base):
    """고객사 정보 테이블 (customer_schema.customers)"""
    __tablename__ = "customers"
    __table_args__ = {"schema": "customer_schema"}

    # 기본 정보
    id = Column(Integer, primary_key=True, index=True, comment="고객사 고유 ID")
    company_name = Column(String(100), nullable=False, unique=True, index=True, comment="고객사명")
    
    # 담당자 정보
    contact_person = Column(String(50), comment="담당자명")
    contact_email = Column(String(100), comment="담당자 이메일")
    contact_phone = Column(String(20), comment="담당자 전화번호")
    
    # 계약 정보
    contract_type = Column(String(50), comment="계약 유형 (예: Full MSP, Consulting, Support)")
    contract_start = Column(Date, comment="계약 시작일")
    contract_end = Column(Date, comment="계약 종료일")
    
    # 상태 및 메모
    status = Column(String(20), default="Active", comment="상태 (Active, Pending, Expired, Suspended)")
    notes = Column(Text, comment="특이사항 및 메모")
    
    # 시스템 정보
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성일시")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="수정일시")
    
    # 관계 설정 (Assignment와의 관계)
    assignments = relationship("Assignment", back_populates="customer", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Customer(id={self.id}, company_name='{self.company_name}', status='{self.status}')>"
    
    @property
    def is_active(self):
        """계약이 활성 상태인지 확인"""
        return self.status == "Active"
    
    @property
    def contract_days_remaining(self):
        """계약 종료까지 남은 일수"""
        if self.contract_end:
            today = date.today()
            if self.contract_end > today:
                return (self.contract_end - today).days
            else:
                return 0  # 계약 만료
        return None  # 종료일 미설정

class Assignment(Base):
    """고객사 담당 배정 테이블 (customer_schema.assignments)"""
    __tablename__ = "assignments"
    __table_args__ = {"schema": "customer_schema"}

    # 기본 정보
    id = Column(Integer, primary_key=True, index=True, comment="배정 고유 ID")
    
    # 외래 키 (다른 서비스의 ID를 단순 저장)
    member_id = Column(Integer, nullable=False, comment="담당 팀원 ID")
    customer_id = Column(Integer, ForeignKey("customer_schema.customers.id"), nullable=False, comment="담당 고객사 ID")
    
    # 배정 정보
    role = Column(String(20), default="Primary", comment="담당 역할 (Primary, Secondary, Backup)")
    assigned_date = Column(Date, default=date.today, comment="배정 시작일")
    end_date = Column(Date, comment="배정 종료일")
    is_primary = Column(Boolean, default=True, comment="주 담당자 여부")
    
    # 업무 내용
    responsibilities = Column(Text, comment="담당 업무 및 책임 사항")
    
    # 시스템 정보
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성일시")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="수정일시")
    
    # 관계 설정 (Customer와의 관계만, Member는 다른 서비스)
    customer = relationship("Customer", back_populates="assignments")
    
    def __repr__(self):
        return f"<Assignment(id={self.id}, member_id={self.member_id}, customer_id={self.customer_id}, role='{self.role}')>"
    
    @property
    def is_active(self):
        """배정이 활성 상태인지 확인"""
        today = date.today()
        if self.end_date:
            return self.assigned_date <= today <= self.end_date
        return self.assigned_date <= today
    
    @property
    def duration_days(self):
        """배정 기간 (일수)"""
        if self.end_date:
            return (self.end_date - self.assigned_date).days
        else:
            # 종료일이 없으면 현재까지의 기간
            return (date.today() - self.assigned_date).days 