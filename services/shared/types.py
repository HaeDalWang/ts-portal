"""
Shared types for TS Portal services

공통으로 사용되는 enum 타입들을 정의합니다.
"""

import enum


class UserRole(str, enum.Enum):
    """사용자 권한 레벨 (PostgreSQL enum과 일치)"""
    ADMIN = "ADMIN"           # 관리자: 모든 권한
    POWER_USER = "POWER_USER" # 파워유저: 데이터 조회/수정
    USER = "USER"             # 일반유저: 기본 조회만


# 권한 계층 구조 (권한 확인용)
ROLE_HIERARCHY = {
    UserRole.USER: 0,
    UserRole.POWER_USER: 1,
    UserRole.ADMIN: 2
}


def has_permission(user_role: UserRole, required_role: UserRole) -> bool:
    """권한 확인 유틸리티 함수"""
    return ROLE_HIERARCHY.get(user_role, 0) >= ROLE_HIERARCHY.get(required_role, 0)


def is_admin(user_role: UserRole) -> bool:
    """관리자 권한 확인"""
    return user_role == UserRole.ADMIN


def is_power_user_or_above(user_role: UserRole) -> bool:
    """파워유저 이상 권한 확인"""
    return user_role in [UserRole.POWER_USER, UserRole.ADMIN] 