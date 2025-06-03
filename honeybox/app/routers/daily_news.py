"""
일일 소식 관련 엔드포인트
"""

import logging
from datetime import datetime
from fastapi import APIRouter

from ..models.schemas import DailyTipResponse, DailyTip, CacheInfo
from ..services.rss_service import RSSService
from ..services.selection_service import SelectionService
from ..services.translation_service import TranslationService
from ..utils.cache import daily_tip_cache
from ..config import settings

logger = logging.getLogger(__name__)

router = APIRouter(tags=["daily_news"])


@router.get("/daily-tip", response_model=DailyTipResponse)
async def get_daily_tip(translate: bool = False):
    """오늘의 AWS 소식을 반환합니다."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # 캐시 확인 (번역 여부에 따라 다른 캐시 키 사용)
    cache_key = f"{today_str}_translated" if translate else today_str
    cached_response = daily_tip_cache.get(cache_key)
    
    if cached_response:
        logger.info(f"캐시에서 일일 소식 반환: {cache_key}")
        cached_response["cache_info"]["cached"] = True
        return cached_response
    
    logger.info(f"새로운 일일 소식 생성 시작: {today_str} (번역: {translate})")
    
    # 오래된 캐시 정리
    daily_tip_cache.clear_old_entries(today_str)
    
    # 최근 게시물 수집 (14일)
    category_entries = await RSSService.collect_recent_entries(days_back=settings.DEFAULT_DAYS_BACK * 2)
    
    # 하이브리드 선별 로직 적용
    result = SelectionService.select_with_extended_search(category_entries, today_str)
    
    # 백업 로직: 14일 내에 적절한 항목이 없으면 30일로 확장
    if not result["entry"]:
        logger.info("14일 내 게시물 없음, 30일로 확장 검색")
        category_entries = await RSSService.collect_recent_entries(days_back=settings.EXTENDED_DAYS_BACK)
        result = SelectionService.select_with_extended_search(category_entries, today_str)
        
        if result["entry"]:
            result["metadata"].extended_search = True
    
    # 응답 생성
    if result["entry"]:
        entry = result["entry"]
        
        # 번역 처리
        title = entry.title
        summary = entry.summary
        translated = False
        
        if translate:
            title, summary, translated = TranslationService.translate_entry_content(
                entry.title, entry.summary
            )
        
        daily_tip = DailyTip(
            title=title,
            link=entry.link,
            summary=summary,
            published_readable=entry.published_readable,
            published=entry.published,
            quality_score=entry.quality_score or 0.0,
            tags=entry.tags,
            translated=translated
        )
        
        cache_info = CacheInfo(
            cached=False,
            cache_date=today_str,
            generated_at=datetime.now().isoformat(),
            translation_enabled=translate
        )
        
        response = DailyTipResponse(
            success=True,
            daily_tip=daily_tip,
            selection_metadata=result["metadata"],
            cache_info=cache_info
        )
        
        logger.info(f"일일 소식 생성 완료: {entry.title}")
        
    else:
        # 적절한 게시물을 찾지 못한 경우
        cache_info = CacheInfo(
            cached=False,
            cache_date=today_str,
            generated_at=datetime.now().isoformat(),
            translation_enabled=translate
        )
        
        response = DailyTipResponse(
            success=False,
            daily_tip=None,
            selection_metadata=result["metadata"],
            cache_info=cache_info,
            message="오늘은 추천할 소식이 없습니다.",
            suggestion="내일 다시 확인해주세요. 새로운 AWS 소식이 업데이트될 예정입니다."
        )
        
        logger.warning("일일 소식 생성 실패: 적절한 게시물 없음")
    
    # 캐시에 저장
    daily_tip_cache.set(cache_key, response.dict())
    
    return response 