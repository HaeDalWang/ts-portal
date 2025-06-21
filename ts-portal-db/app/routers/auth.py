"""
인증 관련 API 라우터
로그인, 토큰 검증, 권한 관리 등을 담당
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..database import get_db
from ..services.auth_service import auth_service, get_current_user
from ..models.member import UserRole, Member
from ..schemas.member import (
    LoginRequest,
    LoginResponse,
    CurrentUser,
    MemberResponse
)

# 로깅 설정
logger = logging.getLogger(__name__)

# 라우터 생성
router = APIRouter(prefix="/auth", tags=["인증"])

# HTTP Bearer 토큰 스키마
security = HTTPBearer()


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


@router.post("/login", response_model=LoginResponse, summary="로그인")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    사용자 로그인
    
    - **email**: 이메일 주소
    - **password**: 비밀번호
    
    성공 시 JWT 토큰과 사용자 정보를 반환합니다.
    """
    try:
        result = auth_service.authenticate_user(db, request.email, request.password)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"로그인 실패: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="로그인 처리 중 오류가 발생했습니다."
        )


@router.post("/verify", summary="토큰 검증")
async def verify_token(current_user: Member = Depends(get_current_user)):
    """
    JWT 토큰 검증 및 현재 사용자 정보 반환
    
    Authorization 헤더에 Bearer 토큰을 포함하여 요청해야 합니다.
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "role": current_user.role,
        "team": current_user.team,
        "phone": current_user.phone,
        "position": current_user.position,
        "skills": current_user.skills,
        "join_date": current_user.join_date.isoformat() if current_user.join_date else None,
        "profile_image": current_user.profile_image,
        "is_active": current_user.is_active,
        "last_login": current_user.last_login.isoformat() if current_user.last_login else None,
        "mfa_enabled": current_user.mfa_enabled,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
        "updated_at": current_user.updated_at.isoformat() if current_user.updated_at else None,
        "skills_list": current_user.skills_list
    }


@router.post("/change-password", summary="비밀번호 변경")
async def change_password(
    request: ChangePasswordRequest,
    current_user: Member = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """비밀번호 변경"""
    try:
        # 현재 비밀번호 확인
        if not auth_service.verify_password(request.current_password, current_user.password_hash):
            raise HTTPException(status_code=400, detail="현재 비밀번호가 올바르지 않습니다.")
        
        # 새 비밀번호 길이 확인
        if len(request.new_password) < 6:
            raise HTTPException(status_code=400, detail="새 비밀번호는 최소 6자 이상이어야 합니다.")
        
        # 새 비밀번호 해시화 및 저장
        current_user.password_hash = auth_service.hash_password(request.new_password)
        db.commit()
        
        logger.info(f"사용자 {current_user.email}의 비밀번호가 변경되었습니다.")
        return {"message": "비밀번호가 성공적으로 변경되었습니다."}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"비밀번호 변경 실패: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="비밀번호 변경 중 오류가 발생했습니다.")