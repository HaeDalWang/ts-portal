"""
AWS Translate를 사용한 번역 서비스
"""

import re
import logging
from typing import Optional

from ..config import settings

logger = logging.getLogger(__name__)

# AWS Translate 클라이언트 초기화 (선택적)
translate_client = None
if settings.ENABLE_TRANSLATION:
    try:
        import boto3
        translate_client = boto3.client('translate', region_name=settings.AWS_REGION)
        logger.info("AWS Translate 활성화됨")
    except Exception as e:
        logger.warning(f"AWS Translate 초기화 실패: {e}")
        translate_client = None


class TranslationService:
    """번역 서비스"""
    
    @staticmethod
    def is_likely_english(text: str) -> bool:
        """텍스트가 영어일 가능성이 높은지 확인합니다."""
        if not text:
            return False
        
        # ASCII 문자(영어, 숫자, 특수문자)의 비율 계산
        ascii_chars = sum(1 for char in text if ord(char) < 128)
        ascii_ratio = ascii_chars / len(text)
        
        return ascii_ratio >= settings.MIN_ASCII_RATIO_FOR_TRANSLATION
    
    @staticmethod
    def translate_text_to_korean(text: str, max_chars: int = None) -> str:
        """텍스트를 한국어로 번역합니다."""
        if not settings.ENABLE_TRANSLATION or not translate_client or not text.strip():
            return text
        
        # 텍스트 길이 제한
        if max_chars is None:
            max_chars = settings.MAX_TRANSLATION_CHARS
        
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
            logger.info(f"번역 텍스트 길이 제한 적용: {max_chars}자")
        
        # 영어로 보이지 않으면 번역하지 않음
        if not TranslationService.is_likely_english(text):
            logger.debug("영어가 아닌 것으로 판단되어 번역 건너뜀")
            return text
        
        try:
            logger.debug(f"번역 시작: {len(text)}자")
            response = translate_client.translate_text(
                Text=text,
                SourceLanguageCode='auto',
                TargetLanguageCode='ko'
            )
            
            translated_text = response['TranslatedText']
            logger.info("번역 완료")
            return translated_text
            
        except Exception as e:
            logger.warning(f"번역 실패: {e}")
            return text
    
    @staticmethod
    def translate_entry_content(title: str, summary: str) -> tuple[str, str, bool]:
        """엔트리의 제목과 요약을 번역합니다."""
        if not settings.ENABLE_TRANSLATION or not translate_client:
            return title, summary, False
        
        translated = False
        translated_title = title
        translated_summary = summary
        
        try:
            # 제목 번역
            if TranslationService.is_likely_english(title):
                translated_title = TranslationService.translate_text_to_korean(title, 200)
                translated = True
            
            # 요약 번역
            if TranslationService.is_likely_english(summary):
                translated_summary = TranslationService.translate_text_to_korean(summary, 1000)
                translated = True
            
            return translated_title, translated_summary, translated
            
        except Exception as e:
            logger.warning(f"엔트리 번역 실패: {e}")
            return title, summary, False 