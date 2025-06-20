"""
고객사 정보 모델
"""

from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Text, Date, DateTime
from sqlalchemy.orm import relationship

from ..database import Base


class Customer(Base):
    """고객사 정보 테이블"""
    
    __tablename__ = "customers"
    
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
    created_at = Column(DateTime, default=datetime.utcnow, comment="생성일시")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="수정일시")
    
    # 관계 설정
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