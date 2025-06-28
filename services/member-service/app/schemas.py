"""
Member Service - Pydantic 스키마

API 요청/응답 데이터 검증 및 직렬화
"""

from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, validator

from .models import UserRole


# 기본 멤버 정보 (공통)
class MemberBase(BaseModel):
    """멤버 기본 정보"""
    name: str = Field(..., max_length=50, description="이름")
    email: EmailStr = Field(..., description="이메일")
    phone: Optional[str] = Field(None, max_length=20, description="전화번호")
    position: Optional[str] = Field(None, max_length=50, description="직급/직책")
    team: str = Field(default="TS팀", max_length=50, description="소속팀")
    skills: Optional[str] = Field(None, description="보유 기술 (쉼표로 구분)")
    join_date: Optional[date] = Field(None, description="입사일")
    profile_image: Optional[str] = Field(None, max_length=200, description="프로필 사진 URL")


# 멤버 생성 요청
class MemberCreate(MemberBase):
    """멤버 생성 요청 스키마"""
    password: str = Field(..., min_length=8, description="비밀번호 (최소 8자)")
    role: UserRole = Field(default=UserRole.USER, description="사용자 권한")
    is_active: bool = Field(default=True, description="재직 여부")
    
    @validator('skills')
    def validate_skills(cls, v):
        """기술 목록 검증"""
        if v and len(v) > 1000:
            raise ValueError('기술 목록이 너무 깁니다 (최대 1000자)')
        return v


# 멤버 업데이트 요청  
class MemberUpdate(BaseModel):
    """멤버 업데이트 요청 스키마"""
    name: Optional[str] = Field(None, max_length=50, description="이름")
    phone: Optional[str] = Field(None, max_length=20, description="전화번호")
    position: Optional[str] = Field(None, max_length=50, description="직급/직책")
    team: Optional[str] = Field(None, max_length=50, description="소속팀")
    skills: Optional[str] = Field(None, description="보유 기술")
    join_date: Optional[date] = Field(None, description="입사일")
    profile_image: Optional[str] = Field(None, max_length=200, description="프로필 사진 URL")
    is_active: Optional[bool] = Field(None, description="재직 여부")


# 비밀번호 변경 요청
class PasswordChange(BaseModel):
    """비밀번호 변경 요청 스키마"""
    current_password: str = Field(..., description="현재 비밀번호")
    new_password: str = Field(..., min_length=8, description="새 비밀번호 (최소 8자)")


# 권한 변경 요청 (관리자만)
class RoleChange(BaseModel):
    """권한 변경 요청 스키마"""
    role: UserRole = Field(..., description="새 권한")


# 멤버 응답 (상세)
class MemberResponse(MemberBase):
    """멤버 상세 응답 스키마"""
    id: int = Field(..., description="멤버 ID")
    role: UserRole = Field(..., description="사용자 권한")
    last_login: Optional[datetime] = Field(None, description="마지막 로그인")
    mfa_enabled: bool = Field(default=False, description="MFA 활성화 여부")
    is_active: bool = Field(..., description="재직 여부")
    created_at: datetime = Field(..., description="생성일시")
    updated_at: datetime = Field(..., description="수정일시")
    
    class Config:
        from_attributes = True


# 멤버 목록 응답 (간략)
class MemberListResponse(BaseModel):
    """멤버 목록 응답 스키마"""
    id: int = Field(..., description="멤버 ID")
    name: str = Field(..., description="이름")
    email: str = Field(..., description="이메일")
    position: Optional[str] = Field(None, description="직급/직책")
    team: str = Field(..., description="소속팀")
    role: UserRole = Field(..., description="사용자 권한")
    is_active: bool = Field(..., description="재직 여부")
    last_login: Optional[datetime] = Field(None, description="마지막 로그인")
    
    class Config:
        from_attributes = True


# 기술 목록 응답
class SkillsResponse(BaseModel):
    """기술 목록 응답 스키마"""
    skills: List[str] = Field(..., description="기술 목록")


# 멤버 검색 필터
class MemberFilter(BaseModel):
    """멤버 검색 필터 스키마"""
    name: Optional[str] = Field(None, description="이름 검색")
    email: Optional[str] = Field(None, description="이메일 검색")
    team: Optional[str] = Field(None, description="팀별 필터")
    position: Optional[str] = Field(None, description="직급별 필터")
    role: Optional[UserRole] = Field(None, description="권한별 필터")
    is_active: Optional[bool] = Field(None, description="재직 여부 필터")
    skills: Optional[str] = Field(None, description="기술별 검색")


# 페이지네이션 응답
class MemberListPaginated(BaseModel):
    """페이지네이션된 멤버 목록 응답"""
    items: List[MemberListResponse] = Field(..., description="멤버 목록")
    total: int = Field(..., description="전체 개수")
    page: int = Field(..., description="현재 페이지")
    size: int = Field(..., description="페이지 크기")
    pages: int = Field(..., description="전체 페이지 수")


# 멤버 통계
class MemberStats(BaseModel):
    """멤버 통계 응답 스키마"""
    total_members: int = Field(..., description="전체 멤버 수")
    active_members: int = Field(..., description="재직 중인 멤버 수")
    inactive_members: int = Field(..., description="퇴사한 멤버 수")
    by_team: dict = Field(..., description="팀별 멤버 수")
    by_role: dict = Field(..., description="권한별 멤버 수")
    by_position: dict = Field(..., description="직급별 멤버 수")
    recent_logins: int = Field(..., description="최근 7일 로그인 수") 