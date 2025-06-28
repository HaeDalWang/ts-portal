"""
Notice Service 비즈니스 로직
"""

from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_, func

from .models import Notice
from .schemas import (
    NoticeCreate, 
    NoticeUpdate, 
    NoticeResponse,
    NoticeListResponse,
    NoticeStats,
    SearchParams,
    PaginationParams,
    AuthorInfo
)

class NoticeService:
    """공지사항 서비스"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_notice(self, notice_data: NoticeCreate) -> NoticeResponse:
        """공지사항 생성"""
        # 공지사항 생성
        notice = Notice(
            title=notice_data.title,
            content=notice_data.content,
            priority=notice_data.priority.value,
            author_id=notice_data.author_id,
            is_pinned=notice_data.is_pinned
        )
        
        self.db.add(notice)
        self.db.commit()
        self.db.refresh(notice)
        
        return self._to_response(notice)
    
    def get_notice(self, notice_id: int) -> Optional[NoticeResponse]:
        """공지사항 단일 조회"""
        notice = self.db.query(Notice).filter(
            Notice.id == notice_id,
            Notice.is_active == True
        ).first()
        
        if not notice:
            return None
            
        return self._to_response(notice)
    
    def get_notices(self, params: PaginationParams) -> NoticeListResponse:
        """공지사항 목록 조회"""
        query = self.db.query(Notice).filter(Notice.is_active == True)
        
        # 고정 공지사항을 먼저, 그 다음 최신순
        query = query.order_by(desc(Notice.is_pinned), desc(Notice.created_at))
        
        # 전체 개수
        total = query.count()
        
        # 페이지네이션 적용
        notices = query.offset(params.skip).limit(params.limit).all()
        
        return NoticeListResponse(
            total=total,
            notices=[self._to_response(notice) for notice in notices]
        )
    
    def search_notices(self, search_params: SearchParams, pagination: PaginationParams) -> NoticeListResponse:
        """공지사항 검색"""
        query = self.db.query(Notice)
        
        # 활성 공지사항만
        if search_params.active_only:
            query = query.filter(Notice.is_active == True)
        
        # 키워드 검색
        if search_params.q:
            search_term = f"%{search_params.q}%"
            query = query.filter(
                or_(
                    Notice.title.ilike(search_term),
                    Notice.content.ilike(search_term)
                )
            )
        
        # 중요도 필터
        if search_params.priority:
            query = query.filter(Notice.priority == search_params.priority.value)
        
        # 작성자 필터
        if search_params.author_id:
            query = query.filter(Notice.author_id == search_params.author_id)
        
        # 고정 공지사항 필터
        if search_params.is_pinned is not None:
            query = query.filter(Notice.is_pinned == search_params.is_pinned)
        
        # 정렬: 고정 공지사항 먼저, 그 다음 최신순
        query = query.order_by(desc(Notice.is_pinned), desc(Notice.created_at))
        
        # 전체 개수
        total = query.count()
        
        # 페이지네이션 적용
        notices = query.offset(pagination.skip).limit(pagination.limit).all()
        
        return NoticeListResponse(
            total=total,
            notices=[self._to_response(notice) for notice in notices]
        )
    
    def update_notice(self, notice_id: int, notice_data: NoticeUpdate) -> Optional[NoticeResponse]:
        """공지사항 수정"""
        notice = self.db.query(Notice).filter(
            Notice.id == notice_id,
            Notice.is_active == True
        ).first()
        
        if not notice:
            return None
        
        # 수정할 필드만 업데이트
        update_data = notice_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "priority" and value:
                setattr(notice, field, value.value)
            else:
                setattr(notice, field, value)
        
        notice.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(notice)
        
        return self._to_response(notice)
    
    def delete_notice(self, notice_id: int) -> bool:
        """공지사항 삭제 (소프트 삭제)"""
        notice = self.db.query(Notice).filter(
            Notice.id == notice_id,
            Notice.is_active == True
        ).first()
        
        if not notice:
            return False
        
        notice.is_active = False
        notice.updated_at = datetime.utcnow()
        self.db.commit()
        
        return True
    
    def get_pinned_notices(self) -> List[NoticeResponse]:
        """고정 공지사항 조회"""
        notices = self.db.query(Notice).filter(
            Notice.is_active == True,
            Notice.is_pinned == True
        ).order_by(desc(Notice.created_at)).all()
        
        return [self._to_response(notice) for notice in notices]
    
    def get_recent_notices(self, days: int = 7, limit: int = 5) -> List[NoticeResponse]:
        """최근 공지사항 조회"""
        since_date = datetime.utcnow() - timedelta(days=days)
        
        notices = self.db.query(Notice).filter(
            Notice.is_active == True,
            Notice.created_at >= since_date
        ).order_by(desc(Notice.created_at)).limit(limit).all()
        
        return [self._to_response(notice) for notice in notices]
    
    def get_notices_by_author(self, author_id: int, pagination: PaginationParams) -> NoticeListResponse:
        """특정 작성자의 공지사항 조회"""
        query = self.db.query(Notice).filter(
            Notice.author_id == author_id,
            Notice.is_active == True
        ).order_by(desc(Notice.created_at))
        
        total = query.count()
        notices = query.offset(pagination.skip).limit(pagination.limit).all()
        
        return NoticeListResponse(
            total=total,
            notices=[self._to_response(notice) for notice in notices]
        )
    
    def get_notice_stats(self) -> NoticeStats:
        """공지사항 통계"""
        # 기본 통계
        total_notices = self.db.query(Notice).count()
        active_notices = self.db.query(Notice).filter(Notice.is_active == True).count()
        pinned_notices = self.db.query(Notice).filter(
            Notice.is_active == True,
            Notice.is_pinned == True
        ).count()
        
        # 중요도별 통계
        priority_stats = self.db.query(
            Notice.priority,
            func.count(Notice.id).label('count')
        ).filter(Notice.is_active == True).group_by(Notice.priority).all()
        
        notices_by_priority = {
            priority: count for priority, count in priority_stats
        }
        
        # 최근 7일 공지사항
        recent_date = datetime.utcnow() - timedelta(days=7)
        recent_notices = self.db.query(Notice).filter(
            Notice.is_active == True,
            Notice.created_at >= recent_date
        ).count()
        
        return NoticeStats(
            total_notices=total_notices,
            active_notices=active_notices,
            pinned_notices=pinned_notices,
            notices_by_priority=notices_by_priority,
            recent_notices=recent_notices
        )
    
    def _to_response(self, notice: Notice) -> NoticeResponse:
        """Notice 모델을 NoticeResponse로 변환"""
        # 작성자 정보는 일단 None으로 설정 (나중에 다른 서비스에서 조회)
        return NoticeResponse(
            id=notice.id,
            title=notice.title,
            content=notice.content,
            priority=notice.priority,
            author_id=notice.author_id,
            author=None,  # 추후 Member Service에서 조회
            is_active=notice.is_active,
            is_pinned=notice.is_pinned,
            created_at=notice.created_at,
            updated_at=notice.updated_at,
            priority_display=notice.priority_display,
            priority_color=notice.priority_color,
            priority_icon=notice.priority_icon
        ) 