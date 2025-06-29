"""
TS Portal Feeds Service
======================

AWS 소식 수집 마이크로서비스 (경량화 버전)
"""

import logging
from datetime import datetime
from typing import List, Dict, Any
import feedparser
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="TS Portal Feeds Service",
    version="0.1.0",
    description="AWS 소식 수집 마이크로서비스",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📰 AWS 피드 목록 (경량화)
AWS_FEEDS = {
    "aws-blog": {
        "name": "AWS Blog",
        "url": "https://aws.amazon.com/blogs/feed/",
        "description": "AWS 공식 블로그"
    },
    "aws-news": {
        "name": "AWS What's New",
        "url": "https://aws.amazon.com/about-aws/whats-new/recent/feed/",
        "description": "AWS 최신 소식"
    },
    "aws-security": {
        "name": "AWS Security Blog", 
        "url": "https://aws.amazon.com/blogs/security/feed/",
        "description": "AWS 보안 블로그"
    }
}


async def fetch_feed(feed_url: str, limit: int = 10) -> List[Dict[str, Any]]:
    """RSS 피드를 가져와서 파싱합니다."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(feed_url)
            response.raise_for_status()
            
        # feedparser로 RSS 파싱
        feed = feedparser.parse(response.content)
        
        items = []
        for entry in feed.entries[:limit]:
            items.append({
                "title": entry.get("title", "제목 없음"),
                "link": entry.get("link", ""),
                "summary": entry.get("summary", "요약 없음")[:200] + "...",
                "published": entry.get("published", ""),
                "author": entry.get("author", "AWS")
            })
        
        return items
        
    except Exception as e:
        logger.error(f"피드 가져오기 실패 {feed_url}: {e}")
        return []


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "service": "TS Portal Feeds Service",
        "version": "0.1.0",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "feeds_count": len(AWS_FEEDS),
        "endpoints": {
            "/feeds": "사용 가능한 피드 목록",
            "/feeds/all": "모든 피드 최신 소식",
            "/feeds/{feed_id}": "특정 피드 조회",
            "/health": "헬스체크"
        }
    }


@app.get("/health")
async def health_check():
    """헬스체크 엔드포인트"""
    return {
        "status": "healthy",
        "service": "feeds-service",
        "timestamp": datetime.now().isoformat(),
        "feeds_available": len(AWS_FEEDS)
    }


@app.get("/feeds")
async def get_feeds():
    """사용 가능한 피드 목록을 반환합니다."""
    return {
        "feeds": AWS_FEEDS,
        "total": len(AWS_FEEDS)
    }


@app.get("/feeds/all")
async def get_all_feeds(limit: int = 5):
    """모든 피드에서 최신 소식을 가져옵니다."""
    all_items = []
    
    for feed_id, feed_info in AWS_FEEDS.items():
        logger.info(f"피드 수집 중: {feed_info['name']}")
        items = await fetch_feed(feed_info["url"], limit)
        
        for item in items:
            item["feed_id"] = feed_id
            item["feed_name"] = feed_info["name"]
            
        all_items.extend(items)
    
    # 최신순 정렬 (간단히 제목 기준)
    all_items.sort(key=lambda x: x.get("published", ""), reverse=True)
    
    return {
        "items": all_items[:limit * len(AWS_FEEDS)],
        "total": len(all_items),
        "timestamp": datetime.now().isoformat()
    }


@app.get("/feeds/{feed_id}")
async def get_feed(feed_id: str, limit: int = 10):
    """특정 피드의 최신 소식을 가져옵니다."""
    if feed_id not in AWS_FEEDS:
        raise HTTPException(status_code=404, detail=f"피드를 찾을 수 없습니다: {feed_id}")
    
    feed_info = AWS_FEEDS[feed_id]
    items = await fetch_feed(feed_info["url"], limit)
    
    return {
        "feed_id": feed_id,
        "feed_name": feed_info["name"],
        "description": feed_info["description"],
        "items": items,
        "total": len(items),
        "timestamp": datetime.now().isoformat()
    }


@app.get("/feeds/latest")
async def get_latest_news(limit: int = 3):
    """오늘의 AWS 소식 (가장 간단한 버전)"""
    items = await fetch_feed(AWS_FEEDS["aws-news"]["url"], limit)
    
    return {
        "latest_news": items,
        "total": len(items),
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 