"""
일일 소식 선별 로직 서비스
"""

import hashlib
import logging
from datetime import datetime
from typing import List, Dict, Optional, Tuple

from ..config import settings
from ..models.schemas import FeedEntry, SelectionMetadata
from ..services.quality_service import QualityService

logger = logging.getLogger(__name__)


class SelectionService:
    """일일 소식 선별 서비스"""
    
    @staticmethod
    def select_daily_tip_logic(category_entries: Dict[str, List[FeedEntry]], today_str: str) -> Dict:
        """하이브리드 선별 로직: 요일별 카테고리 우선순위 + 결정적 선택"""
        
        # 오늘의 요일 계산 (0=월요일, 6=일요일)
        today_date = datetime.strptime(today_str, "%Y-%m-%d")
        weekday = today_date.weekday()
        weekday_names = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
        weekday_name = weekday_names[weekday]
        
        logger.info(f"오늘의 요일: {weekday_name} ({weekday})")
        
        # 우선순위 카테고리 가져오기
        priority_categories = settings.WEEKDAY_CATEGORY_PRIORITY.get(weekday, ["aws-korea"])
        logger.info(f"우선순위 카테고리: {priority_categories}")
        
        selected_entry = None
        selection_reason = ""
        backup_used = False
        candidate_count = 0
        selected_category = None
        category_name = None
        
        # 1단계: 우선순위 카테고리에서 선택
        for category in priority_categories:
            if category in category_entries and category_entries[category]:
                category_name = settings.AWS_BLOG_FEEDS.get(category, {}).get("name", category)
                logger.info(f"카테고리 '{category_name}' 검사 중: {len(category_entries[category])}개 후보")
                
                # 품질 필터링
                qualified_entries = QualityService.filter_by_quality(
                    category_entries[category], 
                    settings.MIN_QUALITY_SCORE
                )
                
                if qualified_entries:
                    selected_entry = SelectionService._deterministic_select(qualified_entries, today_str)
                    selected_category = category
                    selection_reason = f"요일별 우선순위 ({weekday_name}) - {category_name}"
                    candidate_count = len(qualified_entries)
                    logger.info(f"우선순위 카테고리에서 선택됨: {selected_entry.title}")
                    break
        
        # 2단계: 백업 로직 - 모든 카테고리에서 선택
        if not selected_entry:
            logger.info("우선순위 카테고리에서 찾지 못함, 전체 카테고리 검색")
            backup_used = True
            
            all_qualified_entries = []
            for category, entries in category_entries.items():
                if entries:
                    qualified = QualityService.filter_by_quality(entries, settings.MIN_QUALITY_SCORE)
                    for entry in qualified:
                        entry.source_category = category
                    all_qualified_entries.extend(qualified)
            
            if all_qualified_entries:
                # 품질 점수 순으로 정렬
                all_qualified_entries.sort(key=lambda x: x.quality_score, reverse=True)
                selected_entry = SelectionService._deterministic_select(all_qualified_entries, today_str)
                selected_category = selected_entry.source_category
                category_name = settings.AWS_BLOG_FEEDS.get(selected_category, {}).get("name", selected_category)
                selection_reason = f"백업 선택 (전체 카테고리) - {category_name}"
                candidate_count = len(all_qualified_entries)
                logger.info(f"백업 로직으로 선택됨: {selected_entry.title}")
            else:
                logger.warning("품질 기준을 만족하는 게시물을 찾지 못함")
        
        # 메타데이터 생성
        metadata = SelectionMetadata(
            date=today_str,
            weekday=weekday,
            weekday_name=weekday_name,
            priority_categories=priority_categories,
            selection_reason=selection_reason,
            backup_used=backup_used,
            candidate_count=candidate_count,
            quality_filter_applied=True,
            selected_category=selected_category,
            category_name=category_name
        )
        
        return {
            "entry": selected_entry,
            "metadata": metadata
        }
    
    @staticmethod
    def _deterministic_select(entries: List[FeedEntry], seed: str) -> FeedEntry:
        """결정적 선택 알고리즘 (시드 기반)"""
        if not entries:
            return None
        
        # 시드를 사용하여 해시값 생성
        hash_object = hashlib.md5(seed.encode())
        hash_int = int(hash_object.hexdigest(), 16)
        
        # 해시값을 사용하여 인덱스 선택
        selected_index = hash_int % len(entries)
        selected_entry = entries[selected_index]
        
        logger.info(
            f"결정적 선택: 시드='{seed}', 후보={len(entries)}개, "
            f"선택인덱스={selected_index}, 제목='{selected_entry.title}'"
        )
        
        return selected_entry
    
    @staticmethod
    def select_with_extended_search(category_entries: Dict[str, List[FeedEntry]], today_str: str) -> Dict:
        """확장 검색을 포함한 선별 로직"""
        
        # 먼저 기본 로직 시도
        result = SelectionService.select_daily_tip_logic(category_entries, today_str)
        
        if result["entry"]:
            return result
        
        # 확장 검색: 더 낮은 품질 기준 적용
        logger.info("기본 선별 실패, 확장 검색 시작 (낮은 품질 기준)")
        
        today_date = datetime.strptime(today_str, "%Y-%m-%d")
        weekday = today_date.weekday()
        weekday_names = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
        weekday_name = weekday_names[weekday]
        
        all_qualified_entries = []
        for category, entries in category_entries.items():
            if entries:
                qualified = QualityService.filter_by_quality(entries, settings.EXTENDED_MIN_QUALITY_SCORE)
                for entry in qualified:
                    entry.source_category = category
                all_qualified_entries.extend(qualified)
        
        if all_qualified_entries:
            all_qualified_entries.sort(key=lambda x: x.quality_score, reverse=True)
            selected_entry = SelectionService._deterministic_select(all_qualified_entries, today_str)
            selected_category = selected_entry.source_category
            category_name = settings.AWS_BLOG_FEEDS.get(selected_category, {}).get("name", selected_category)
            
            metadata = SelectionMetadata(
                date=today_str,
                weekday=weekday,
                weekday_name=weekday_name,
                priority_categories=settings.WEEKDAY_CATEGORY_PRIORITY.get(weekday, ["aws-korea"]),
                selection_reason=f"확장 검색 (낮은 품질 기준) - {category_name}",
                backup_used=True,
                candidate_count=len(all_qualified_entries),
                quality_filter_applied=True,
                selected_category=selected_category,
                category_name=category_name,
                extended_search=True
            )
            
            logger.info(f"확장 검색으로 선택됨: {selected_entry.title}")
            
            return {
                "entry": selected_entry,
                "metadata": metadata
            }
        
        # 완전 실패
        logger.warning("확장 검색에서도 적절한 게시물을 찾지 못함")
        
        metadata = SelectionMetadata(
            date=today_str,
            weekday=weekday,
            weekday_name=weekday_name,
            priority_categories=settings.WEEKDAY_CATEGORY_PRIORITY.get(weekday, ["aws-korea"]),
            selection_reason="선별 실패 - 적절한 게시물을 찾지 못함",
            backup_used=True,
            candidate_count=0,
            quality_filter_applied=True,
            extended_search=True,
            error="적절한 게시물을 찾지 못했습니다"
        )
        
        return {
            "entry": None,
            "metadata": metadata
        }