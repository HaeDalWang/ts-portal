"""
인증 관련 스키마
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class LoginRequest(BaseModel):
    """로그인 요청 스키마"""
    email: EmailStr = Field(..., description="이메일")
    password: str = Field(..., min_length=6, description="비밀번호")


class LoginResponse(BaseModel):
    """로그인 응답 스키마"""
    access_token: str = Field(..., description="액세스 토큰")
    token_type: str = Field(default="bearer", description="토큰 타입")
    user: dict = Field(..., description="사용자 정보")


class PasswordResetRequest(BaseModel):
    """비밀번호 재설정 요청 스키마"""
    password: str = Field(..., min_length=6, max_length=100, description="새 비밀번호")


class PasswordChangeRequest(BaseModel):
    """비밀번호 변경 요청 스키마"""
    current_password: str = Field(..., description="현재 비밀번호")
    new_password: str = Field(..., min_length=6, max_length=100, description="새 비밀번호")


class TokenData(BaseModel):
    """토큰 데이터 스키마"""
    email: Optional[str] = None
    user_id: Optional[int] = None


class UserResponse(BaseModel):
    """사용자 응답 스키마"""
    id: int
    name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class CurrentUser(BaseModel):
    """현재 사용자 정보 스키마"""
    id: int
    name: str
    email: str
    role: str
    team: str
    position: Optional[str] = None
    is_active: bool 