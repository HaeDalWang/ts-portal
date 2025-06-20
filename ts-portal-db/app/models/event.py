"""
팀 일정/이벤트 모델
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from ..database import Base


class Event(Base):
    """팀 일정/이벤트 테이블"""
    
    __tablename__ = "events"
    
    # 기본 정보
    id = Column(Integer, primary_key=True, index=True, comment="이벤트 고유 ID")
    title = Column(String(200), nullable=False, comment="일정 제목")
    description = Column(Text, comment="일정 상세 내용")
    
    # 일정 분류
    event_type = Column(String(50), nullable=False, default="other", comment="일정 타입")
    
    # 시간 정보
    start_time = Column(DateTime, nullable=False, comment="시작 시간")
    end_time = Column(DateTime, nullable=True, comment="종료 시간")
    
    # 장소 정보
    location = Column(String(200), comment="장소 (회의실, 온라인 링크 등)")
    
    # 생성자 정보
    created_by = Column(Integer, ForeignKey("members.id"), nullable=False, comment="생성자 ID")
    
    # 시스템 정보
    created_at = Column(DateTime, default=datetime.utcnow, comment="생성일시")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="수정일시")
    
    # 관계 설정
    creator = relationship("Member", back_populates="created_events")
    
    # 추가 필드
    all_day = Column(Boolean, default=False, comment="종일 일정 여부")
    participants = Column(Text, nullable=True, comment="참가자 (쉼표로 구분)")
    is_recurring = Column(Boolean, default=False, comment="반복 일정 여부")
    recurrence_rule = Column(String(500), nullable=True, comment="반복 규칙")
    color = Column(String(20), nullable=True, comment="달력 표시 색상")
    
    def __repr__(self):
        return f"<Event(id={self.id}, title='{self.title}', start_time='{self.start_time}')>"
    
    @property
    def duration_minutes(self):
        """이벤트 지속 시간 (분)"""
        if self.end_time and self.start_time:
            return int((self.end_time - self.start_time).total_seconds() / 60)
        return 0
    
    @property
    def is_today(self):
        """오늘 일정인지 확인"""
        today = datetime.now().date()
        return self.start_time.date() == today
    
    @property
    def is_upcoming(self):
        """다가오는 일정인지 확인 (현재 시간 이후)"""
        return self.start_time > datetime.now()
    
    @property
    def is_ongoing(self):
        """현재 진행 중인 일정인지 확인"""
        now = datetime.now()
        return self.start_time <= now <= self.end_time
    
    @property
    def status(self):
        """일정 상태 반환"""
        now = datetime.now()
        if self.end_time < now:
            return "completed"
        elif self.start_time <= now <= self.end_time:
            return "ongoing"
        else:
            return "upcoming"
    
    @property
    def event_type_display(self):
        """이벤트 타입 한글 표시"""
        type_map = {
            'vacation': '휴가',
            'remote': '재택근무',
            'business_trip': '출장',
            'project': '프로젝트',
            'education': '교육/세미나',
            'meeting': '회의',
            'other': '기타'
        }
        return type_map.get(self.event_type, self.event_type)
    
    @property
    def event_type_icon(self):
        """이벤트 타입 아이콘"""
        icon_map = {
            'vacation': '🌴',
            'remote': '🏠',
            'business_trip': '✈️',
            'project': '💼',
            'education': '📚',
            'meeting': '🤝',
            'other': '📝'
        }
        return icon_map.get(self.event_type, '📝')
    
    @property
    def default_color(self):
        """이벤트 타입별 기본 색상"""
        color_map = {
            'vacation': '#10B981',  # green
            'remote': '#3B82F6',    # blue
            'business_trip': '#F59E0B',  # amber
            'project': '#8B5CF6',   # violet
            'education': '#06B6D4', # cyan
            'meeting': '#EF4444',   # red
            'other': '#6B7280'      # gray
        }
        return self.color or color_map.get(self.event_type, '#6B7280') 