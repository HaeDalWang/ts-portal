"""
Calendar Service API 라우터
"""

from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query, Header, status
from sqlalchemy.orm import Session

from .database import get_db
from .service import CalendarService
from .schemas import (
    EventCreateInternal, EventUpdate, EventResponse, EventListResponse,
    EventStats, CalendarEventResponse, SearchParams, PaginationParams,
    EventTypeEnum, EVENT_TYPES, EventCreate
)

router = APIRouter(prefix="/events", tags=["events"])

def get_calendar_service(db: Session = Depends(get_db)) -> CalendarService:
    return CalendarService(db)

def get_current_user_id(x_user_id: int = Header(..., alias="X-User-ID")) -> int:
    return x_user_id

def get_current_user_role(x_user_role: str = Header(..., alias="X-User-Role")) -> str:
    return x_user_role

@router.post("/", response_model=EventResponse, summary="이벤트 생성")
async def create_event(
    event_data: EventCreateInternal,
    service: CalendarService = Depends(get_calendar_service),
    current_user_id: int = Depends(get_current_user_id)
):
    create_data = EventCreate(**event_data.model_dump(), created_by=current_user_id)
    try:
        return service.create_event(create_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=EventListResponse, summary="이벤트 목록 조회")
async def get_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    q: str = Query(None),
    event_type: EventTypeEnum = Query(None),
    member_id: Optional[int] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    service: CalendarService = Depends(get_calendar_service)
):
    pagination = PaginationParams(skip=skip, limit=limit)
    search_params = None
    if any([q, event_type, member_id, start_date, end_date]):
        search_params = SearchParams(
            q=q, event_type=event_type, member_id=member_id,
            start_date=start_date, end_date=end_date
        )
    return service.get_events(pagination, search_params)

@router.get("/calendar", response_model=List[CalendarEventResponse], summary="달력용 이벤트 조회")
async def get_calendar_events(
    start: date = Query(...),
    end: date = Query(...),
    member_id: Optional[int] = Query(None),
    service: CalendarService = Depends(get_calendar_service)
):
    return service.get_events_for_calendar(start, end, member_id)

@router.get("/today", response_model=List[EventResponse], summary="오늘 일정")
async def get_today_events(service: CalendarService = Depends(get_calendar_service)):
    return service.get_today_events()

@router.get("/upcoming", response_model=List[EventResponse], summary="다가오는 일정")
async def get_upcoming_events(
    days: int = Query(7, ge=1, le=30),
    service: CalendarService = Depends(get_calendar_service)
):
    return service.get_upcoming_events(days)

@router.get("/search", response_model=List[EventResponse], summary="이벤트 검색")
async def search_events(
    q: str = Query(..., min_length=1),
    service: CalendarService = Depends(get_calendar_service)
):
    return service.search_events(q)

@router.get("/stats", response_model=EventStats, summary="이벤트 통계")
async def get_event_stats(service: CalendarService = Depends(get_calendar_service)):
    return service.get_event_stats()

@router.get("/types", summary="이벤트 타입 목록")
async def get_event_types():
    return [{"value": v, "label": l} for v, l in EVENT_TYPES]

@router.get("/{event_id}", response_model=EventResponse, summary="이벤트 조회")
async def get_event(event_id: int, service: CalendarService = Depends(get_calendar_service)):
    event = service.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="이벤트를 찾을 수 없습니다.")
    return event

@router.put("/{event_id}", response_model=EventResponse, summary="이벤트 수정")
async def update_event(
    event_id: int,
    event_data: EventUpdate,
    service: CalendarService = Depends(get_calendar_service),
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: str = Depends(get_current_user_role)
):
    existing_event = service.get_event(event_id)
    if not existing_event:
        raise HTTPException(status_code=404, detail="이벤트를 찾을 수 없습니다.")
    
    if existing_event.created_by != current_user_id and current_user_role != "admin":
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    
    try:
        return service.update_event(event_id, event_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{event_id}", summary="이벤트 삭제")
async def delete_event(
    event_id: int,
    service: CalendarService = Depends(get_calendar_service),
    current_user_id: int = Depends(get_current_user_id),
    current_user_role: str = Depends(get_current_user_role)
):
    existing_event = service.get_event(event_id)
    if not existing_event:
        raise HTTPException(status_code=404, detail="이벤트를 찾을 수 없습니다.")
    
    if existing_event.created_by != current_user_id and current_user_role != "admin":
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    
    success = service.delete_event(event_id)
    if not success:
        raise HTTPException(status_code=404, detail="이벤트를 찾을 수 없습니다.")
    return {"message": "이벤트가 삭제되었습니다."}

events_router = router 