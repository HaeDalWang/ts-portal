"""
공지사항 스키마 정의
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum

class NoticePriorityEnum(str, Enum):
    """공지사항 중요도 열거형"""
    normal = "normal"
    caution = "caution"
    important = "important"

class NoticeBase(BaseModel):
    """공지사항 기본 스키마"""
    title: str = Field(..., min_length=1, max_length=200, description="제목")
    content: str = Field(..., min_length=1, description="내용")
    priority: NoticePriorityEnum = Field(default=NoticePriorityEnum.normal, description="중요도")
    is_pinned: bool = Field(default=False, description="상단 고정 여부")

class NoticeCreate(NoticeBase):
    """공지사항 생성 스키마"""
    author_id: int = Field(..., description="작성자 ID")

class NoticeUpdate(BaseModel):
    """공지사항 수정 스키마"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="제목")
    content: Optional[str] = Field(None, min_length=1, description="내용")
    priority: Optional[NoticePriorityEnum] = Field(None, description="중요도")
    is_pinned: Optional[bool] = Field(None, description="상단 고정 여부")

class AuthorInfo(BaseModel):
    """작성자 정보"""
    id: int
    name: str
    email: str
    position: Optional[str] = None
    team: Optional[str] = None

class NoticeResponse(NoticeBase):
    """공지사항 응답 스키마"""
    id: int
    author_id: int
    author: Optional[AuthorInfo] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    # 추가 계산 필드
    priority_display: str = Field(..., description="중요도 한글 표시")
    priority_color: str = Field(..., description="중요도 색상")
    priority_icon: str = Field(..., description="중요도 아이콘")
    
    class Config:
        from_attributes = True

class NoticeListResponse(BaseModel):
    """공지사항 목록 응답 스키마"""
    total: int
    notices: List[NoticeResponse]

class NoticeStats(BaseModel):
    """공지사항 통계 스키마"""
    total_notices: int
    active_notices: int
    pinned_notices: int
    notices_by_priority: dict
    recent_notices: int

class SearchParams(BaseModel):
    """검색 파라미터"""
    q: Optional[str] = Field(None, description="검색 키워드")
    priority: Optional[NoticePriorityEnum] = Field(None, description="중요도 필터")
    author_id: Optional[int] = Field(None, description="작성자 필터")
    is_pinned: Optional[bool] = Field(None, description="고정 공지사항만")
    active_only: bool = Field(default=True, description="활성 공지사항만")

class PaginationParams(BaseModel):
    """페이지네이션 파라미터"""
    skip: int = Field(default=0, ge=0, description="건너뛸 개수")
    limit: int = Field(default=20, ge=1, le=100, description="가져올 개수") 