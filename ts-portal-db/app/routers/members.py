"""
팀원 관련 API 라우터
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.member_service import MemberService
from ..services.auth_service import (
    get_current_user, 
    require_admin,
    can_edit_member,
    can_delete_member,
    get_allowed_member_fields_for_update
)
from ..models.member import Member
from ..schemas.member import (
    MemberCreate,
    MemberUpdate,
    MemberResponse,
    MemberListResponse
)
from ..schemas.auth import PasswordResetRequest
import bcrypt

# 라우터 생성
router = APIRouter(
    prefix="/members",
    tags=["members"],
    responses={404: {"description": "팀원을 찾을 수 없습니다"}}
)


def get_member_service(db: Session = Depends(get_db)) -> MemberService:
    """팀원 서비스 의존성 주입"""
    return MemberService(db)


@router.get("/", response_model=MemberListResponse, summary="팀원 목록 조회")
async def get_members(
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
    limit: int = Query(100, ge=1, le=1000, description="가져올 개수"),
    active_only: bool = Query(False, description="재직자만 조회"),
    exclude_admin: bool = Query(True, description="관리자 제외"),
    service: MemberService = Depends(get_member_service)
):
    """
    팀원 목록을 조회합니다.
    
    - **skip**: 건너뛸 개수 (페이징용)
    - **limit**: 가져올 개수 (최대 1000)
    - **active_only**: True면 재직자만, False면 전체 조회
    - **exclude_admin**: True면 관리자 제외, False면 관리자 포함
    """
    members = service.get_members(skip=skip, limit=limit, active_only=active_only, exclude_admin=exclude_admin)
    total = service.get_members_count(active_only=active_only, exclude_admin=exclude_admin)
    
    # 응답 데이터 변환
    member_responses = [
        MemberResponse.from_orm(member) for member in members
    ]
    
    return MemberListResponse(total=total, members=member_responses)


@router.get("/search", response_model=List[MemberResponse], summary="팀원 검색")
async def search_members(
    q: str = Query(..., min_length=1, description="검색어 (이름, 이메일, 직급)"),
    active_only: bool = Query(False, description="재직자만 검색"),
    exclude_admin: bool = Query(True, description="관리자 제외"),
    service: MemberService = Depends(get_member_service)
):
    """
    팀원을 검색합니다.
    
    - **q**: 검색어 (이름, 이메일, 직급에서 검색)
    - **active_only**: True면 재직자만, False면 전체에서 검색
    - **exclude_admin**: True면 관리자 제외, False면 관리자 포함
    """
    members = service.search_members(query=q, active_only=active_only, exclude_admin=exclude_admin)
    
    return [MemberResponse.from_orm(member) for member in members]


@router.get("/{member_id}", response_model=MemberResponse, summary="팀원 단일 조회")
async def get_member(
    member_id: int,
    service: MemberService = Depends(get_member_service)
):
    """
    특정 팀원의 상세 정보를 조회합니다.
    
    - **member_id**: 팀원 ID
    """
    member = service.get_member(member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {member_id}인 팀원을 찾을 수 없습니다."
        )
    
    return MemberResponse.from_orm(member)


@router.post("/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED, summary="팀원 생성 (관리자 전용)")
async def create_member(
    member_data: MemberCreate,
    service: MemberService = Depends(get_member_service),
    current_user: Member = Depends(get_current_user)
):
    """
    새 팀원을 등록합니다. (관리자 전용)
    
    - **member_data**: 팀원 정보
    """
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="관리자 권한이 필요합니다"
        )
    
    member = service.create_member(member_data)
    return MemberResponse.from_orm(member)


@router.put("/{member_id}", response_model=MemberResponse, summary="팀원 정보 수정")
async def update_member(
    member_id: int,
    member_data: MemberUpdate,
    service: MemberService = Depends(get_member_service),
    current_user: Member = Depends(get_current_user)
):
    """
    팀원 정보를 수정합니다.
    
    권한별 수정 가능 범위:
    - 관리자: 모든 필드 수정 가능
    - 파워유저: 권한 변경 제외하고 모든 필드 수정 가능
    - 일반유저: 자신의 이메일, 전화번호, 기술스택, 프로필 사진만 수정 가능
    
    - **member_id**: 팀원 ID
    - **member_data**: 수정할 팀원 정보
    """
    # 권한 체크
    if not can_edit_member(current_user, member_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="해당 팀원 정보를 수정할 권한이 없습니다"
        )
    
    # 수정 가능한 필드 체크
    allowed_fields = get_allowed_member_fields_for_update(current_user, member_id)
    update_data = member_data.model_dump(exclude_unset=True)
    
    # 허용되지 않은 필드 제거
    filtered_data = {}
    for field, value in update_data.items():
        if field in allowed_fields:
            filtered_data[field] = value
        elif field in update_data:
            # 권한이 없는 필드를 수정하려고 할 때 경고
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"'{field}' 필드를 수정할 권한이 없습니다"
            )
    
    # 자기 자신의 권한을 변경하려고 하는 경우 방지 (관리자도 불가)
    if member_id == current_user.id and 'role' in filtered_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="자신의 권한은 변경할 수 없습니다"
        )
    
    # 필터링된 데이터로 MemberUpdate 객체 재생성
    filtered_member_data = MemberUpdate(**filtered_data)
    
    member = service.update_member(member_id, filtered_member_data)
    return MemberResponse.from_orm(member)


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT, summary="팀원 삭제 (관리자 전용)")
async def delete_member(
    member_id: int,
    service: MemberService = Depends(get_member_service),
    current_user: Member = Depends(get_current_user)
):
    """
    팀원을 삭제합니다. (관리자 전용, 소프트 삭제 - is_active를 False로 변경)
    
    - **member_id**: 팀원 ID
    """
    # 권한 체크
    if not can_delete_member(current_user, member_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="팀원을 삭제할 권한이 없습니다"
        )
    
    service.delete_member(member_id)


@router.patch("/{member_id}/restore", response_model=MemberResponse, summary="팀원 복구")
async def restore_member(
    member_id: int,
    service: MemberService = Depends(get_member_service)
):
    """
    삭제된 팀원을 복구합니다. (is_active를 True로 변경)
    
    - **member_id**: 팀원 ID
    """
    member = service.restore_member(member_id)
    return MemberResponse.from_orm(member)


@router.get("/stats/summary", summary="팀원 통계")
async def get_member_stats(
    exclude_admin: bool = Query(True, description="관리자 제외"),
    service: MemberService = Depends(get_member_service)
):
    """
    팀원 관련 통계를 조회합니다.
    
    - **exclude_admin**: True면 관리자 제외, False면 관리자 포함
    """
    total_members = service.get_members_count(active_only=False, exclude_admin=exclude_admin)
    active_members = service.get_members_count(active_only=True, exclude_admin=exclude_admin)
    inactive_members = total_members - active_members
    
    return {
        "total_members": total_members,
        "active_members": active_members,
        "inactive_members": inactive_members,
        "active_rate": round((active_members / total_members * 100) if total_members > 0 else 0, 2)
    }


@router.post("/{member_id}/reset-password", summary="팀원 비밀번호 초기화 (관리자 전용)")
async def reset_member_password(
    member_id: int,
    password_data: PasswordResetRequest,
    service: MemberService = Depends(get_member_service),
    current_user: Member = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    팀원의 비밀번호를 초기화합니다. (관리자 전용)
    
    - **member_id**: 팀원 ID
    - **password_data**: 새 비밀번호 정보
    """
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="관리자 권한이 필요합니다"
        )
    
    # 팀원 조회
    member = service.get_member(member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {member_id}인 팀원을 찾을 수 없습니다."
        )
    
    try:
        # 새 비밀번호 해시화
        hashed_password = bcrypt.hashpw(
            password_data.password.encode('utf-8'), 
            bcrypt.gensalt()
        ).decode('utf-8')
        
        # 비밀번호 업데이트
        db_member = db.query(Member).filter(Member.id == member_id).first()
        db_member.password_hash = hashed_password
        db.commit()
        
        return {"message": f"{member.name}님의 비밀번호가 성공적으로 초기화되었습니다"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"비밀번호 초기화 중 오류가 발생했습니다: {str(e)}"
        )


@router.post("/{member_id}/toggle-status", summary="팀원 활성/비활성 상태 토글 (관리자 전용)")
async def toggle_member_status(
    member_id: int,
    service: MemberService = Depends(get_member_service),
    current_user: Member = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    팀원의 활성/비활성 상태를 토글합니다. (관리자 전용)
    
    - **member_id**: 팀원 ID
    """
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="관리자 권한이 필요합니다"
        )
    
    # 팀원 조회
    member = service.get_member(member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {member_id}인 팀원을 찾을 수 없습니다."
        )
    
    # 자기 자신의 상태를 변경하려고 하는 경우 방지
    if member_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="자신의 상태는 변경할 수 없습니다"
        )
    
    try:
        # 상태 토글
        db_member = db.query(Member).filter(Member.id == member_id).first()
        db_member.is_active = not db_member.is_active
        db.commit()
        
        status_text = "활성화" if db_member.is_active else "비활성화"
        return {"message": f"{member.name}님이 {status_text}되었습니다"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"상태 변경 중 오류가 발생했습니다: {str(e)}"
        ) 