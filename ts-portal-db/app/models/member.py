"""
팀원 정보 모델
"""

from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
import enum

from ..database import Base


class UserRole(str, enum.Enum):
    """사용자 권한 레벨"""
    ADMIN = "admin"           # 관리자: 모든 권한
    POWER_USER = "power_user" # 파워유저: 데이터 조회/수정
    USER = "user"             # 일반유저: 기본 조회만


class Member(Base):
    """팀원 정보 테이블"""
    
    __tablename__ = "members"
    
    # 기본 정보
    id = Column(Integer, primary_key=True, index=True, comment="팀원 고유 ID")
    name = Column(String(50), nullable=False, comment="이름")
    email = Column(String(100), unique=True, nullable=False, index=True, comment="이메일")
    phone = Column(String(20), comment="전화번호")
    
    # 인증 정보
    password_hash = Column(String(255), comment="비밀번호 해시")
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False, comment="사용자 권한")
    last_login = Column(DateTime, comment="마지막 로그인 시간")
    mfa_enabled = Column(Boolean, default=False, comment="MFA 활성화 여부")
    mfa_secret = Column(String(100), comment="MFA 시크릿 키")
    
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
        role_hierarchy = {
            UserRole.USER: 0,
            UserRole.POWER_USER: 1,
            UserRole.ADMIN: 2
        }
        return role_hierarchy.get(self.role, 0) >= role_hierarchy.get(required_role, 0)
    
    def is_admin(self) -> bool:
        """관리자 권한 확인"""
        return self.role == UserRole.ADMIN
    
    def is_power_user_or_above(self) -> bool:
        """파워유저 이상 권한 확인"""
        return self.role in [UserRole.POWER_USER, UserRole.ADMIN] 