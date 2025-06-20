"""
팀원 정보 모델
"""

from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Boolean
from sqlalchemy.orm import relationship

from ..database import Base


class Member(Base):
    """팀원 정보 테이블"""
    
    __tablename__ = "members"
    
    # 기본 정보
    id = Column(Integer, primary_key=True, index=True, comment="팀원 고유 ID")
    name = Column(String(50), nullable=False, comment="이름")
    email = Column(String(100), unique=True, nullable=False, index=True, comment="이메일")
    phone = Column(String(20), comment="전화번호")
    
    # 직무 정보
    position = Column(String(50), comment="직급/직책 (예: 선임, 책임, 팀장)")
    team = Column(String(50), default="TS팀", comment="소속팀")
    skills = Column(Text, comment="보유 기술 (쉼표로 구분)")
    
    # 날짜 정보
    join_date = Column(Date, comment="입사일")
    is_active = Column(Boolean, default=True, comment="재직 여부")
    
    # 추가 정보
    profile_image = Column(String(200), comment="프로필 사진 URL")
    
    # 시스템 정보
    created_at = Column(DateTime, default=datetime.utcnow, comment="생성일시")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="수정일시")
    
    # 관계 설정
    assignments = relationship("Assignment", back_populates="member", cascade="all, delete-orphan")
    created_events = relationship("Event", back_populates="creator")
    notices = relationship("Notice", back_populates="author", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Member(id={self.id}, name='{self.name}', email='{self.email}')>"
    
    @property
    def skills_list(self):
        """기술 목록을 리스트로 반환"""
        if self.skills:
            return [skill.strip() for skill in self.skills.split(",") if skill.strip()]
        return []
    
    @skills_list.setter
    def skills_list(self, skills):
        """기술 목록을 문자열로 저장"""
        if isinstance(skills, list):
            self.skills = ", ".join(skills)
        else:
            self.skills = skills 