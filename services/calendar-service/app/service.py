"""
Calendar Service 비즈니스 로직
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_, func
import colorsys

from .models import Event
from .schemas import (
    EventCreate, 
    EventUpdate, 
    EventResponse,
    EventListResponse,
    EventStats,
    CalendarEventResponse,
    SearchParams,
    PaginationParams,
    CreatorInfo
)

class CalendarService:
    """캘린더 서비스"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_event(self, event_data: EventCreate) -> EventResponse:
        """이벤트 생성"""
        # 시간 유효성 검사
        if event_data.end_time and event_data.start_time >= event_data.end_time:
            raise ValueError("종료 시간은 시작 시간보다 늦어야 합니다.")
        
        # 이벤트 생성
        event = Event(
            title=event_data.title,
            description=event_data.description,
            event_type=event_data.event_type.value,
            start_time=event_data.start_time,
            end_time=event_data.end_time,
            is_all_day=event_data.is_all_day,
            location=event_data.location,
            is_recurring=event_data.is_recurring,
            recurrence_rule=event_data.recurrence_rule,
            created_by=event_data.created_by
        )
        
        # attendees 처리 (리스트나 딕셔너리 형태)
        if event_data.attendees:
            event.attendees = event_data.attendees
        
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        
        return self._to_response(event)
    
    def get_event(self, event_id: int) -> Optional[EventResponse]:
        """이벤트 단일 조회"""
        event = self.db.query(Event).filter(Event.id == event_id).first()
        
        if not event:
            return None
            
        return self._to_response(event)
    
    def get_events(self, params: PaginationParams, search_params: Optional[SearchParams] = None) -> EventListResponse:
        """이벤트 목록 조회"""
        query = self.db.query(Event)
        
        # 검색 조건 적용
        if search_params:
            # 키워드 검색
            if search_params.q:
                search_term = f"%{search_params.q}%"
                query = query.filter(
                    or_(
                        Event.title.ilike(search_term),
                        Event.description.ilike(search_term),
                        Event.location.ilike(search_term)
                    )
                )
            
            # 이벤트 타입 필터
            if search_params.event_type:
                query = query.filter(Event.event_type == search_params.event_type.value)
            
            # 생성자 필터
            if search_params.member_id:
                query = query.filter(Event.created_by == search_params.member_id)
            
            # 날짜 필터링 (복잡한 로직)
            if search_params.start_date or search_params.end_date:
                query = self._apply_date_filter(query, search_params.start_date, search_params.end_date)
        
        # 정렬: 최신 순
        query = query.order_by(desc(Event.start_time))
        
        # 전체 개수
        total = query.count()
        
        # 페이지네이션 적용
        events = query.offset(params.skip).limit(params.limit).all()
        
        return EventListResponse(
            total=total,
            events=[self._to_response(event) for event in events]
        )
    
    def get_events_for_calendar(self, start_date: date, end_date: date, 
                               member_id: Optional[int] = None) -> List[CalendarEventResponse]:
        """달력용 이벤트 목록 조회 (FullCalendar 형식)"""
        query = self.db.query(Event)
        
        # 날짜 범위 필터링
        query = self._apply_date_filter(query, start_date, end_date)
        
        # 특정 멤버 필터
        if member_id:
            query = query.filter(Event.created_by == member_id)
        
        events = query.order_by(Event.start_time).all()
        
        calendar_events = []
        for event in events:
            # 팀원별 동적 색상 생성
            member_color = self._generate_member_color(event.created_by)
            
            calendar_event = CalendarEventResponse(
                id=str(event.id),
                title=f"{event.event_type_icon} {event.title}",
                start=event.start_time.isoformat(),
                end=event.end_time.isoformat() if event.end_time else None,
                allDay=event.is_all_day,
                backgroundColor=member_color,
                borderColor=member_color,
                textColor='white',
                extendedProps={
                    'event_type': event.event_type,
                    'event_type_display': event.event_type_display,
                    'description': event.description,
                    'location': event.location,
                    'participants': ', '.join(str(attendee) for attendee in event.attendees if attendee) if event.attendees and isinstance(event.attendees, list) else '',
                    'attendees': event.attendees,
                    'creator_id': event.created_by,
                    'duration_minutes': event.duration_minutes,
                    'status': event.status
                }
            )
            calendar_events.append(calendar_event)
        
        return calendar_events
    
    def update_event(self, event_id: int, event_data: EventUpdate) -> Optional[EventResponse]:
        """이벤트 수정"""
        event = self.db.query(Event).filter(Event.id == event_id).first()
        
        if not event:
            return None
        
        # 수정할 필드만 업데이트
        update_data = event_data.model_dump(exclude_unset=True)
        
        # 시간 유효성 검사
        start_time = update_data.get('start_time', event.start_time)
        end_time = update_data.get('end_time', event.end_time)
        
        if end_time and start_time >= end_time:
            raise ValueError("종료 시간은 시작 시간보다 늦어야 합니다.")
        
        for field, value in update_data.items():
            if field == "event_type" and value:
                setattr(event, field, value.value)
            elif field == "attendees" and value is not None:
                # attendees 필드 특별 처리
                setattr(event, field, value)
            else:
                setattr(event, field, value)
        
        event.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(event)
        
        return self._to_response(event)
    
    def delete_event(self, event_id: int) -> bool:
        """이벤트 삭제"""
        event = self.db.query(Event).filter(Event.id == event_id).first()
        
        if not event:
            return False
        
        self.db.delete(event)
        self.db.commit()
        
        return True
    
    def get_today_events(self) -> List[EventResponse]:
        """오늘 일정 조회"""
        today = datetime.now().date()
        
        query = self.db.query(Event)
        query = self._apply_date_filter(query, today, today)
        
        events = query.order_by(Event.start_time).all()
        return [self._to_response(event) for event in events]
    
    def get_upcoming_events(self, days: int = 7) -> List[EventResponse]:
        """다가오는 일정 조회"""
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=days)
        
        events = self.db.query(Event).filter(
            and_(
                Event.start_time >= datetime.now(),
                func.date(Event.start_time).between(start_date, end_date)
            )
        ).order_by(Event.start_time).all()
        
        return [self._to_response(event) for event in events]
    
    def search_events(self, query_string: str) -> List[EventResponse]:
        """이벤트 검색"""
        events = self.db.query(Event).filter(
            or_(
                Event.title.ilike(f"%{query_string}%"),
                Event.description.ilike(f"%{query_string}%"),
                Event.location.ilike(f"%{query_string}%")
            )
        ).order_by(desc(Event.start_time)).all()
        
        return [self._to_response(event) for event in events]
    
    def get_events_by_member(self, member_id: int, pagination: PaginationParams) -> EventListResponse:
        """특정 멤버의 이벤트 조회"""
        query = self.db.query(Event).filter(
            Event.created_by == member_id
        ).order_by(desc(Event.start_time))
        
        total = query.count()
        events = query.offset(pagination.skip).limit(pagination.limit).all()
        
        return EventListResponse(
            total=total,
            events=[self._to_response(event) for event in events]
        )
    
    def get_events_by_type(self, event_type: str, start_date: Optional[date] = None, 
                          end_date: Optional[date] = None) -> List[EventResponse]:
        """타입별 이벤트 조회"""
        query = self.db.query(Event).filter(Event.event_type == event_type)
        
        if start_date or end_date:
            query = self._apply_date_filter(query, start_date, end_date)
        
        events = query.order_by(desc(Event.start_time)).all()
        return [self._to_response(event) for event in events]
    
    def get_event_stats(self) -> EventStats:
        """이벤트 통계"""
        now = datetime.now()
        today = now.date()
        
        # 기본 통계
        total_events = self.db.query(Event).count()
        today_events = self.db.query(Event).filter(
            func.date(Event.start_time) == today
        ).count()
        
        upcoming_events = self.db.query(Event).filter(
            Event.start_time > now
        ).count()
        
        ongoing_events = self.db.query(Event).filter(
            and_(
                Event.start_time <= now,
                Event.end_time >= now
            )
        ).count()
        
        completed_events = self.db.query(Event).filter(
            Event.end_time < now
        ).count()
        
        # 타입별 통계
        type_stats = self.db.query(
            Event.event_type,
            func.count(Event.id).label('count')
        ).group_by(Event.event_type).all()
        
        events_by_type = {
            event_type: count for event_type, count in type_stats
        }
        
        # 멤버별 통계 (ID만 - 이름은 다른 서비스에서 조회)
        member_stats = self.db.query(
            Event.created_by,
            func.count(Event.id).label('count')
        ).group_by(Event.created_by).all()
        
        events_by_member = {
            f"member_{member_id}": count for member_id, count in member_stats
        }
        
        return EventStats(
            total_events=total_events,
            today_events=today_events,
            upcoming_events=upcoming_events,
            ongoing_events=ongoing_events,
            completed_events=completed_events,
            events_by_type=events_by_type,
            events_by_member=events_by_member
        )
    
    def _apply_date_filter(self, query, start_date: Optional[date], end_date: Optional[date]):
        """날짜 필터링 적용 (복잡한 로직)"""
        if start_date and end_date:
            # 특정 날짜 범위 내에 겹치는 이벤트를 찾기
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date + timedelta(days=1), datetime.min.time())
            
            # 이벤트가 조회 범위와 겹치는 조건:
            # 1. 이벤트 시작일이 조회 종료일 이전이고
            # 2. 이벤트 종료일이 조회 시작일 이후인 경우
            query = query.filter(
                and_(
                    Event.start_time < end_datetime,
                    Event.end_time >= start_datetime
                )
            )
        elif start_date:
            # 시작일만 지정된 경우
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(start_date + timedelta(days=1), datetime.min.time())
            
            query = query.filter(
                and_(
                    Event.start_time < end_datetime,
                    Event.end_time >= start_datetime
                )
            )
        elif end_date:
            # 종료일만 지정된 경우
            end_datetime = datetime.combine(end_date + timedelta(days=1), datetime.min.time())
            query = query.filter(Event.start_time < end_datetime)
        
        return query
    
    def _generate_member_color(self, member_id: int) -> str:
        """팀원 ID 기반 동적 색상 생성"""
        # HSL 색상 생성 (프론트엔드와 동일한 로직)
        hue = (member_id * 137.508) % 360
        saturation = 45 + (member_id % 15)  # 45-60% 채도로 부드러운 색상
        lightness = 60 + (member_id % 15)   # 60-75% 명도로 옅은 색상
        
        # HSL을 HEX로 변환
        h, s, l = hue / 360, saturation / 100, lightness / 100
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
    
    def _to_response(self, event: Event) -> EventResponse:
        """Event 모델을 EventResponse로 변환"""
        # 하위 호환성을 위한 participants 문자열 계산
        participants_str = ""
        if event.attendees:
            if isinstance(event.attendees, list):
                participants_str = ', '.join(str(attendee) for attendee in event.attendees if attendee)
            elif isinstance(event.attendees, dict):
                participants_str = ', '.join(str(v) for v in event.attendees.values() if v)
        
        return EventResponse(
            id=event.id,
            title=event.title,
            description=event.description,
            event_type=event.event_type,
            start_time=event.start_time,
            end_time=event.end_time,
            is_all_day=event.is_all_day,
            location=event.location,
            attendees=event.attendees,
            is_recurring=event.is_recurring,
            recurrence_rule=event.recurrence_rule,
            created_by=event.created_by,
            created_at=event.created_at,
            updated_at=event.updated_at,
            creator=None,  # 추후 Member Service에서 조회
            # 계산된 속성들
            event_type_display=event.event_type_display,
            event_type_icon=event.event_type_icon,
            default_color=event.default_color,
            duration_minutes=event.duration_minutes,
            is_today=event.is_today,
            is_upcoming=event.is_upcoming,
            is_ongoing=event.is_ongoing,
            status=event.status,
            # 하위 호환성 필드들
            participants=participants_str,
            all_day=event.is_all_day,
            color=event.default_color
        ) 