"""
팀원 관련 Pydantic 스키마
"""

from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


class MemberBase(BaseModel):
    """팀원 기본 스키마"""
    name: str = Field(..., min_length=1, max_length=50, description="이름")
    email: str = Field(..., description="이메일")
    phone: Optional[str] = Field(None, max_length=20, description="전화번호")
    position: Optional[str] = Field(None, max_length=50, description="직급/직책")
    team: str = Field(default="TS팀", max_length=50, description="소속팀")
    skills: Optional[str] = Field(None, description="보유 기술 (쉼표로 구분)")
    join_date: Optional[date] = Field(None, description="입사일")
    profile_image: Optional[str] = Field(None, max_length=200, description="프로필 사진 URL")


class MemberCreate(MemberBase):
    """팀원 생성 스키마"""
    is_active: bool = Field(default=True, description="재직 여부")


class MemberUpdate(BaseModel):
    """팀원 수정 스키마"""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="이름")
    email: Optional[str] = Field(None, description="이메일")
    phone: Optional[str] = Field(None, max_length=20, description="전화번호")
    position: Optional[str] = Field(None, max_length=50, description="직급/직책")
    team: Optional[str] = Field(None, max_length=50, description="소속팀")
    skills: Optional[str] = Field(None, description="보유 기술 (쉼표로 구분)")
    join_date: Optional[date] = Field(None, description="입사일")
    profile_image: Optional[str] = Field(None, max_length=200, description="프로필 사진 URL")
    is_active: Optional[bool] = Field(None, description="재직 여부")


class MemberResponse(MemberBase):
    """팀원 응답 스키마"""
    id: int
    is_active: bool
    skills_list: List[str] = Field(description="기술 목록")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_with_skills(cls, member):
        """ORM 객체에서 skills_list 포함하여 변환"""
        data = {
            "id": member.id,
            "name": member.name,
            "email": member.email,
            "phone": member.phone,
            "position": member.position,
            "team": member.team,
            "skills": member.skills,
            "join_date": member.join_date,
            "profile_image": member.profile_image,
            "is_active": member.is_active,
            "skills_list": member.skills_list,
            "created_at": member.created_at,
            "updated_at": member.updated_at
        }
        return cls(**data)


class MemberListResponse(BaseModel):
    """팀원 목록 응답 스키마"""
    total: int
    members: List[MemberResponse] 