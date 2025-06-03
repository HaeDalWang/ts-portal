"""
Pydantic 데이터 모델 스키마
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class FeedEntry(BaseModel):
    """RSS 피드 항목 모델"""
    title: str
    link: str
    summary: str
    published: Optional[str] = None
    published_readable: str
    published_raw: Optional[str] = None
    author: str = "작성자 미상"
    tags: List[str] = []
    quality_score: Optional[float] = None
    source_category: Optional[str] = None


class FeedInfo(BaseModel):
    """피드 정보 모델"""
    url: str
    name: str
    description: str


class FeedResponse(BaseModel):
    """피드 응답 모델"""
    feed_id: str
    name: str
    description: str
    url: str
    entries: List[FeedEntry]
    entry_count: int
    days_back: int
    collected_at: str
    error: Optional[str] = None


class AllFeedsResponse(BaseModel):
    """전체 피드 응답 모델"""
    results: Dict[str, FeedResponse]
    summary: Dict[str, Any]


class SelectionMetadata(BaseModel):
    """선별 메타데이터 모델"""
    date: str
    weekday: Optional[int] = None
    weekday_name: Optional[str] = None
    priority_categories: Optional[List[str]] = None
    selection_reason: str
    backup_used: bool = False
    candidate_count: int = 0
    quality_filter_applied: bool = True
    selected_category: Optional[str] = None
    category_name: Optional[str] = None
    extended_search: Optional[bool] = None
    error: Optional[str] = None


class CacheInfo(BaseModel):
    """캐시 정보 모델"""
    cached: bool
    cache_date: str
    generated_at: str
    translation_enabled: bool = False


class DailyTip(BaseModel):
    """일일 소식 모델"""
    title: str
    link: str
    summary: str
    published_readable: str
    published: Optional[str] = None
    quality_score: float = 0.0
    tags: List[str] = []
    translated: bool = False


class DailyTipResponse(BaseModel):
    """일일 소식 응답 모델"""
    success: bool
    daily_tip: Optional[DailyTip] = None
    selection_metadata: Optional[SelectionMetadata] = None
    cache_info: Optional[CacheInfo] = None
    message: Optional[str] = None
    suggestion: Optional[str] = None


class HealthResponse(BaseModel):
    """헬스 체크 응답 모델"""
    status: str
    timestamp: str


class FeedsListResponse(BaseModel):
    """피드 목록 응답 모델"""
    feeds: Dict[str, FeedInfo]
    total_feeds: int


class APIInfoResponse(BaseModel):
    """API 정보 응답 모델"""
    message: str
    version: str
    endpoints: Dict[str, str] 