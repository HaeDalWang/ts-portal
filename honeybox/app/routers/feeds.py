"""
RSS 피드 관련 엔드포인트
"""

import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from ..config import settings
from ..models.schemas import FeedsListResponse, FeedInfo, FeedResponse, AllFeedsResponse
from ..services.rss_service import RSSService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/feeds", tags=["feeds"])


@router.get("/", response_model=FeedsListResponse)
async def get_feeds_list():
    """사용 가능한 RSS 피드 목록을 반환합니다."""
    feeds = {}
    for feed_id, feed_config in settings.AWS_BLOG_FEEDS.items():
        feeds[feed_id] = FeedInfo(
            url=feed_config["url"],
            name=feed_config["name"],
            description=feed_config["description"]
        )
    
    return FeedsListResponse(
        feeds=feeds,
        total_feeds=len(feeds)
    )


@router.get("/all")
async def get_all_feeds(days_back: int = 7):
    """모든 피드에서 최신 게시물을 수집합니다."""
    logger.info(f"전체 피드 수집 시작 (최근 {days_back}일)")
    
    results = {}
    total_entries = 0
    successful_feeds = 0
    failed_feeds = 0
    
    for feed_id, feed_config in settings.AWS_BLOG_FEEDS.items():
        try:
            logger.info(f"피드 처리 중: {feed_id}")
            
            # RSS 피드 가져오기
            result = RSSService.fetch_rss_feed(feed_config["url"])
            
            if result["success"]:
                # 엔트리 처리
                entries = RSSService.process_feed_entries(result["feed"], days_back)
                
                feed_response = FeedResponse(
                    feed_id=feed_id,
                    name=feed_config["name"],
                    description=feed_config["description"],
                    url=feed_config["url"],
                    entries=entries,
                    entry_count=len(entries),
                    days_back=days_back,
                    collected_at=datetime.now().isoformat()
                )
                
                results[feed_id] = feed_response
                total_entries += len(entries)
                successful_feeds += 1
                logger.info(f"{feed_id}: {len(entries)}개 수집 완료")
                
            else:
                # 실패한 피드도 결과에 포함 (오류 정보와 함께)
                feed_response = FeedResponse(
                    feed_id=feed_id,
                    name=feed_config["name"],
                    description=feed_config["description"],
                    url=feed_config["url"],
                    entries=[],
                    entry_count=0,
                    days_back=days_back,
                    collected_at=datetime.now().isoformat(),
                    error=result["error"]
                )
                
                results[feed_id] = feed_response
                failed_feeds += 1
                logger.warning(f"{feed_id}: 수집 실패 - {result['error']}")
                
        except Exception as e:
            logger.error(f"피드 처리 중 오류 ({feed_id}): {e}")
            failed_feeds += 1
            continue
    
    # 요약 정보
    summary = {
        "total_feeds": len(settings.AWS_BLOG_FEEDS),
        "successful_feeds": successful_feeds,
        "failed_feeds": failed_feeds,
        "total_entries": total_entries,
        "days_back": days_back,
        "collected_at": datetime.now().isoformat()
    }
    
    logger.info(f"전체 피드 수집 완료: {successful_feeds}/{len(settings.AWS_BLOG_FEEDS)}개 성공, 총 {total_entries}개 항목")
    
    return AllFeedsResponse(
        results=results,
        summary=summary
    )


@router.get("/{feed_id}", response_model=FeedResponse)
async def get_specific_feed(feed_id: str, days_back: int = 7):
    """특정 피드의 최신 게시물을 반환합니다."""
    if feed_id not in settings.AWS_BLOG_FEEDS:
        raise HTTPException(status_code=404, detail=f"피드를 찾을 수 없습니다: {feed_id}")
    
    feed_config = settings.AWS_BLOG_FEEDS[feed_id]
    logger.info(f"특정 피드 요청: {feed_id} (최근 {days_back}일)")
    
    try:
        # RSS 피드 가져오기
        result = RSSService.fetch_rss_feed(feed_config["url"])
        
        if not result["success"]:
            raise HTTPException(
                status_code=500, 
                detail=f"피드 가져오기 실패: {result['error']}"
            )
        
        # 엔트리 처리
        entries = RSSService.process_feed_entries(result["feed"], days_back)
        
        return FeedResponse(
            feed_id=feed_id,
            name=feed_config["name"],
            description=feed_config["description"],
            url=feed_config["url"],
            entries=entries,
            entry_count=len(entries),
            days_back=days_back,
            collected_at=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"특정 피드 처리 중 오류 ({feed_id}): {e}")
        raise HTTPException(status_code=500, detail=f"피드 처리 중 오류가 발생했습니다: {str(e)}") 