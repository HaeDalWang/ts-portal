"""Prometheus 메트릭 모듈"""
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time

# 메트릭 정의
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
ACTIVE_REQUESTS = Gauge('http_requests_in_progress', 'Active HTTP requests')
SERVICE_HEALTH = Gauge('service_health_status', 'Service health status', ['service'])

def generate_metrics():
    """Prometheus 메트릭 생성"""
    return generate_latest() 