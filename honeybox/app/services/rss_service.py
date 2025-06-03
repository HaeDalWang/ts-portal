"""
RSS 피드 수집 및 파싱 서비스
"""

import re
import logging
import requests
import feedparser
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional

from ..config import settings
from ..models.schemas import FeedEntry
from ..utils.date_utils import parse_feed_date

logger = logging.getLogger(__name__)


class RSSService:
    """RSS 피드 처리 서비스"""
    
    @staticmethod
    def fetch_rss_feed(feed_url: str) -> Dict:
        """RSS 피드를 가져와서 파싱합니다."""
        try:
            logger.info(f"RSS 피드 가져오는 중: {feed_url}")
            
            # User-Agent 헤더 설정
            headers = {
                'User-Agent': 'HoneyBox-RSS-Parser/1.0 (AWS-Tips-Collector)'
            }
            
            # requests를 사용하여 RSS 피드 가져오기
            response = requests.get(
                feed_url, 
                headers=headers, 
                timeout=settings.RSS_REQUEST_TIMEOUT
            )
            response.raise_for_status()
            logger.info(f"RSS 피드 응답 크기: {len(response.content)} bytes")
            
            # feedparser로 파싱
            feed = feedparser.parse(response.content)
            logger.info(f"RSS 피드 파싱 완료: {len(feed.entries)}개 항목 발견")
            
            if feed.bozo:
                logger.warning(f"RSS 피드 파싱 경고: {feed_url} - {feed.bozo_exception}")
            
            return {
                "success": True,
                "feed": feed,
                "error": None
            }
        
        except requests.exceptions.RequestException as e:
            logger.error(f"RSS 피드 요청 실패: {feed_url} - {e}")
            return {
                "success": False,
                "feed": None,
                "error": f"네트워크 오류: {str(e)}"
            }
        except Exception as e:
            logger.error(f"RSS 피드 파싱 실패: {feed_url} - {e}")
            return {
                "success": False,
                "feed": None,
                "error": f"파싱 오류: {str(e)}"
            }
    
    @staticmethod
    def process_feed_entries(feed, days_back: int = 7) -> List[FeedEntry]:
        """피드 엔트리를 처리하여 구조화된 데이터로 변환합니다."""
        entries = []
        # UTC 기준으로 cutoff_date 계산
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)
        logger.info(f"날짜 필터링 기준: {cutoff_date.isoformat()} (최근 {days_back}일)")
        logger.info(f"총 {len(feed.entries)}개 항목 처리 시작")
        
        for i, entry in enumerate(feed.entries[:settings.MAX_ENTRIES_PER_FEED]):
            try:
                logger.debug(f"항목 {i+1} 처리 중: {getattr(entry, 'title', 'No title')}")
                
                # 발행일 파싱
                published_date = None
                published_raw = None
                
                if hasattr(entry, 'published'):
                    published_raw = entry.published
                    published_date = parse_feed_date(entry.published)
                    logger.debug(f"published 날짜: {published_raw} -> {published_date}")
                elif hasattr(entry, 'updated'):
                    published_raw = entry.updated
                    published_date = parse_feed_date(entry.updated)
                    logger.debug(f"updated 날짜: {published_raw} -> {published_date}")
                else:
                    logger.debug("날짜 정보 없음")
                
                # 날짜 필터링 (지정된 일수 이내의 항목만)
                if published_date:
                    # naive datetime을 UTC로 간주
                    if published_date.tzinfo is None:
                        published_date = published_date.replace(tzinfo=timezone.utc)
                    
                    if published_date < cutoff_date:
                        logger.debug(f"날짜 필터링으로 제외: {published_date} < {cutoff_date}")
                        continue
                    else:
                        logger.debug(f"날짜 필터링 통과: {published_date} >= {cutoff_date}")
                else:
                    logger.debug("날짜 정보가 없어 날짜 필터링 통과")
                
                # 요약 또는 설명 추출
                summary = ""
                if hasattr(entry, 'summary'):
                    summary = entry.summary
                elif hasattr(entry, 'description'):
                    summary = entry.description
                
                # HTML 태그 제거 (간단한 처리)
                summary = re.sub(r'<[^>]+>', '', summary)
                summary = summary.strip()[:500]  # 500자로 제한
                
                feed_entry = FeedEntry(
                    title=entry.title if hasattr(entry, 'title') else "제목 없음",
                    link=entry.link if hasattr(entry, 'link') else "",
                    summary=summary,
                    published=published_date.isoformat() if published_date else None,
                    published_readable=published_date.strftime("%Y년 %m월 %d일 %H:%M") if published_date else "날짜 미상",
                    published_raw=published_raw,
                    author=entry.author if hasattr(entry, 'author') else "작성자 미상",
                    tags=[tag.term for tag in entry.tags] if hasattr(entry, 'tags') else []
                )
                
                entries.append(feed_entry)
                logger.debug(f"항목 추가됨: {feed_entry.title}")
                
            except Exception as e:
                logger.warning(f"엔트리 처리 중 오류: {e}")
                continue
        
        logger.info(f"최종 처리된 항목 수: {len(entries)}")
        return entries
    
    @classmethod
    async def collect_recent_entries(cls, days_back: int = 14) -> Dict[str, List[FeedEntry]]:
        """최근 게시물들을 카테고리별로 수집합니다."""
        logger.info(f"최근 {days_back}일 게시물 수집 시작")
        category_entries = {}
        
        for feed_id, feed_config in settings.AWS_BLOG_FEEDS.items():
            logger.info(f"피드 수집 중: {feed_id}")
            
            # RSS 피드 가져오기
            result = cls.fetch_rss_feed(feed_config["url"])
            
            if result["success"]:
                entries = cls.process_feed_entries(result["feed"], days_back)
                category_entries[feed_id] = entries
                logger.info(f"{feed_id}: {len(entries)}개 수집 완료")
            else:
                category_entries[feed_id] = []
                logger.warning(f"{feed_id}: 수집 실패 - {result['error']}")
        
        return category_entries 