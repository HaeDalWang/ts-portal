"""
팀원 관련 API 라우터
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.member_service import MemberService
from ..schemas.member import (
    MemberCreate,
    MemberUpdate,
    MemberResponse,
    MemberListResponse
)

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
    service: MemberService = Depends(get_member_service)
):
    """
    팀원 목록을 조회합니다.
    
    - **skip**: 건너뛸 개수 (페이징용)
    - **limit**: 가져올 개수 (최대 1000)
    - **active_only**: True면 재직자만, False면 전체 조회
    """
    members = service.get_members(skip=skip, limit=limit, active_only=active_only)
    total = service.get_members_count(active_only=active_only)
    
    # 응답 데이터 변환
    member_responses = [
        MemberResponse.from_orm_with_skills(member) for member in members
    ]
    
    return MemberListResponse(total=total, members=member_responses)


@router.get("/search", response_model=List[MemberResponse], summary="팀원 검색")
async def search_members(
    q: str = Query(..., min_length=1, description="검색어 (이름, 이메일, 직급)"),
    active_only: bool = Query(False, description="재직자만 검색"),
    service: MemberService = Depends(get_member_service)
):
    """
    팀원을 검색합니다.
    
    - **q**: 검색어 (이름, 이메일, 직급에서 검색)
    - **active_only**: True면 재직자만, False면 전체에서 검색
    """
    members = service.search_members(query=q, active_only=active_only)
    
    return [MemberResponse.from_orm_with_skills(member) for member in members]


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
    
    return MemberResponse.from_orm_with_skills(member)


@router.post("/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED, summary="팀원 생성")
async def create_member(
    member_data: MemberCreate,
    service: MemberService = Depends(get_member_service)
):
    """
    새 팀원을 등록합니다.
    
    - **member_data**: 팀원 정보
    """
    member = service.create_member(member_data)
    return MemberResponse.from_orm_with_skills(member)


@router.put("/{member_id}", response_model=MemberResponse, summary="팀원 정보 수정")
async def update_member(
    member_id: int,
    member_data: MemberUpdate,
    service: MemberService = Depends(get_member_service)
):
    """
    팀원 정보를 수정합니다.
    
    - **member_id**: 팀원 ID
    - **member_data**: 수정할 팀원 정보
    """
    member = service.update_member(member_id, member_data)
    return MemberResponse.from_orm_with_skills(member)


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT, summary="팀원 삭제")
async def delete_member(
    member_id: int,
    service: MemberService = Depends(get_member_service)
):
    """
    팀원을 삭제합니다. (소프트 삭제 - is_active를 False로 변경)
    
    - **member_id**: 팀원 ID
    """
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
    return MemberResponse.from_orm_with_skills(member)


@router.get("/stats/summary", summary="팀원 통계")
async def get_member_stats(
    service: MemberService = Depends(get_member_service)
):
    """
    팀원 관련 통계를 조회합니다.
    """
    total_members = service.get_members_count(active_only=False)
    active_members = service.get_members_count(active_only=True)
    inactive_members = total_members - active_members
    
    return {
        "total_members": total_members,
        "active_members": active_members,
        "inactive_members": inactive_members,
        "active_rate": round((active_members / total_members * 100) if total_members > 0 else 0, 2)
    } 