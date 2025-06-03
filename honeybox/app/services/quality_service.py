"""
품질 평가 알고리즘 서비스
"""

import re
import logging
from typing import List, Set
from ..models.schemas import FeedEntry

logger = logging.getLogger(__name__)


class QualityService:
    """게시물 품질 평가 서비스"""
    
    # AWS 관련 키워드들
    AWS_KEYWORDS = {
        "architecture", "serverless", "lambda", "api", "gateway", "cloudformation",
        "terraform", "automation", "monitoring", "security", "performance",
        "optimization", "cost", "scaling", "deployment", "devops", "ci/cd",
        "container", "kubernetes", "docker", "microservices", "database",
        "analytics", "machine learning", "ai", "data", "storage", "backup",
        "disaster recovery", "compliance", "governance", "best practices",
        "tutorial", "guide", "how-to", "implementation", "integration"
    }
    
    @staticmethod
    def calculate_quality_score(entry: FeedEntry) -> float:
        """게시물의 품질 점수를 계산합니다."""
        score = 0.0
        
        # 1. 제목 길이 평가 (0.0 ~ 1.0점)
        title_length = len(entry.title)
        if 20 <= title_length <= 100:
            score += 1.0
        elif 10 <= title_length < 20 or 100 < title_length <= 150:
            score += 0.5
        
        # 2. 요약 내용 평가 (0.0 ~ 1.5점)
        summary_length = len(entry.summary)
        if summary_length >= 100:
            score += 1.5
        elif summary_length >= 50:
            score += 1.0
        elif summary_length >= 20:
            score += 0.5
        
        # 3. 태그 수 평가 (0.0 ~ 0.5점)
        tag_count = len(entry.tags)
        if tag_count >= 3:
            score += 0.5
        elif tag_count >= 1:
            score += 0.25
        
        # 4. AWS 관련 키워드 매칭 (0.0 ~ 1.0점)
        text_to_check = (entry.title + " " + entry.summary).lower()
        matched_keywords = QualityService._count_keyword_matches(text_to_check)
        
        if matched_keywords >= 3:
            score += 1.0
        elif matched_keywords >= 2:
            score += 0.7
        elif matched_keywords >= 1:
            score += 0.4
        
        # 5. 제목 품질 보너스 (0.0 ~ 0.5점)
        if QualityService._has_quality_title_indicators(entry.title):
            score += 0.5
        
        logger.debug(
            f"품질 점수 계산: '{entry.title[:50]}...' = {score:.2f} "
            f"(제목길이: {title_length}, 요약길이: {summary_length}, "
            f"태그: {tag_count}, 키워드: {matched_keywords})"
        )
        
        return round(score, 2)
    
    @staticmethod
    def _count_keyword_matches(text: str) -> int:
        """텍스트에서 AWS 키워드 매칭 개수를 세어봅니다."""
        matched_count = 0
        for keyword in QualityService.AWS_KEYWORDS:
            if keyword in text:
                matched_count += 1
        return matched_count
    
    @staticmethod
    def _has_quality_title_indicators(title: str) -> bool:
        """제목에 품질 지시어가 있는지 확인합니다."""
        quality_indicators = [
            "how to", "tutorial", "guide", "best practices", "tips",
            "optimization", "performance", "security", "automation",
            "implementation", "deep dive", "introduction", "getting started"
        ]
        
        title_lower = title.lower()
        return any(indicator in title_lower for indicator in quality_indicators)
    
    @staticmethod
    def filter_by_quality(entries: List[FeedEntry], min_score: float = 1.5) -> List[FeedEntry]:
        """품질 점수로 게시물을 필터링합니다."""
        qualified_entries = []
        
        for entry in entries:
            quality_score = QualityService.calculate_quality_score(entry)
            entry.quality_score = quality_score
            
            if quality_score >= min_score:
                qualified_entries.append(entry)
        
        # 품질 점수 순으로 정렬 (높은 순)
        qualified_entries.sort(key=lambda x: x.quality_score, reverse=True)
        
        logger.info(f"품질 필터링 결과: {len(qualified_entries)}/{len(entries)}개 통과 (최소 점수: {min_score})")
        
        return qualified_entries 