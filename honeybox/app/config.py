"""
애플리케이션 설정 관리
"""

import os
from typing import Dict, List


class Settings:
    """애플리케이션 설정 클래스"""
    
    # 앱 기본 정보
    APP_NAME: str = "HoneyBox - AWS 소식 RSS 수집기"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "AWS 블로그들의 RSS를 수집하여 매일 하나씩 선별해서 보여주는 API"
    
    # 번역 기능 설정
    ENABLE_TRANSLATION: bool = os.getenv("ENABLE_TRANSLATION", "false").lower() == "true"
    AWS_REGION: str = os.getenv("AWS_REGION", "ap-northeast-2")
    
    # AWS 블로그 RSS 피드 설정
    AWS_BLOG_FEEDS: Dict[str, Dict[str, str]] = {
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
    
    # 요일별 카테고리 우선순위 설정
    WEEKDAY_CATEGORY_PRIORITY: Dict[int, List[str]] = {
        0: ["aws-korea", "aws-architecture", "aws-news"],      # 월요일
        1: ["aws-korea", "aws-security", "aws-devops"],        # 화요일
        2: ["aws-korea", "aws-devops", "aws-opensource"],      # 수요일
        3: ["aws-korea", "aws-news", "aws-whats-new"],         # 목요일
        4: ["aws-korea", "aws-architecture", "aws-security"],  # 금요일
        5: ["aws-korea", "aws-opensource", "aws-news"],        # 토요일
        6: ["aws-korea", "aws-whats-new", "aws-devops"]        # 일요일
    }
    
    # RSS 처리 설정
    RSS_REQUEST_TIMEOUT: int = 30
    MAX_ENTRIES_PER_FEED: int = 20
    DEFAULT_DAYS_BACK: int = 7
    EXTENDED_DAYS_BACK: int = 30
    
    # 품질 평가 설정
    MIN_QUALITY_SCORE: float = 1.5
    EXTENDED_MIN_QUALITY_SCORE: float = 1.0
    
    # 번역 설정
    MAX_TRANSLATION_CHARS: int = 5000
    MIN_ASCII_RATIO_FOR_TRANSLATION: float = 0.7


# 싱글톤 설정 인스턴스
settings = Settings() 