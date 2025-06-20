"""
이벤트 관련 서비스 레이어
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_, func, extract
from fastapi import HTTPException, status

from ..models.event import Event
from ..models.member import Member
from ..schemas.event import EventCreate, EventUpdate, CalendarEventResponse


class EventService:
    """이벤트 관련 비즈니스 로직"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_event(self, event_id: int) -> Optional[Event]:
        """이벤트 단일 조회"""
        return self.db.query(Event).options(
            joinedload(Event.creator)
        ).filter(Event.id == event_id).first()
    
    def get_events(self, skip: int = 0, limit: int = 100, 
                   member_id: Optional[int] = None,
                   event_type: Optional[str] = None,
                   start_date: Optional[date] = None,
                   end_date: Optional[date] = None) -> List[Event]:
        """이벤트 목록 조회"""
        query = self.db.query(Event).options(joinedload(Event.creator))
        
        # 필터링
        if member_id:
            query = query.filter(Event.created_by == member_id)
        
        if event_type:
            query = query.filter(Event.event_type == event_type)
        
        if start_date:
            query = query.filter(Event.start_time >= start_date)
        
        if end_date:
            # end_date 다음날 00:00:00 전까지
            end_datetime = datetime.combine(end_date + timedelta(days=1), datetime.min.time())
            query = query.filter(Event.start_time < end_datetime)
        
        return query.order_by(Event.start_time.desc()).offset(skip).limit(limit).all()
    
    def get_events_for_calendar(self, start_date: date, end_date: date, 
                               member_id: Optional[int] = None) -> List[CalendarEventResponse]:
        """달력용 이벤트 목록 조회 (FullCalendar 형식)"""
        events = self.get_events(
            start_date=start_date,
            end_date=end_date,
            member_id=member_id,
            limit=1000  # 달력용은 많은 데이터 필요
        )
        
        calendar_events = []
        for event in events:
            # 팀원 ID 기반 동적 색상 생성
            def generate_member_color(member_id: int) -> str:
                # HSL 색상 생성 (프론트엔드와 동일한 로직)
                hue = (member_id * 137.508) % 360
                saturation = 45 + (member_id % 15)  # 45-60% 채도로 부드러운 색상
                lightness = 60 + (member_id % 15)   # 60-75% 명도로 옅은 색상
                
                # HSL을 HEX로 변환
                import colorsys
                h, s, l = hue / 360, saturation / 100, lightness / 100
                r, g, b = colorsys.hls_to_rgb(h, l, s)
                return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
            
            # 팀원별 색상 또는 기본 색상
            member_color = generate_member_color(event.created_by) if event.created_by else event.default_color
            
            calendar_event = CalendarEventResponse(
                id=str(event.id),
                title=f"{event.event_type_icon} {event.title}",
                start=event.start_time.isoformat(),
                end=event.end_time.isoformat() if event.end_time else None,
                allDay=event.all_day,
                backgroundColor=member_color,
                borderColor=member_color,
                textColor='white',
                extendedProps={
                    'event_type': event.event_type,
                    'event_type_display': event.event_type_display,
                    'description': event.description,
                    'location': event.location,
                    'participants': event.participants,
                    'creator_name': event.creator.name if event.creator else None,
                    'creator_id': event.created_by,
                    'duration_minutes': event.duration_minutes,
                    'status': event.status
                }
            )
            calendar_events.append(calendar_event)
        
        return calendar_events
    
    def create_event(self, event_data: EventCreate) -> Event:
        """이벤트 생성"""
        try:
            # 생성자 확인
            creator = self.db.query(Member).filter(Member.id == event_data.created_by).first()
            if not creator:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"팀원 ID {event_data.created_by}를 찾을 수 없습니다."
                )
            
            # 시간 유효성 검사
            if event_data.end_time and event_data.start_time >= event_data.end_time:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="종료 시간은 시작 시간보다 늦어야 합니다."
                )
            
            # 이벤트 생성
            db_event = Event(**event_data.model_dump())
            self.db.add(db_event)
            self.db.commit()
            self.db.refresh(db_event)
            
            return db_event
            
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이벤트 생성 중 오류가 발생했습니다."
            )
    
    def update_event(self, event_id: int, event_data: EventUpdate) -> Optional[Event]:
        """이벤트 수정"""
        db_event = self.get_event(event_id)
        if not db_event:
            return None
        
        try:
            # 업데이트할 데이터만 추출
            update_data = event_data.model_dump(exclude_unset=True)
            
            # 시간 유효성 검사
            start_time = update_data.get('start_time', db_event.start_time)
            end_time = update_data.get('end_time', db_event.end_time)
            
            if end_time and start_time >= end_time:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="종료 시간은 시작 시간보다 늦어야 합니다."
                )
            
            # 필드 업데이트
            for field, value in update_data.items():
                setattr(db_event, field, value)
            
            self.db.commit()
            self.db.refresh(db_event)
            
            return db_event
            
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이벤트 수정 중 오류가 발생했습니다."
            )
    
    def delete_event(self, event_id: int) -> bool:
        """이벤트 삭제"""
        db_event = self.get_event(event_id)
        if not db_event:
            return False
        
        try:
            self.db.delete(db_event)
            self.db.commit()
            return True
            
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이벤트 삭제 중 오류가 발생했습니다."
            )
    
    def get_event_stats(self) -> Dict[str, Any]:
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
        events_by_type = {}
        type_stats = self.db.query(
            Event.event_type,
            func.count(Event.id).label('count')
        ).group_by(Event.event_type).all()
        
        for event_type, count in type_stats:
            events_by_type[event_type] = count
        
        # 팀원별 통계
        events_by_member = {}
        member_stats = self.db.query(
            Member.name,
            func.count(Event.id).label('count')
        ).join(Event, Member.id == Event.created_by)\
         .group_by(Member.id, Member.name).all()
        
        for member_name, count in member_stats:
            events_by_member[member_name] = count
        
        return {
            'total_events': total_events,
            'today_events': today_events,
            'upcoming_events': upcoming_events,
            'ongoing_events': ongoing_events,
            'completed_events': completed_events,
            'events_by_type': events_by_type,
            'events_by_member': events_by_member
        }
    
    def get_today_events(self) -> List[Event]:
        """오늘 일정 조회"""
        today = datetime.now().date()
        return self.get_events(start_date=today, end_date=today)
    
    def get_upcoming_events(self, days: int = 7) -> List[Event]:
        """다가오는 일정 조회 (기본 7일)"""
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=days)
        
        return self.db.query(Event).options(joinedload(Event.creator)).filter(
            and_(
                Event.start_time >= datetime.now(),
                func.date(Event.start_time).between(start_date, end_date)
            )
        ).order_by(Event.start_time).all()
    
    def search_events(self, query: str) -> List[Event]:
        """이벤트 검색"""
        return self.db.query(Event).options(joinedload(Event.creator)).filter(
            or_(
                Event.title.ilike(f"%{query}%"),
                Event.description.ilike(f"%{query}%"),
                Event.location.ilike(f"%{query}%")
            )
        ).order_by(Event.start_time.desc()).all() 