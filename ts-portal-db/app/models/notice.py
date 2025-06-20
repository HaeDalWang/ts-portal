"""
공지사항 모델
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database import Base

class NoticePriority(str, enum.Enum):
    """공지사항 중요도"""
    normal = "normal"      # 일반
    caution = "caution"    # 주의  
    important = "important" # 중요

class Notice(Base):
    """공지사항 테이블"""
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, comment="제목")
    content = Column(Text, nullable=False, comment="내용")
    priority = Column(Enum(NoticePriority), default=NoticePriority.normal, comment="중요도")
    
    # 작성자 정보
    author_id = Column(Integer, ForeignKey("members.id"), nullable=False, comment="작성자 ID")
    author = relationship("Member", back_populates="notices")
    
    # 상태 정보
    is_active = Column(Boolean, default=True, comment="활성 상태")
    is_pinned = Column(Boolean, default=False, comment="상단 고정")
    
    # 타임스탬프
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성일시")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="수정일시")
    
    def __repr__(self):
        return f"<Notice(id={self.id}, title='{self.title}', priority='{self.priority.value}')>"
    
    @property
    def priority_display(self) -> str:
        """중요도 한글 표시"""
        priority_map = {
            NoticePriority.normal: "일반",
            NoticePriority.caution: "주의", 
            NoticePriority.important: "중요"
        }
        return priority_map.get(self.priority, "일반")
    
    @property
    def priority_color(self) -> str:
        """중요도별 색상"""
        color_map = {
            NoticePriority.normal: "#6B7280",     # gray-500
            NoticePriority.caution: "#F59E0B",    # amber-500
            NoticePriority.important: "#EF4444"   # red-500
        }
        return color_map.get(self.priority, "#6B7280")
    
    @property
    def priority_icon(self) -> str:
        """중요도별 아이콘"""
        icon_map = {
            NoticePriority.normal: "📢",
            NoticePriority.caution: "⚠️",
            NoticePriority.important: "🚨"
        }
        return icon_map.get(self.priority, "📢") 