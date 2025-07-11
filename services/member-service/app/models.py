"""
Member Service - 데이터베이스 모델

팀원 정보 모델 정의
"""

from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Boolean, Enum

from .database import Base

# shared 모듈 import를 위한 경로 추가
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.types import UserRole, has_permission, is_admin, is_power_user_or_above


class Member(Base):
    """팀원 정보 테이블 (기존 Auth Service 스키마와 호환)"""
    
    __tablename__ = "members"
    __table_args__ = {"schema": "member_schema"}
    
    # 기본 정보 (기존 스키마와 일치)
    id = Column(Integer, primary_key=True, index=True, comment="팀원 고유 ID")
    name = Column(String(50), nullable=False, comment="이름")
    username = Column(String(50), unique=True, nullable=True, index=True, comment="로그인 ID")
    email = Column(String(100), unique=True, nullable=False, index=True, comment="이메일")
    phone = Column(String(20), comment="전화번호")
    
    # 인증 정보 (기존 스키마와 일치)
    password_hash = Column(String(255), comment="비밀번호 해시")
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False, comment="사용자 권한")
    last_login = Column(DateTime, comment="마지막 로그인 시간")
    
    # 직무 정보 (기존 스키마와 일치)
    position = Column(String(50), comment="직급/직책 (예: 선임, 책임, 팀장)")
    team = Column(String(50), default="TS팀", comment="소속팀")
    skills = Column(Text, comment="보유 기술 (쉼표로 구분)")
    
    # 날짜 정보 (기존 스키마와 일치)
    join_date = Column(Date, comment="입사일")
    is_active = Column(Boolean, default=True, comment="재직 여부")
    
    # 추가 정보 (기존 스키마와 일치)
    profile_image_url = Column(String(500), comment="프로필 사진 URL")
    
    # 시스템 정보 (기존 스키마와 일치)
    created_at = Column(DateTime, default=datetime.utcnow, comment="생성일시")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="수정일시")
    
    def __repr__(self):
        return f"<Member(id={self.id}, name='{self.name}', email='{self.email}', role='{self.role}')>"
    
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
    
    def has_permission(self, required_role: UserRole) -> bool:
        """권한 확인"""
        return has_permission(self.role, required_role)
    
    def is_admin(self) -> bool:
        """관리자 권한 확인"""
        return is_admin(self.role)
    
    def is_power_user_or_above(self) -> bool:
        """파워유저 이상 권한 확인"""
        return is_power_user_or_above(self.role) 