"""
Notice Service API 라우터
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Header, status
from sqlalchemy.orm import Session

from .database import get_db
from .service import NoticeService
from .schemas import (
    NoticeCreate,
    NoticeCreateInternal,
    NoticeUpdate,
    NoticeResponse,
    NoticeListResponse,
    NoticeStats,
    SearchParams,
    PaginationParams,
    NoticePriorityEnum
)

router = APIRouter(prefix="/notices", tags=["notices"])

def get_notice_service(db: Session = Depends(get_db)) -> NoticeService:
    """공지사항 서비스 의존성"""
    return NoticeService(db)

def get_current_user_id(x_user_id: int = Header(..., alias="X-User-ID")) -> int:
    """API Gateway에서 전달된 사용자 ID 추출"""
    return x_user_id

def get_current_user_role(x_user_role: str = Header(..., alias="X-User-Role")) -> str:
    """API Gateway에서 전달된 사용자 역할 추출"""
    return x_user_role

def can_create_priority_notice(priority: str, user_role: str) -> bool:
    """중요도별 생성 권한 체크"""
    if priority == "important":  # 긴급: admin만
        return user_role.lower() == "admin"
    elif priority == "caution":  # 경고: power_user 이상
        return user_role.lower() in ["admin", "power_user"]
    return True  # normal: 누구나 가능

def can_delete_priority_notice(priority: str, user_role: str, author_id: int, current_user_id: int) -> bool:
    """중요도별 삭제 권한 체크"""
    if priority == "important":  # 긴급: admin만
        return user_role.lower() == "admin"
    elif priority == "caution":  # 경고: power_user 이상
        return user_role.lower() in ["admin", "power_user"]
    else:  # normal: 누구나 가능
        return True

@router.post("/", response_model=NoticeResponse, summary="공지사항 생성")
async def create_notice(
    notice_data: NoticeCreateInternal,
    service: NoticeService = Depends(get_notice_service),
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: str = Depends(get_current_user_role)
):
    """
    새로운 공지사항을 생성합니다.
    
    권한별 생성 가능 범위:
    - 관리자/파워유저: 모든 우선순위 공지사항 생성 가능
    - 일반유저: 일반 우선순위만 생성 가능
    """
    # 권한 체크
    if not can_create_priority_notice(notice_data.priority.value, current_user_role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"'{notice_data.priority.value}' 우선순위 공지사항을 생성할 권한이 없습니다."
        )
    
    # NoticeCreate 스키마로 변환 (author_id 추가)
    create_data = NoticeCreate(
        title=notice_data.title,
        content=notice_data.content,
        priority=notice_data.priority,
        is_pinned=notice_data.is_pinned,
        author_id=current_user_id
    )
    
    try:
        return service.create_notice(create_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"공지사항 생성 중 오류가 발생했습니다: {str(e)}")

@router.get("/", response_model=NoticeListResponse, summary="공지사항 목록 조회")
async def get_notices(
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
    limit: int = Query(20, ge=1, le=100, description="가져올 개수"),
    service: NoticeService = Depends(get_notice_service)
):
    """공지사항 목록을 조회합니다. 고정 공지사항이 먼저 표시됩니다."""
    pagination = PaginationParams(skip=skip, limit=limit)
    return service.get_notices(pagination)

@router.get("/search", response_model=NoticeListResponse, summary="공지사항 검색")
async def search_notices(
    q: str = Query(None, description="검색 키워드"),
    priority: NoticePriorityEnum = Query(None, description="중요도 필터"),
    author_id: int = Query(None, description="작성자 ID 필터"),
    is_pinned: bool = Query(None, description="고정 공지사항만"),
    active_only: bool = Query(True, description="활성 공지사항만"),
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
    limit: int = Query(20, ge=1, le=100, description="가져올 개수"),
    service: NoticeService = Depends(get_notice_service)
):
    """공지사항을 검색합니다."""
    search_params = SearchParams(
        q=q,
        priority=priority,
        author_id=author_id,
        is_pinned=is_pinned,
        active_only=active_only
    )
    pagination = PaginationParams(skip=skip, limit=limit)
    return service.search_notices(search_params, pagination)

@router.get("/pinned", response_model=List[NoticeResponse], summary="고정 공지사항 조회")
async def get_pinned_notices(
    service: NoticeService = Depends(get_notice_service)
):
    """고정된 공지사항들을 조회합니다."""
    return service.get_pinned_notices()

@router.get("/recent", response_model=List[NoticeResponse], summary="최근 공지사항 조회")
async def get_recent_notices(
    days: int = Query(7, ge=1, le=30, description="최근 며칠간의 공지사항"),
    limit: int = Query(5, ge=1, le=20, description="최대 개수"),
    service: NoticeService = Depends(get_notice_service)
):
    """최근 공지사항들을 조회합니다."""
    return service.get_recent_notices(days=days, limit=limit)

@router.get("/stats", response_model=NoticeStats, summary="공지사항 통계")
async def get_notice_stats(
    service: NoticeService = Depends(get_notice_service)
):
    """공지사항 통계 정보를 조회합니다."""
    return service.get_notice_stats()

@router.get("/author/{author_id}", response_model=NoticeListResponse, summary="작성자별 공지사항 조회")
async def get_notices_by_author(
    author_id: int,
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
    limit: int = Query(20, ge=1, le=100, description="가져올 개수"),
    service: NoticeService = Depends(get_notice_service)
):
    """특정 작성자의 공지사항들을 조회합니다."""
    pagination = PaginationParams(skip=skip, limit=limit)
    return service.get_notices_by_author(author_id, pagination)

@router.get("/{notice_id}", response_model=NoticeResponse, summary="공지사항 단일 조회")
async def get_notice(
    notice_id: int,
    service: NoticeService = Depends(get_notice_service)
):
    """특정 공지사항을 조회합니다."""
    notice = service.get_notice(notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="공지사항을 찾을 수 없습니다.")
    return notice

@router.put("/{notice_id}", response_model=NoticeResponse, summary="공지사항 수정")
async def update_notice(
    notice_id: int,
    notice_data: NoticeUpdate,
    service: NoticeService = Depends(get_notice_service),
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: str = Depends(get_current_user_role)
):
    """공지사항을 수정합니다."""
    # 기존 공지사항 확인
    existing_notice = service.get_notice(notice_id)
    if not existing_notice:
        raise HTTPException(status_code=404, detail="공지사항을 찾을 수 없습니다.")
    
    # 권한 체크 (작성자 본인 또는 관리자만)
    if existing_notice.author_id != current_user_id and current_user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="공지사항을 수정할 권한이 없습니다."
        )
    
    # 중요도 변경 권한 체크
    if notice_data.priority and not can_create_priority_notice(notice_data.priority.value, current_user_role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"'{notice_data.priority.value}' 우선순위로 변경할 권한이 없습니다."
        )
    
    try:
        notice = service.update_notice(notice_id, notice_data)
        if not notice:
            raise HTTPException(status_code=404, detail="공지사항을 찾을 수 없습니다.")
        return notice
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"공지사항 수정 중 오류가 발생했습니다: {str(e)}")

@router.delete("/{notice_id}", summary="공지사항 삭제")
async def delete_notice(
    notice_id: int,
    service: NoticeService = Depends(get_notice_service),
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: str = Depends(get_current_user_role)
):
    """공지사항을 삭제합니다 (소프트 삭제)."""
    # 기존 공지사항 확인
    existing_notice = service.get_notice(notice_id)
    if not existing_notice:
        raise HTTPException(status_code=404, detail="공지사항을 찾을 수 없습니다.")
    
    # 중요도별 삭제 권한 체크
    if not can_delete_priority_notice(existing_notice.priority.value, current_user_role, existing_notice.author_id, current_user_id):
        priority_names = {"normal": "일반", "caution": "경고", "important": "긴급"}
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"'{priority_names.get(existing_notice.priority.value, existing_notice.priority.value)}' 공지사항을 삭제할 권한이 없습니다."
        )
    
    try:
        success = service.delete_notice(notice_id)
        if not success:
            raise HTTPException(status_code=404, detail="공지사항을 찾을 수 없습니다.")
        return {"message": "공지사항이 성공적으로 삭제되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"공지사항 삭제 중 오류가 발생했습니다: {str(e)}")

@router.get("/priorities/list", summary="중요도 목록 조회")
async def get_priority_list():
    """공지사항 중요도 목록을 조회합니다."""
    return [
        {"value": "normal", "label": "일반", "icon": "📢", "color": "#6B7280", "description": "누구나 생성/삭제 가능"},
        {"value": "caution", "label": "Warning", "icon": "⚠️", "color": "#F59E0B", "description": "Power User 이상"},
        {"value": "important", "label": "긴급", "icon": "🚨", "color": "#EF4444", "description": "Admin만 가능"}
    ]

# 라우터를 notices_router로 export
notices_router = router 