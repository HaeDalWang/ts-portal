"""
Notice Service 모델 정의
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
import enum
from .database import Base

class NoticePriority(str, enum.Enum):
    """공지사항 중요도"""
    normal = "normal"      # 일반
    caution = "caution"    # 주의  
    important = "important" # 중요

class Notice(Base):
    """공지사항 테이블 (notice_schema.notices)"""
    __tablename__ = "notices"
    __table_args__ = {"schema": "notice_schema"}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, comment="제목")
    content = Column(Text, nullable=False, comment="내용")
    priority = Column(String(20), default="normal", comment="중요도")
    
    # 작성자 정보 (외래키 대신 단순 ID로 저장)
    author_id = Column(Integer, nullable=False, comment="작성자 ID")
    
    # 상태 정보
    is_active = Column(Boolean, default=True, comment="활성 상태")
    is_pinned = Column(Boolean, default=False, comment="상단 고정")
    
    # 타임스탬프
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성일시")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="수정일시")
    
    def __repr__(self):
        return f"<Notice(id={self.id}, title='{self.title}', priority='{self.priority}')>"
    
    @property
    def priority_display(self) -> str:
        """중요도 한글 표시"""
        priority_map = {
            "normal": "일반",
            "caution": "주의", 
            "important": "중요"
        }
        return priority_map.get(self.priority, "일반")
    
    @property
    def priority_color(self) -> str:
        """중요도별 색상"""
        color_map = {
            "normal": "#6B7280",     # gray-500
            "caution": "#F59E0B",    # amber-500
            "important": "#EF4444"   # red-500
        }
        return color_map.get(self.priority, "#6B7280")
    
    @property
    def priority_icon(self) -> str:
        """중요도별 아이콘"""
        icon_map = {
            "normal": "📢",
            "caution": "⚠️",
            "important": "🚨"
        }
        return icon_map.get(self.priority, "📢") 