"""
날짜 처리 유틸리티 함수들
"""

import logging
from datetime import datetime
from typing import Optional
from dateutil import parser as date_parser

logger = logging.getLogger(__name__)


def parse_feed_date(date_string: str) -> Optional[datetime]:
    """RSS 피드의 다양한 날짜 형식을 파싱합니다."""
    if not date_string:
        return None
    
    try:
        # feedparser가 제공하는 parsed time을 먼저 시도
        return date_parser.parse(date_string)
    except Exception:
        try:
            # RFC 2822 형식 시도
            return datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %z")
        except Exception:
            try:
                # ISO 8601 형식 시도
                return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            except Exception:
                logger.warning(f"날짜 파싱 실패: {date_string}")
                return None 