"""
고객사 담당 배정 모델
"""

from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class Assignment(Base):
    """고객사 담당 배정 테이블"""
    
    __tablename__ = "assignments"
    
    # 기본 정보
    id = Column(Integer, primary_key=True, index=True, comment="배정 고유 ID")
    
    # 외래 키
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, comment="담당 팀원 ID")
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, comment="담당 고객사 ID")
    
    # 배정 정보
    role = Column(String(20), default="Primary", comment="담당 역할 (Primary, Secondary, Backup)")
    assigned_date = Column(Date, default=date.today, comment="배정 시작일")
    end_date = Column(Date, comment="배정 종료일")
    is_primary = Column(Boolean, default=True, comment="주 담당자 여부")
    
    # 업무 내용
    responsibilities = Column(Text, comment="담당 업무 및 책임 사항")
    
    # 시스템 정보
    created_at = Column(DateTime, default=datetime.utcnow, comment="생성일시")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="수정일시")
    
    # 관계 설정
    member = relationship("Member", back_populates="assignments")
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