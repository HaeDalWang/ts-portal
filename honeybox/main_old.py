from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import feedparser
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional
import logging
from dateutil import parser as date_parser
import requests
import hashlib
import asyncio
import os

# 로깅 설정
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 번역 기능 (선택적)
ENABLE_TRANSLATION = os.getenv("ENABLE_TRANSLATION", "false").lower() == "true"
AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-2")

if ENABLE_TRANSLATION:
    try:
        import boto3
        translate_client = boto3.client('translate', region_name=AWS_REGION)
        logger = logging.getLogger(__name__)
        logger.info("AWS Translate 활성화됨")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.warning(f"AWS Translate 초기화 실패: {e}")
        ENABLE_TRANSLATION = False

# FastAPI 애플리케이션 초기화
app = FastAPI(
    title="HoneyBox - AWS 팁 블로그 RSS 수집기",
    description="AWS 블로그들의 RSS를 수집하여 매일 하나씩 선별해서 보여주는 API",
    version="1.0.0"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포시에는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AWS 블로그 RSS 피드 설정
AWS_BLOG_FEEDS = {
    "aws-news": {
        "url": "https://aws.amazon.com/blogs/aws/feed/",
        "name": "AWS News Blog",
        "description": "공식 AWS 뉴스 및 제품 업데이트"
    },
    "aws-architecture": {
        "url": "https://aws.amazon.com/blogs/architecture/feed/",
        "name": "AWS Architecture Blog",
        "description": "AWS 아키텍처 및 설계 패턴"
    },
    "aws-devops": {
        "url": "https://aws.amazon.com/blogs/devops/feed/",
        "name": "AWS DevOps Blog",
        "description": "AWS DevOps 및 개발자 생산성"
    },
    "aws-security": {
        "url": "https://aws.amazon.com/blogs/security/feed/",
        "name": "AWS Security Blog",
        "description": "AWS 보안 모범 사례 및 팁"
    },
    "aws-opensource": {
        "url": "https://aws.amazon.com/blogs/opensource/feed/",
        "name": "AWS Open Source Blog",
        "description": "AWS 오픈소스 프로젝트 및 기여"
    },
    "aws-whats-new": {
        "url": "https://aws.amazon.com/about-aws/whats-new/recent/feed/",
        "name": "AWS What's New",
        "description": "AWS 신규 서비스 및 기능 발표"
    },
    "aws-korea": {
        "url": "https://aws.amazon.com/ko/blogs/korea/feed/",
        "name": "AWS Korea Blog",
        "description": "AWS 한국 블로그 - 한국어 콘텐츠"
    }
}

# 일일 캐시 (메모리 기반)
daily_tip_cache = {}

# 요일별 카테고리 우선순위 설정
WEEKDAY_CATEGORY_PRIORITY = {
    0: ["aws-korea", "aws-architecture", "aws-news"],      # 월요일: 한국 블로그 우선, 아키텍처 중심
    1: ["aws-korea", "aws-security", "aws-devops"],        # 화요일: 한국 블로그 우선, 보안 & DevOps
    2: ["aws-korea", "aws-devops", "aws-opensource"],      # 수요일: 한국 블로그 우선, 개발 중심
    3: ["aws-korea", "aws-news", "aws-whats-new"],         # 목요일: 한국 블로그 우선, 새소식 중심
    4: ["aws-korea", "aws-architecture", "aws-security"],  # 금요일: 한국 블로그 우선, 아키텍처 & 보안
    5: ["aws-korea", "aws-opensource", "aws-news"],        # 토요일: 한국 블로그 우선, 오픈소스 & 뉴스
    6: ["aws-korea", "aws-whats-new", "aws-devops"]        # 일요일: 한국 블로그 우선, 신기능 & DevOps
}

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

def translate_text_to_korean(text: str, max_chars: int = 5000) -> str:
    """텍스트를 한국어로 번역합니다."""
    if not ENABLE_TRANSLATION or not text.strip():
        return text
    
    try:
        # 텍스트 길이 제한 (AWS Translate 비용 절약)
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
        
        # 영어인지 간단히 확인 (ASCII 문자 비율로 판단)
        ascii_ratio = sum(1 for c in text if ord(c) < 128) / len(text)
        if ascii_ratio < 0.7:  # 한글이나 다른 언어로 추정
            return text
        
        # AWS Translate로 번역
        result = translate_client.translate_text(
            Text=text,
            SourceLanguageCode='en',
            TargetLanguageCode='ko'
        )
        
        translated = result.get('TranslatedText', text)
        logger.debug(f"번역 완료: {text[:50]}... -> {translated[:50]}...")
        return translated
        
    except Exception as e:
        logger.warning(f"번역 실패: {e}")
        return text

def fetch_rss_feed(feed_url: str) -> Dict:
    """RSS 피드를 가져와서 파싱합니다."""
    try:
        logger.info(f"RSS 피드 가져오는 중: {feed_url}")
        
        # User-Agent 헤더 설정
        headers = {
            'User-Agent': 'HoneyBox-RSS-Parser/1.0 (AWS-Tips-Collector)'
        }
        
        # requests를 사용하여 RSS 피드 가져오기
        response = requests.get(feed_url, headers=headers, timeout=30)
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

def process_feed_entries(feed, days_back: int = 7) -> List[Dict]:
    """피드 엔트리를 처리하여 구조화된 데이터로 변환합니다."""
    entries = []
    # UTC 기준으로 cutoff_date 계산
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)
    logger.info(f"날짜 필터링 기준: {cutoff_date.isoformat()} (최근 {days_back}일)")
    logger.info(f"총 {len(feed.entries)}개 항목 처리 시작")
    
    for i, entry in enumerate(feed.entries[:20]):  # 최대 20개 항목만 처리
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
            import re
            summary = re.sub(r'<[^>]+>', '', summary)
            summary = summary.strip()[:500]  # 500자로 제한
            
            processed_entry = {
                "title": entry.title if hasattr(entry, 'title') else "제목 없음",
                "link": entry.link if hasattr(entry, 'link') else "",
                "summary": summary,
                "published": published_date.isoformat() if published_date else None,
                "published_readable": published_date.strftime("%Y년 %m월 %d일 %H:%M") if published_date else "날짜 미상",
                "published_raw": published_raw,  # 디버깅용 원본 날짜
                "author": entry.author if hasattr(entry, 'author') else "작성자 미상",
                "tags": [tag.term for tag in entry.tags] if hasattr(entry, 'tags') else []
            }
            
            entries.append(processed_entry)
            logger.debug(f"항목 추가됨: {processed_entry['title']}")
            
        except Exception as e:
            logger.warning(f"엔트리 처리 중 오류: {e}")
            continue
    
    logger.info(f"최종 처리된 항목 수: {len(entries)}")
    return entries

@app.get("/")
async def root():
    """API 루트 엔드포인트"""
    return {
        "message": "HoneyBox - AWS 팁 블로그 RSS 수집기 API", 
        "version": "1.0.0",
        "endpoints": {
            "/health": "헬스 체크",
            "/feeds": "사용 가능한 RSS 피드 목록",
            "/feeds/all": "모든 피드에서 최신 게시물 수집",
            "/feeds/{feed_id}": "특정 피드의 게시물 조회",
            "/daily-tip": "오늘의 AWS 팁 (추후 구현)"
        }
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/feeds")
async def get_available_feeds():
    """사용 가능한 RSS 피드 목록을 반환합니다."""
    return {
        "feeds": AWS_BLOG_FEEDS,
        "total_feeds": len(AWS_BLOG_FEEDS)
    }

@app.get("/feeds/all")
async def get_all_feeds(days_back: int = 7):
    """모든 RSS 피드에서 최신 게시물을 수집합니다."""
    all_results = {}
    total_entries = 0
    
    for feed_id, feed_config in AWS_BLOG_FEEDS.items():
        logger.info(f"피드 처리 중: {feed_id}")
        
        # RSS 피드 가져오기
        result = fetch_rss_feed(feed_config["url"])
        
        if result["success"]:
            # 엔트리 처리
            entries = process_feed_entries(result["feed"], days_back)
            total_entries += len(entries)
            
            all_results[feed_id] = {
                "name": feed_config["name"],
                "description": feed_config["description"],
                "url": feed_config["url"],
                "entries": entries,
                "entry_count": len(entries),
                "error": None
            }
        else:
            all_results[feed_id] = {
                "name": feed_config["name"],
                "description": feed_config["description"],
                "url": feed_config["url"],
                "entries": [],
                "entry_count": 0,
                "error": result["error"]
            }
    
    return {
        "results": all_results,
        "summary": {
            "total_feeds": len(AWS_BLOG_FEEDS),
            "total_entries": total_entries,
            "days_back": days_back,
            "collected_at": datetime.now().isoformat()
        }
    }

@app.get("/feeds/{feed_id}")
async def get_specific_feed(feed_id: str, days_back: int = 7):
    """특정 RSS 피드의 게시물을 조회합니다."""
    if feed_id not in AWS_BLOG_FEEDS:
        raise HTTPException(status_code=404, detail=f"피드를 찾을 수 없습니다: {feed_id}")
    
    feed_config = AWS_BLOG_FEEDS[feed_id]
    
    # RSS 피드 가져오기
    result = fetch_rss_feed(feed_config["url"])
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=f"RSS 피드 가져오기 실패: {result['error']}")
    
    # 엔트리 처리
    entries = process_feed_entries(result["feed"], days_back)
    
    return {
        "feed_id": feed_id,
        "name": feed_config["name"],
        "description": feed_config["description"],
        "url": feed_config["url"],
        "entries": entries,
        "entry_count": len(entries),
        "days_back": days_back,
        "collected_at": datetime.now().isoformat()
    }

@app.get("/daily-tip")
async def get_daily_tip(translate: bool = False):
    """오늘의 AWS 팁을 반환합니다."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # 캐시 확인 (번역 여부에 따라 다른 캐시 키 사용)
    cache_key = f"{today_str}_translated" if translate else today_str
    if cache_key in daily_tip_cache:
        logger.info(f"캐시에서 일일 팁 반환: {cache_key}")
        cached_response = daily_tip_cache[cache_key].copy()
        cached_response["cache_info"]["cached"] = True
        return cached_response
    
    logger.info(f"새로운 일일 팁 생성 시작: {today_str} (번역: {translate})")
    
    # 최근 게시물 수집 (14일)
    category_entries = await collect_recent_entries(days_back=14)
    
    # 하이브리드 선별 로직 적용
    result = select_daily_tip_logic(category_entries, today_str)
    
    # 백업 로직: 14일 내에 적절한 항목이 없으면 30일로 확장
    if not result["entry"]:
        logger.info("14일 내 항목 없음, 30일로 확장 검색")
        result = await expand_search_range(today_str)
    
    # 응답 구성
    if result["entry"]:
        entry = result["entry"].copy()
        
        # 번역 처리
        if translate and ENABLE_TRANSLATION:
            logger.info("번역 처리 시작")
            entry["title"] = translate_text_to_korean(entry["title"])
            entry["summary"] = translate_text_to_korean(entry["summary"])
            # 태그는 번역하지 않음 (기술 용어이므로)
        
        response = {
            "success": True,
            "daily_tip": {
                "title": entry["title"],
                "link": entry["link"],
                "summary": entry["summary"],
                "published_readable": entry["published_readable"],
                "published": entry["published"],
                "quality_score": entry.get("quality_score", 0),
                "tags": entry["tags"],
                "translated": translate and ENABLE_TRANSLATION
            },
            "selection_metadata": result["metadata"],
            "cache_info": {
                "cached": False,
                "cache_date": today_str,
                "generated_at": datetime.now().isoformat(),
                "translation_enabled": ENABLE_TRANSLATION
            }
        }
    else:
        response = {
            "success": False,
            "message": "오늘 추천할 수 있는 AWS 팁을 찾지 못했습니다.",
            "selection_metadata": result["metadata"],
            "suggestion": "나중에 다시 시도하거나 /feeds/all 엔드포인트를 사용해보세요.",
            "cache_info": {
                "cached": False,
                "cache_date": today_str,
                "generated_at": datetime.now().isoformat(),
                "translation_enabled": ENABLE_TRANSLATION
            }
        }
    
    # 캐시에 저장 (성공/실패 상관없이)
    daily_tip_cache[cache_key] = response
    
    # 이전 날짜 캐시 정리 (메모리 절약)
    cache_keys_to_remove = [key for key in daily_tip_cache.keys() if key.split('_')[0] < today_str]
    for key in cache_keys_to_remove:
        del daily_tip_cache[key]
        
    logger.info(f"오늘의 팁 생성 완료: {today_str} (번역: {translate})")
    return response

def calculate_quality_score(entry: Dict) -> float:
    """게시물의 품질 점수를 계산합니다."""
    score = 0.0
    
    # 제목 길이 (적절한 길이 선호)
    title_len = len(entry.get('title', ''))
    if 30 <= title_len <= 120:
        score += 2.0
    elif title_len >= 120:
        score += 1.0
    
    # 요약 길이 (내용이 충실한지 확인)
    summary_len = len(entry.get('summary', ''))
    if summary_len >= 200:
        score += 3.0
    elif summary_len >= 100:
        score += 2.0
    elif summary_len >= 50:
        score += 1.0
    
    # 태그 개수 (카테고리화가 잘 되어있는지)
    tag_count = len(entry.get('tags', []))
    score += min(tag_count * 0.5, 2.0)
    
    # 키워드 보너스 (유용한 키워드가 포함되어 있는지)
    useful_keywords = [
        'tutorial', 'guide', 'best practices', 'how to', 'tips',
        '가이드', '방법', '팁', '모범 사례', '튜토리얼',
        'architecture', 'security', 'performance', 'cost',
        '아키텍처', '보안', '성능', '비용'
    ]
    
    title_lower = entry.get('title', '').lower()
    summary_lower = entry.get('summary', '').lower()
    
    for keyword in useful_keywords:
        if keyword in title_lower or keyword in summary_lower:
            score += 0.5
    
    return score

def filter_quality_entries(entries: List[Dict], min_score: float = 2.0) -> List[Dict]:
    """품질 점수 기준으로 게시물을 필터링합니다."""
    quality_entries = []
    
    for entry in entries:
        score = calculate_quality_score(entry)
        entry['quality_score'] = score
        
        if score >= min_score:
            quality_entries.append(entry)
            logger.debug(f"품질 통과: {entry['title'][:50]}... (점수: {score:.1f})")
        else:
            logger.debug(f"품질 미달: {entry['title'][:50]}... (점수: {score:.1f})")
    
    return quality_entries

def get_deterministic_choice(items: List, seed: str) -> any:
    """시드 기반으로 결정적 선택을 수행합니다."""
    if not items:
        return None
    
    # 시드를 해시화하여 인덱스 생성
    hash_obj = hashlib.md5(seed.encode())
    hash_int = int(hash_obj.hexdigest(), 16)
    index = hash_int % len(items)
    
    return items[index]

async def collect_recent_entries(days_back: int = 14) -> Dict[str, List[Dict]]:
    """최근 게시물들을 카테고리별로 수집합니다."""
    logger.info(f"최근 {days_back}일 게시물 수집 시작")
    category_entries = {}
    
    for feed_id, feed_config in AWS_BLOG_FEEDS.items():
        logger.info(f"피드 수집 중: {feed_id}")
        
        # RSS 피드 가져오기
        result = fetch_rss_feed(feed_config["url"])
        
        if result["success"]:
            entries = process_feed_entries(result["feed"], days_back)
            # 품질 필터링 적용
            quality_entries = filter_quality_entries(entries, min_score=1.5)  # 조금 더 관대한 기준
            category_entries[feed_id] = quality_entries
            logger.info(f"{feed_id}: {len(entries)}개 수집 → {len(quality_entries)}개 품질 통과")
        else:
            category_entries[feed_id] = []
            logger.warning(f"{feed_id}: 수집 실패 - {result['error']}")
    
    return category_entries

def select_daily_tip_logic(category_entries: Dict[str, List[Dict]], today_str: str) -> Dict:
    """하이브리드 방식으로 오늘의 팁을 선별합니다."""
    today_date = datetime.strptime(today_str, "%Y-%m-%d").date()
    weekday = today_date.weekday()
    
    # 오늘 요일의 우선순위 카테고리
    priority_categories = WEEKDAY_CATEGORY_PRIORITY[weekday]
    
    selection_metadata = {
        "date": today_str,
        "weekday": weekday,
        "weekday_name": ["월", "화", "수", "목", "금", "토", "일"][weekday],
        "priority_categories": priority_categories,
        "selection_reason": "",
        "backup_used": False,
        "candidate_count": 0,
        "quality_filter_applied": True
    }
    
    # 1차: 우선순위 카테고리에서 선택 시도
    for category in priority_categories:
        if category in category_entries and category_entries[category]:
            entries = category_entries[category]
            selection_metadata["candidate_count"] = len(entries)
            
            # 품질 점수 순으로 정렬 (상위 50%에서 선택)
            entries_sorted = sorted(entries, key=lambda x: x.get('quality_score', 0), reverse=True)
            top_entries = entries_sorted[:max(1, len(entries_sorted) // 2)]
            
            selected = get_deterministic_choice(top_entries, f"{today_str}-{category}")
            if selected:
                selection_metadata["selection_reason"] = f"{selection_metadata['weekday_name']}요일 우선 카테고리 '{AWS_BLOG_FEEDS[category]['name']}'에서 선택"
                selection_metadata["selected_category"] = category
                selection_metadata["category_name"] = AWS_BLOG_FEEDS[category]['name']
                return {"entry": selected, "metadata": selection_metadata}
    
    # 2차: 모든 카테고리에서 백업 선택
    selection_metadata["backup_used"] = True
    all_entries = []
    
    for category, entries in category_entries.items():
        for entry in entries:
            entry['source_category'] = category
            all_entries.append(entry)
    
    if all_entries:
        selection_metadata["candidate_count"] = len(all_entries)
        # 품질 점수 순으로 정렬하여 상위 30%에서 선택
        all_entries_sorted = sorted(all_entries, key=lambda x: x.get('quality_score', 0), reverse=True)
        top_entries = all_entries_sorted[:max(1, len(all_entries_sorted) // 3)]
        
        selected = get_deterministic_choice(top_entries, f"{today_str}-fallback")
        if selected:
            category = selected['source_category']
            selection_metadata["selection_reason"] = f"백업 로직: 전체 카테고리에서 품질 점수 기준 선택 (출처: {AWS_BLOG_FEEDS[category]['name']})"
            selection_metadata["selected_category"] = category
            selection_metadata["category_name"] = AWS_BLOG_FEEDS[category]['name']
            return {"entry": selected, "metadata": selection_metadata}
    
    # 3차: 최종 실패
    selection_metadata["selection_reason"] = "14일 내 적합한 게시물을 찾을 수 없음"
    selection_metadata["error"] = "No suitable entries found in 14 days"
    return {"entry": None, "metadata": selection_metadata}

async def expand_search_range(today_str: str) -> Dict:
    """검색 범위를 확장하여 백업 게시물을 찾습니다."""
    logger.info("30일 범위로 확장 검색 시작")
    
    extended_entries = await collect_recent_entries(days_back=30)
    
    all_entries = []
    for category, entries in extended_entries.items():
        for entry in entries:
            entry['source_category'] = category
            all_entries.append(entry)
    
    if all_entries:
        # 최소 품질 기준도 낮춤
        quality_entries = [e for e in all_entries if e.get('quality_score', 0) >= 1.0]
        if not quality_entries:
            quality_entries = all_entries  # 품질 기준 완전 제거
        
        selected = get_deterministic_choice(quality_entries, f"{today_str}-extended")
        if selected:
            category = selected['source_category']
            metadata = {
                "date": today_str,
                "selection_reason": f"확장 검색 (30일): {AWS_BLOG_FEEDS[category]['name']}에서 선택",
                "backup_used": True,
                "extended_search": True,
                "selected_category": category,
                "category_name": AWS_BLOG_FEEDS[category]['name'],
                "candidate_count": len(quality_entries)
            }
            return {"entry": selected, "metadata": metadata}
    
    # 최종 실패
    return {
        "entry": None,
        "metadata": {
            "date": today_str,
            "selection_reason": "30일 내에도 적합한 게시물을 찾을 수 없음",
            "backup_used": True,
            "extended_search": True,
            "error": "No suitable entries found even in extended search"
        }
    }

# 개발 서버 실행 (프로덕션에서는 사용하지 않음)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 