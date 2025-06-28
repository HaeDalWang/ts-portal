"""
Member Service - API 라우터

팀원 관리 REST API 엔드포인트 정의
"""

import logging
import math
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Header, Query
from sqlalchemy.orm import Session

from .database import get_db
from .service import MemberService
from .models import UserRole
from .schemas import (
    MemberCreate, MemberUpdate, MemberResponse, MemberListResponse,
    MemberListPaginated, PasswordChange, RoleChange, MemberFilter,
    SkillsResponse, MemberStats
)

logger = logging.getLogger(__name__)

# 라우터 생성
member_router = APIRouter()


def get_current_user_id(x_user_id: Optional[str] = Header(None)) -> Optional[int]:
    """현재 사용자 ID 추출 (API Gateway에서 전달)"""
    if x_user_id:
        try:
            return int(x_user_id)
        except ValueError:
            return None
    return None


def get_current_user_role(x_user_role: Optional[str] = Header(None)) -> Optional[UserRole]:
    """현재 사용자 권한 추출 (API Gateway에서 전달)"""
    if x_user_role:
        try:
            return UserRole(x_user_role)
        except ValueError:
            return UserRole.USER
    return UserRole.USER


def require_admin(user_role: UserRole = Depends(get_current_user_role)):
    """관리자 권한 필요 (의존성)"""
    if user_role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="관리자 권한이 필요합니다."
        )


def require_power_user_or_above(user_role: UserRole = Depends(get_current_user_role)):
    """파워유저 이상 권한 필요 (의존성)"""
    if user_role not in [UserRole.POWER_USER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="파워유저 이상 권한이 필요합니다."
        )


@member_router.post("/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
async def create_member(
    member_data: MemberCreate,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin)  # 관리자만 멤버 생성 가능
):
    """
    새 멤버 생성
    
    - **관리자 권한 필요**
    - 이메일 중복 확인 후 생성
    """
    service = MemberService(db)
    return service.create_member(member_data)


@member_router.get("/", response_model=MemberListPaginated)
async def get_members(
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(20, ge=1, le=100, description="페이지 크기"),
    name: Optional[str] = Query(None, description="이름 검색"),
    email: Optional[str] = Query(None, description="이메일 검색"),
    team: Optional[str] = Query(None, description="팀별 필터"),
    position: Optional[str] = Query(None, description="직급별 필터"),
    role: Optional[UserRole] = Query(None, description="권한별 필터"),
    is_active: Optional[bool] = Query(None, description="재직 여부 필터"),
    skills: Optional[str] = Query(None, description="기술별 검색"),
    db: Session = Depends(get_db),
    _: None = Depends(require_power_user_or_above)  # 파워유저 이상만 목록 조회
):
    """
    멤버 목록 조회 (페이지네이션 및 필터링)
    
    - **파워유저 이상 권한 필요**
    - 다양한 필터 옵션 제공
    """
    service = MemberService(db)
    
    # 필터 객체 생성
    filters = MemberFilter(
        name=name,
        email=email,
        team=team,
        position=position,
        role=role,
        is_active=is_active,
        skills=skills
    )
    
    # 페이지네이션 계산
    skip = (page - 1) * size
    
    members, total = service.get_members(skip=skip, limit=size, filters=filters)
    
    # 응답 데이터 변환
    items = [MemberListResponse.from_orm(member) for member in members]
    pages = math.ceil(total / size) if total > 0 else 1
    
    return MemberListPaginated(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@member_router.get("/{member_id}", response_model=MemberResponse)
async def get_member(
    member_id: int,
    db: Session = Depends(get_db),
    current_user_id: Optional[int] = Depends(get_current_user_id),
    current_user_role: UserRole = Depends(get_current_user_role)
):
    """
    멤버 상세 정보 조회
    
    - 본인 정보는 누구나 조회 가능
    - 다른 사람 정보는 파워유저 이상만 조회 가능
    """
    service = MemberService(db)
    member = service.get_member_by_id(member_id)
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="멤버를 찾을 수 없습니다."
        )
    
    # 권한 확인: 본인 또는 파워유저 이상
    if member_id != current_user_id and current_user_role == UserRole.USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="본인 정보만 조회할 수 있습니다."
        )
    
    return MemberResponse.from_orm(member)


@member_router.put("/{member_id}", response_model=MemberResponse)
async def update_member(
    member_id: int,
    member_data: MemberUpdate,
    db: Session = Depends(get_db),
    current_user_id: Optional[int] = Depends(get_current_user_id),
    current_user_role: UserRole = Depends(get_current_user_role)
):
    """
    멤버 정보 업데이트
    
    - 본인 정보는 누구나 수정 가능 (일부 필드 제한)
    - 다른 사람 정보는 관리자만 수정 가능
    """
    service = MemberService(db)
    
    # 권한 확인
    if member_id != current_user_id and current_user_role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="본인 정보만 수정할 수 있습니다."
        )
    
    updated_member = service.update_member(member_id, member_data)
    
    if not updated_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="멤버를 찾을 수 없습니다."
        )
    
    return MemberResponse.from_orm(updated_member)


@member_router.post("/{member_id}/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    member_id: int,
    password_data: PasswordChange,
    db: Session = Depends(get_db),
    current_user_id: Optional[int] = Depends(get_current_user_id)
):
    """
    비밀번호 변경
    
    - 본인만 비밀번호 변경 가능
    """
    # 본인 확인
    if member_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="본인 비밀번호만 변경할 수 있습니다."
        )
    
    service = MemberService(db)
    success = service.change_password(member_id, password_data)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="멤버를 찾을 수 없습니다."
        )
    
    return {"message": "비밀번호가 성공적으로 변경되었습니다."}


@member_router.post("/{member_id}/change-role", response_model=MemberResponse)
async def change_member_role(
    member_id: int,
    role_data: RoleChange,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin)  # 관리자만 권한 변경 가능
):
    """
    멤버 권한 변경
    
    - **관리자 권한 필요**
    """
    service = MemberService(db)
    updated_member = service.change_role(member_id, role_data)
    
    if not updated_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="멤버를 찾을 수 없습니다."
        )
    
    return MemberResponse.from_orm(updated_member)


@member_router.delete("/{member_id}", status_code=status.HTTP_200_OK)
async def delete_member(
    member_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin)  # 관리자만 삭제 가능
):
    """
    멤버 삭제 (비활성화)
    
    - **관리자 권한 필요**
    - 실제 삭제가 아닌 비활성화 처리
    """
    service = MemberService(db)
    success = service.delete_member(member_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="멤버를 찾을 수 없습니다."
        )
    
    return {"message": "멤버가 성공적으로 비활성화되었습니다."}


@member_router.post("/{member_id}/login", status_code=status.HTTP_200_OK)
async def update_last_login(
    member_id: int,
    db: Session = Depends(get_db)
):
    """
    마지막 로그인 시간 업데이트
    
    - 인증 서비스에서 호출하는 내부 API
    """
    service = MemberService(db)
    success = service.update_last_login(member_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="멤버를 찾을 수 없습니다."
        )
    
    return {"message": "로그인 시간이 업데이트되었습니다."}


@member_router.get("/skills/all", response_model=SkillsResponse)
async def get_all_skills(
    db: Session = Depends(get_db),
    _: None = Depends(require_power_user_or_above)  # 파워유저 이상만 조회
):
    """
    모든 기술 목록 조회
    
    - **파워유저 이상 권한 필요**
    - 팀원들이 등록한 모든 기술의 유니크 리스트
    """
    service = MemberService(db)
    skills = service.get_all_skills()
    
    return SkillsResponse(skills=skills)


@member_router.get("/stats/overview", response_model=MemberStats)
async def get_member_statistics(
    db: Session = Depends(get_db),
    _: None = Depends(require_power_user_or_above)  # 파워유저 이상만 조회
):
    """
    멤버 통계 조회
    
    - **파워유저 이상 권한 필요**
    - 팀별, 권한별, 직급별 통계 제공
    """
    service = MemberService(db)
    return service.get_member_stats() 