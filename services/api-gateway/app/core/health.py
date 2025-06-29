"""헬스체크 모듈"""
import httpx
import asyncio
import logging
from typing import Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

class HealthChecker:
    def __init__(self):
        self.services = settings.SERVICES
        
    async def check_service(self, service_name: str, service_url: str) -> Dict[str, Any]:
        """개별 서비스 헬스체크"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{service_url}/health")
                return {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "response_time": f"{response.elapsed.total_seconds() * 1000:.0f}ms"
                }
        except Exception as e:
            logger.error(f"{service_name} 헬스체크 실패: {e}")
            return {"status": "unhealthy", "error": str(e)}
    
    async def check_all_services(self) -> Dict[str, Any]:
        """모든 서비스 헬스체크"""
        tasks = [
            self.check_service(name, url) 
            for name, url in self.services.items()
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        service_status = {}
        for (name, _), result in zip(self.services.items(), results):
            if isinstance(result, Exception):
                service_status[name] = {"status": "unhealthy", "error": str(result)}
            else:
                service_status[name] = result
        
        return {"services": service_status}
    
    async def start(self):
        """헬스체커 시작"""
        logger.info("헬스체커 시작됨")
    
    async def stop(self):
        """헬스체커 중지"""
        logger.info("헬스체커 중지됨")

# 글로벌 헬스체커 인스턴스
health_checker = HealthChecker() 