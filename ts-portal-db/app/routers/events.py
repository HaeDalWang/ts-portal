"""
이벤트 관련 API 라우터
"""

from typing import List, Optional
from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.event_service import EventService
from ..schemas.event import (
    EventCreate,
    EventUpdate,
    EventResponse,
    EventListResponse,
    EventStats,
    CalendarEventResponse,
    EVENT_TYPE_CHOICES
)

# 라우터 생성
router = APIRouter(
    prefix="/events",
    tags=["events"],
    responses={404: {"description": "이벤트를 찾을 수 없습니다"}}
)


def get_event_service(db: Session = Depends(get_db)) -> EventService:
    """이벤트 서비스 의존성 주입"""
    return EventService(db)


@router.get("/", response_model=EventListResponse, summary="이벤트 목록 조회")
async def get_events(
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
    limit: int = Query(100, ge=1, le=1000, description="조회할 개수"),
    member_id: Optional[int] = Query(None, description="팀원 ID로 필터링"),
    event_type: Optional[str] = Query(None, description="이벤트 타입으로 필터링"),
    start_date: Optional[date] = Query(None, description="시작 날짜 필터"),
    end_date: Optional[date] = Query(None, description="종료 날짜 필터"),
    service: EventService = Depends(get_event_service)
):
    """이벤트 목록을 조회합니다."""
    events = service.get_events(
        skip=skip,
        limit=limit,
        member_id=member_id,
        event_type=event_type,
        start_date=start_date,
        end_date=end_date
    )
    
    total = len(events)  # 실제로는 count 쿼리 필요
    
    # Event 객체를 딕셔너리로 변환하여 직렬화 문제 해결
    result_events = []
    for event in events:
        event_dict = {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "event_type": event.event_type,
            "start_time": event.start_time.isoformat(),
            "end_time": event.end_time.isoformat() if event.end_time else None,
            "all_day": event.all_day,
            "location": event.location,
            "participants": event.participants,
            "created_by": event.created_by,
            "created_at": event.created_at.isoformat(),
            "updated_at": event.updated_at.isoformat(),
            "event_type_display": event.event_type_display,
            "event_type_icon": event.event_type_icon,
            "default_color": event.default_color,
            "duration_minutes": event.duration_minutes,
            "is_today": event.is_today,
            "is_upcoming": event.is_upcoming,
            "is_ongoing": event.is_ongoing,
            "status": event.status,
            "creator": {
                "id": event.creator.id,
                "name": event.creator.name,
                "email": event.creator.email
            } if event.creator else None
        }
        result_events.append(event_dict)
    
    return EventListResponse(total=total, events=result_events)


@router.get("/calendar", response_model=List[CalendarEventResponse], summary="달력용 이벤트 조회")
async def get_calendar_events(
    start: date = Query(..., description="달력 시작 날짜"),
    end: date = Query(..., description="달력 종료 날짜"),
    member_id: Optional[int] = Query(None, description="특정 팀원의 이벤트만 조회"),
    service: EventService = Depends(get_event_service)
):
    """달력 표시용 이벤트 목록을 조회합니다 (FullCalendar 형식)."""
    return service.get_events_for_calendar(start, end, member_id)


@router.get("/today", summary="오늘 일정 조회")
async def get_today_events(
    service: EventService = Depends(get_event_service)
):
    """오늘의 일정을 조회합니다."""
    events = service.get_today_events()
    
    # Event 객체를 딕셔너리로 변환하여 직렬화 문제 해결
    result = []
    for event in events:
        event_dict = {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "event_type": event.event_type,
            "start_time": event.start_time.isoformat(),
            "end_time": event.end_time.isoformat() if event.end_time else None,
            "all_day": event.all_day,
            "location": event.location,
            "participants": event.participants,
            "created_by": event.created_by,
            "created_at": event.created_at.isoformat(),
            "updated_at": event.updated_at.isoformat(),
            "event_type_display": event.event_type_display,
            "event_type_icon": event.event_type_icon,
            "default_color": event.default_color,
            "duration_minutes": event.duration_minutes,
            "is_today": event.is_today,
            "is_upcoming": event.is_upcoming,
            "is_ongoing": event.is_ongoing,
            "status": event.status,
            "creator": {
                "id": event.creator.id,
                "name": event.creator.name,
                "email": event.creator.email
            } if event.creator else None
        }
        result.append(event_dict)
    
    return result


@router.get("/upcoming", response_model=List[EventResponse], summary="다가오는 일정 조회")
async def get_upcoming_events(
    days: int = Query(7, ge=1, le=30, description="몇 일 후까지 조회할지"),
    service: EventService = Depends(get_event_service)
):
    """다가오는 일정을 조회합니다."""
    return service.get_upcoming_events(days)


@router.get("/search", response_model=List[EventResponse], summary="이벤트 검색")
async def search_events(
    q: str = Query(..., min_length=1, description="검색어"),
    service: EventService = Depends(get_event_service)
):
    """제목, 설명, 장소로 이벤트를 검색합니다."""
    return service.search_events(q)


@router.get("/stats/summary", response_model=EventStats, summary="이벤트 통계")
async def get_event_stats(
    service: EventService = Depends(get_event_service)
):
    """이벤트 관련 통계를 조회합니다."""
    return service.get_event_stats()


@router.get("/types", response_model=List[dict], summary="이벤트 타입 목록")
async def get_event_types():
    """사용 가능한 이벤트 타입 목록을 조회합니다."""
    from ..schemas.event import EVENT_TYPES
    return [{"value": value, "label": label} for value, label in EVENT_TYPES]


@router.get("/{event_id}", response_model=EventResponse, summary="이벤트 단일 조회")
async def get_event(
    event_id: int,
    service: EventService = Depends(get_event_service)
):
    """특정 이벤트의 상세 정보를 조회합니다."""
    event = service.get_event(event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"이벤트 ID {event_id}를 찾을 수 없습니다."
        )
    return event


@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED, summary="이벤트 생성")
async def create_event(
    event_data: EventCreate,
    service: EventService = Depends(get_event_service)
):
    """새로운 이벤트를 생성합니다."""
    # 이벤트 타입 유효성 검사
    if event_data.event_type not in EVENT_TYPE_CHOICES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"유효하지 않은 이벤트 타입입니다. 사용 가능한 타입: {EVENT_TYPE_CHOICES}"
        )
    
    return service.create_event(event_data)


@router.put("/{event_id}", response_model=EventResponse, summary="이벤트 수정")
async def update_event(
    event_id: int,
    event_data: EventUpdate,
    service: EventService = Depends(get_event_service)
):
    """기존 이벤트를 수정합니다."""
    # 이벤트 타입 유효성 검사
    if event_data.event_type and event_data.event_type not in EVENT_TYPE_CHOICES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"유효하지 않은 이벤트 타입입니다. 사용 가능한 타입: {EVENT_TYPE_CHOICES}"
        )
    
    event = service.update_event(event_id, event_data)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"이벤트 ID {event_id}를 찾을 수 없습니다."
        )
    return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT, summary="이벤트 삭제")
async def delete_event(
    event_id: int,
    service: EventService = Depends(get_event_service)
):
    """이벤트를 삭제합니다."""
    success = service.delete_event(event_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"이벤트 ID {event_id}를 찾을 수 없습니다."
        )


# 추가 유틸리티 엔드포인트들

@router.get("/member/{member_id}/events", response_model=List[EventResponse], summary="특정 팀원의 이벤트 조회")
async def get_member_events(
    member_id: int,
    start_date: Optional[date] = Query(None, description="시작 날짜"),
    end_date: Optional[date] = Query(None, description="종료 날짜"),
    event_type: Optional[str] = Query(None, description="이벤트 타입"),
    service: EventService = Depends(get_event_service)
):
    """특정 팀원의 이벤트 목록을 조회합니다."""
    return service.get_events(
        member_id=member_id,
        start_date=start_date,
        end_date=end_date,
        event_type=event_type,
        limit=1000
    )


@router.get("/type/{event_type}/events", response_model=List[EventResponse], summary="타입별 이벤트 조회")
async def get_events_by_type(
    event_type: str,
    start_date: Optional[date] = Query(None, description="시작 날짜"),
    end_date: Optional[date] = Query(None, description="종료 날짜"),
    service: EventService = Depends(get_event_service)
):
    """특정 타입의 이벤트 목록을 조회합니다."""
    if event_type not in EVENT_TYPE_CHOICES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"유효하지 않은 이벤트 타입입니다. 사용 가능한 타입: {EVENT_TYPE_CHOICES}"
        )
    
    return service.get_events(
        event_type=event_type,
        start_date=start_date,
        end_date=end_date,
        limit=1000
    ) 