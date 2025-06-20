"""
이벤트 관련 Pydantic 스키마
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class EventBase(BaseModel):
    """이벤트 기본 스키마"""
    title: str = Field(..., min_length=1, max_length=200, description="일정 제목")
    description: Optional[str] = Field(None, description="일정 설명")
    event_type: str = Field(default="other", description="일정 타입")
    start_time: datetime = Field(..., description="시작 시간")
    end_time: Optional[datetime] = Field(None, description="종료 시간")
    all_day: bool = Field(default=False, description="종일 일정 여부")
    location: Optional[str] = Field(None, max_length=200, description="장소")
    participants: Optional[str] = Field(None, description="참가자 (쉼표로 구분)")
    is_recurring: bool = Field(default=False, description="반복 일정 여부")
    recurrence_rule: Optional[str] = Field(None, max_length=500, description="반복 규칙")
    color: Optional[str] = Field(None, max_length=20, description="달력 표시 색상")
    created_by: int = Field(..., description="생성자 ID")


class EventCreate(EventBase):
    """이벤트 생성 스키마"""
    pass


class EventUpdate(BaseModel):
    """이벤트 수정 스키마"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="일정 제목")
    description: Optional[str] = Field(None, description="일정 설명")
    event_type: Optional[str] = Field(None, description="일정 타입")
    start_time: Optional[datetime] = Field(None, description="시작 시간")
    end_time: Optional[datetime] = Field(None, description="종료 시간")
    all_day: Optional[bool] = Field(None, description="종일 일정 여부")
    location: Optional[str] = Field(None, max_length=200, description="장소")
    participants: Optional[str] = Field(None, description="참가자 (쉼표로 구분)")
    is_recurring: Optional[bool] = Field(None, description="반복 일정 여부")
    recurrence_rule: Optional[str] = Field(None, max_length=500, description="반복 규칙")
    color: Optional[str] = Field(None, max_length=20, description="달력 표시 색상")


class EventResponse(EventBase):
    """이벤트 응답 스키마"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    # 계산된 속성들
    event_type_display: str
    event_type_icon: str
    default_color: str
    duration_minutes: int
    is_today: bool
    is_upcoming: bool
    is_ongoing: bool
    status: str
    
    # 관계 데이터 (선택적)
    creator: Optional[dict] = None

    class Config:
        from_attributes = True


class EventListResponse(BaseModel):
    """이벤트 목록 응답 스키마"""
    total: int
    events: List[EventResponse]


class EventStats(BaseModel):
    """이벤트 통계 스키마"""
    total_events: int
    today_events: int
    upcoming_events: int
    ongoing_events: int
    completed_events: int
    events_by_type: dict
    events_by_member: dict


class CalendarEventResponse(BaseModel):
    """달력용 이벤트 응답 스키마 (FullCalendar 형식)"""
    id: str  # FullCalendar는 string ID를 선호
    title: str
    start: str  # ISO 형식 날짜/시간
    end: Optional[str] = None
    allDay: bool = False
    color: Optional[str] = None
    backgroundColor: Optional[str] = None
    borderColor: Optional[str] = None
    textColor: Optional[str] = None
    
    # 추가 메타데이터
    extendedProps: dict = Field(default_factory=dict)

    class Config:
        from_attributes = True


# 이벤트 타입 상수
EVENT_TYPES = [
    ("vacation", "휴가"),
    ("remote", "재택근무"),
    ("business_trip", "출장"),
    ("project", "프로젝트"),
    ("education", "교육/세미나"),
    ("meeting", "회의"),
    ("other", "기타")
]

EVENT_TYPE_CHOICES = [choice[0] for choice in EVENT_TYPES] 