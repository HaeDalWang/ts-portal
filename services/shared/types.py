"""
공통 타입 정의 - 모든 마이크로서비스에서 공유

이 파일은 모든 서비스에서 일관성 있게 사용되어야 하는 enum과 타입들을 정의합니다.
변경 시에는 모든 서비스에 영향을 미치므로 신중하게 진행해야 합니다.
"""

import enum
from datetime import datetime
from typing import Optional


class UserRole(str, enum.Enum):
    """
    사용자 권한 레벨 (전체 시스템 공통)
    
    주의: 이 값들은 PostgreSQL enum과 정확히 일치해야 합니다.
    변경 시 다음 작업이 필요합니다:
    1. PostgreSQL enum 타입 변경
    2. 모든 서비스 재배포
    3. 기존 데이터 마이그레이션
    """
    ADMIN = "ADMIN"           # 관리자: 모든 권한
    POWER_USER = "POWER_USER" # 파워유저: 데이터 조회/수정
    USER = "USER"             # 일반유저: 기본 조회만


class NoticePriority(str, enum.Enum):
    """공지사항 우선순위 (Notice Service 전용)"""
    HIGH = "HIGH"       # 높음
    MEDIUM = "MEDIUM"   # 보통
    LOW = "LOW"         # 낮음


class EventType(str, enum.Enum):
    """일정 유형 (Calendar Service 전용)"""
    MEETING = "MEETING"         # 회의
    PERSONAL = "PERSONAL"       # 개인일정
    PROJECT = "PROJECT"         # 프로젝트
    DEADLINE = "DEADLINE"       # 마감일
    HOLIDAY = "HOLIDAY"         # 휴일


class CustomerStatus(str, enum.Enum):
    """고객 상태 (Customer Service 전용)"""
    ACTIVE = "ACTIVE"           # 활성
    INACTIVE = "INACTIVE"       # 비활성
    PENDING = "PENDING"         # 대기중
    SUSPENDED = "SUSPENDED"     # 정지


class AssignmentRole(str, enum.Enum):
    """고객 담당자 역할 (Customer Service 전용)"""
    PRIMARY = "PRIMARY"         # 주담당자
    SECONDARY = "SECONDARY"     # 부담당자
    CONSULTANT = "CONSULTANT"   # 컨설턴트


# 공통 응답 구조
class BaseResponse:
    """기본 API 응답 구조"""
    success: bool
    message: Optional[str] = None
    timestamp: datetime


class PaginationParams:
    """페이지네이션 공통 파라미터"""
    page: int = 1
    size: int = 20
    
    
class PaginationResponse:
    """페이지네이션 공통 응답"""
    total: int
    page: int
    size: int
    pages: int


# 데이터베이스 스키마 정보
DATABASE_SCHEMAS = {
    "auth": "auth_schema",
    "member": "member_schema", 
    "notice": "notice_schema",
    "calendar": "calendar_schema",
    "customer": "customer_schema",
    "feeds": "feeds_schema"
}


# PostgreSQL enum 타입 정보
POSTGRESQL_ENUMS = {
    "userrole": ["ADMIN", "POWER_USER", "USER"],
    "noticepriority": ["HIGH", "MEDIUM", "LOW"],
    "eventtype": ["MEETING", "PERSONAL", "PROJECT", "DEADLINE", "HOLIDAY"],
    "customerstatus": ["ACTIVE", "INACTIVE", "PENDING", "SUSPENDED"],
    "assignmentrole": ["PRIMARY", "SECONDARY", "CONSULTANT"]
}


def validate_enum_consistency():
    """
    Python enum과 PostgreSQL enum의 일관성을 검증하는 함수
    
    개발/테스트 환경에서 호출하여 enum 값들이 일치하는지 확인합니다.
    """
    errors = []
    
    # UserRole 검증
    python_user_roles = [role.value for role in UserRole]
    if python_user_roles != POSTGRESQL_ENUMS["userrole"]:
        errors.append(f"UserRole 불일치: Python={python_user_roles}, PostgreSQL={POSTGRESQL_ENUMS['userrole']}")
    
    # 다른 enum들도 검증...
    
    if errors:
        raise ValueError(f"Enum 일관성 오류: {errors}")
    
    return True 