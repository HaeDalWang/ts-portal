"""
캐싱 관리 유틸리티
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class CacheManager:
    """메모리 기반 캐시 관리자"""
    
    def __init__(self):
        self._cache: Dict[str, Any] = {}
        
    def get(self, key: str) -> Optional[Any]:
        """캐시에서 값을 가져옵니다."""
        return self._cache.get(key)
    
    def set(self, key: str, value: Any) -> None:
        """캐시에 값을 저장합니다."""
        self._cache[key] = value
        
    def delete(self, key: str) -> bool:
        """캐시에서 키를 제거합니다."""
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    def clear_old_entries(self, current_date: str) -> None:
        """현재 날짜보다 오래된 캐시 엔트리들을 정리합니다."""
        keys_to_remove = []
        
        for key in self._cache.keys():
            # 키가 날짜 형식을 포함하는 경우 (예: "2025-06-03" 또는 "2025-06-03_translated")
            cache_date = key.split('_')[0]
            if cache_date < current_date:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            self.delete(key)
            logger.debug(f"오래된 캐시 엔트리 제거: {key}")
        
        if keys_to_remove:
            logger.info(f"캐시 정리 완료: {len(keys_to_remove)}개 엔트리 제거")
    
    def get_cache_info(self) -> Dict[str, Any]:
        """캐시 상태 정보를 반환합니다."""
        return {
            "total_entries": len(self._cache),
            "keys": list(self._cache.keys())
        }


# 싱글톤 캐시 인스턴스
daily_tip_cache = CacheManager() 