"""서비스 레지스트리 모듈"""
import logging
from typing import Dict, List
from app.core.config import settings

logger = logging.getLogger(__name__)

class ServiceRegistry:
    def __init__(self):
        self.services: Dict[str, str] = {}
        
    async def initialize(self):
        """서비스 레지스트리 초기화"""
        self.services = settings.SERVICES.copy()
        logger.info(f"서비스 레지스트리 초기화 완료: {list(self.services.keys())}")
        
    async def cleanup(self):
        """서비스 레지스트리 정리"""
        logger.info("서비스 레지스트리 정리 완료")
        
    def get_service_url(self, service_name: str) -> str:
        """서비스 URL 가져오기"""
        return self.services.get(service_name, "")
        
    def get_all_services(self) -> Dict[str, str]:
        """모든 서비스 목록 가져오기"""
        return self.services.copy()

# 글로벌 서비스 레지스트리 인스턴스
service_registry = ServiceRegistry() 