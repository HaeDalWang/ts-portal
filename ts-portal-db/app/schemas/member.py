"""
팀원 관련 Pydantic 스키마
"""

from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, validator

from ..models.member import UserRole


# 기본 스키마
class MemberBase(BaseModel):
    """팀원 기본 정보"""
    name: str = Field(..., min_length=1, max_length=50, description="이름")
    email: EmailStr = Field(..., description="이메일")
    phone: Optional[str] = Field(None, max_length=20, description="전화번호")
    position: Optional[str] = Field(None, max_length=50, description="직급/직책")
    team: str = Field(default="TS팀", max_length=50, description="소속팀")
    skills: Optional[str] = Field(None, description="보유 기술 (쉼표로 구분)")
    join_date: Optional[date] = Field(None, description="입사일")
    profile_image: Optional[str] = Field(None, max_length=200, description="프로필 사진 URL")


# 인증 관련 스키마
class LoginRequest(BaseModel):
    """로그인 요청"""
    email: EmailStr = Field(..., description="이메일")
    password: str = Field(..., min_length=6, description="비밀번호")


class LoginResponse(BaseModel):
    """로그인 응답"""
    access_token: str = Field(..., description="JWT 액세스 토큰")
    token_type: str = Field(default="bearer", description="토큰 타입")
    user: 'MemberResponse' = Field(..., description="사용자 정보")


class PasswordChangeRequest(BaseModel):
    """비밀번호 변경 요청"""
    current_password: str = Field(..., description="현재 비밀번호")
    new_password: str = Field(..., min_length=6, description="새 비밀번호")


class RoleUpdateRequest(BaseModel):
    """권한 변경 요청 (관리자만)"""
    role: UserRole = Field(..., description="새 권한")


# 생성 스키마
class MemberCreate(MemberBase):
    """팀원 생성"""
    password: str = Field(..., min_length=6, description="비밀번호")
    role: UserRole = Field(default=UserRole.USER, description="사용자 권한")


# 수정 스키마
class MemberUpdate(BaseModel):
    """팀원 정보 수정"""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="이름")
    email: Optional[EmailStr] = Field(None, description="이메일")
    phone: Optional[str] = Field(None, max_length=20, description="전화번호")
    position: Optional[str] = Field(None, max_length=50, description="직급/직책")
    team: Optional[str] = Field(None, max_length=50, description="소속팀")
    skills: Optional[str] = Field(None, description="보유 기술")
    join_date: Optional[date] = Field(None, description="입사일")
    profile_image: Optional[str] = Field(None, max_length=200, description="프로필 사진 URL")
    is_active: Optional[bool] = Field(None, description="재직 여부")
    role: Optional[UserRole] = Field(None, description="사용자 권한")


# 응답 스키마
class MemberResponse(BaseModel):
    """팀원 응답"""
    id: int
    name: str
    email: str
    phone: Optional[str]
    position: Optional[str]
    team: str
    skills: Optional[str]
    join_date: Optional[date]
    profile_image: Optional[str]
    is_active: bool
    role: UserRole
    last_login: Optional[datetime]
    mfa_enabled: bool
    created_at: datetime
    updated_at: datetime
    
    # 계산된 필드
    skills_list: List[str] = []
    
    class Config:
        from_attributes = True
    
    @validator('skills_list', always=True)
    def set_skills_list(cls, v, values):
        """skills 문자열을 리스트로 변환"""
        skills = values.get('skills')
        if skills:
            return [skill.strip() for skill in skills.split(",") if skill.strip()]
        return []
    
    @classmethod
    def from_orm_with_skills(cls, obj):
        """ORM 객체에서 skills_list를 포함한 응답 생성"""
        # 기본 from_orm 사용
        instance = cls.from_orm(obj)
        # skills_list는 이미 validator에서 처리됨
        return instance


class MemberListResponse(BaseModel):
    """팀원 목록 응답"""
    total: int = Field(..., description="전체 개수")
    members: List[MemberResponse] = Field(..., description="팀원 목록")


# 현재 사용자 정보 (JWT에서 추출)
class CurrentUser(BaseModel):
    """현재 로그인한 사용자 정보"""
    id: int
    email: str
    name: str
    role: UserRole
    is_active: bool
    
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


# Forward reference 해결
LoginResponse.model_rebuild() 