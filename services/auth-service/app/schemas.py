"""
Auth Service - Pydantic 스키마

인증/인가 API 요청/응답 데이터 검증 및 직렬화
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from .models import UserRole


# 로그인 요청
class LoginRequest(BaseModel):
    """로그인 요청 스키마"""
    username: str = Field(..., min_length=1, max_length=50, description="로그인 ID")
    password: str = Field(..., min_length=1, description="비밀번호")


# 토큰 응답
class TokenResponse(BaseModel):
    """토큰 응답 스키마"""
    access_token: str = Field(..., description="JWT 액세스 토큰")
    token_type: str = Field(default="bearer", description="토큰 타입")
    expires_in: int = Field(..., description="토큰 만료 시간 (초)")
    user: dict = Field(..., description="사용자 정보")


# 토큰 검증 요청
class TokenVerifyRequest(BaseModel):
    """토큰 검증 요청 스키마"""
    token: str = Field(..., description="검증할 JWT 토큰")


# 토큰 검증 응답
class TokenVerifyResponse(BaseModel):
    """토큰 검증 응답 스키마"""
    valid: bool = Field(..., description="토큰 유효성")
    user_id: Optional[int] = Field(None, description="사용자 ID")
    user_role: Optional[UserRole] = Field(None, description="사용자 권한")
    expires_at: Optional[datetime] = Field(None, description="토큰 만료 시간")
    message: Optional[str] = Field(None, description="상태 메시지")


# 현재 사용자 정보 응답
class CurrentUserResponse(BaseModel):
    """현재 사용자 정보 응답 스키마"""
    id: int = Field(..., description="사용자 ID")
    name: str = Field(..., description="이름")
    email: str = Field(..., description="이메일")
    role: UserRole = Field(..., description="사용자 권한")
    position: Optional[str] = Field(None, description="직급/직책")
    team: str = Field(..., description="소속팀")
    is_active: bool = Field(..., description="재직 여부")
    last_login: Optional[datetime] = Field(None, description="마지막 로그인")


# 토큰 갱신 요청
class TokenRefreshRequest(BaseModel):
    """토큰 갱신 요청 스키마"""
    refresh_token: str = Field(..., description="리프레시 토큰")


# 로그아웃 요청
class LogoutRequest(BaseModel):
    """로그아웃 요청 스키마"""
    token: str = Field(..., description="로그아웃할 토큰")


# JWT 페이로드 (내부 사용)
class JWTPayload(BaseModel):
    """JWT 페이로드 스키마"""
    user_id: int = Field(..., description="사용자 ID")
    email: str = Field(..., description="이메일")
    role: UserRole = Field(..., description="사용자 권한")
    exp: int = Field(..., description="만료 시간 (Unix timestamp)")
    iat: int = Field(..., description="발급 시간 (Unix timestamp)")


# 에러 응답
class ErrorResponse(BaseModel):
    """에러 응답 스키마"""
    detail: str = Field(..., description="에러 메시지")
    error_code: Optional[str] = Field(None, description="에러 코드")


# 성공 응답 (간단한 메시지)
class SuccessResponse(BaseModel):
    """성공 응답 스키마"""
    message: str = Field(..., description="성공 메시지")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="응답 시간") 