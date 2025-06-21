"""
인증 및 권한 관련 서비스
"""

import os
from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..models.member import Member, UserRole
from ..schemas.member import LoginRequest, CurrentUser
from ..database import get_db

# HTTP Bearer 토큰 스키마
security = HTTPBearer()


class AuthService:
    """인증 관련 서비스"""
    
    def __init__(self):
        # 비밀번호 해싱 설정
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # JWT 설정
        self.secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = int(os.getenv("JWT_EXPIRE_MINUTES", "1440"))  # 24시간
    
    def hash_password(self, password: str) -> str:
        """비밀번호 해싱"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """비밀번호 검증"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def authenticate_user(self, db: Session, email: str, password: str) -> dict:
        """사용자 인증 및 토큰 생성"""
        user = db.query(Member).filter(
            Member.email == email,
            Member.is_active == True
        ).first()
        
        if not user or not user.password_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다."
            )
        
        if not self.verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다."
            )
        
        # 마지막 로그인 시간 업데이트
        user.last_login = datetime.utcnow()
        db.commit()
        
        # 토큰 생성
        access_token = self.create_access_token(user)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "team": user.team,
                "phone": user.phone,
                "position": user.position,
                "skills": user.skills,
                "join_date": user.join_date.isoformat() if user.join_date else None,
                "profile_image": user.profile_image,
                "is_active": user.is_active,
                "last_login": user.last_login.isoformat() if user.last_login else None,
                "mfa_enabled": user.mfa_enabled,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None,
                "skills_list": user.skills_list
            }
        }
    
    def create_access_token(self, user: Member) -> str:
        """JWT 액세스 토큰 생성"""
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        payload = {
            "sub": str(user.id),  # subject (사용자 ID)
            "email": user.email,
            "name": user.name,
            "role": user.role.value if hasattr(user.role, 'value') else user.role,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str, db: Session) -> Optional[Member]:
        """JWT 토큰 검증 및 사용자 정보 추출"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # 토큰 타입 확인
            if payload.get("type") != "access":
                return None
            
            # 사용자 정보 추출
            user_id = int(payload.get("sub"))
            email = payload.get("email")
            
            if not all([user_id, email]):
                return None
            
            # 데이터베이스에서 사용자 활성 상태 확인
            user = db.query(Member).filter(
                Member.id == user_id,
                Member.email == email,
                Member.is_active == True
            ).first()
            
            return user
            
        except jwt.ExpiredSignatureError:
            return None
        except jwt.JWTError:
            return None
        except Exception:
            return None
    
    def change_password(self, user_id: int, current_password: str, new_password: str, db: Session) -> bool:
        """비밀번호 변경"""
        user = db.query(Member).filter(Member.id == user_id).first()
        
        if not user or not user.password_hash:
            return False
        
        # 현재 비밀번호 확인
        if not self.verify_password(current_password, user.password_hash):
            return False
        
        # 새 비밀번호 설정
        user.password_hash = self.hash_password(new_password)
        db.commit()
        
        return True
    
    def set_user_password(self, user_id: int, password: str, db: Session) -> bool:
        """사용자 비밀번호 설정 (관리자용)"""
        user = db.query(Member).filter(Member.id == user_id).first()
        
        if not user:
            return False
        
        user.password_hash = self.hash_password(password)
        db.commit()
        
        return True
    
    def update_user_role(self, user_id: int, new_role: UserRole, db: Session) -> bool:
        """사용자 권한 변경 (관리자용)"""
        user = db.query(Member).filter(Member.id == user_id).first()
        
        if not user:
            return False
        
        user.role = new_role
        db.commit()
        
        return True
    
    def get_user_by_id(self, user_id: int, db: Session) -> Optional[Member]:
        """사용자 ID로 조회"""
        return db.query(Member).filter(
            Member.id == user_id,
            Member.is_active == True
        ).first()
    
    def create_default_admin(self, email: str, password: str, name: str, db: Session) -> Member:
        """기본 관리자 계정 생성"""
        # 이미 존재하는지 확인
        existing_user = db.query(Member).filter(Member.email == email).first()
        if existing_user:
            return existing_user
        
        # 새 관리자 생성
        admin_user = Member(
            name=name,
            email=email,
            password_hash=self.hash_password(password),
            role=UserRole.ADMIN,
            team="TS팀",
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        return admin_user


# 인증 서비스 인스턴스
auth_service = AuthService()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Member:
    """현재 로그인한 사용자 정보 가져오기"""
    token = credentials.credentials
    user = auth_service.verify_token(token, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_active_user(current_user: Member = Depends(get_current_user)) -> Member:
    """활성 사용자만 허용"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="비활성화된 사용자입니다"
        )
    return current_user


# 권한별 의존성 함수들
async def require_admin(current_user: Member = Depends(get_current_user)) -> Member:
    """관리자 권한 필요"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="관리자 권한이 필요합니다"
        )
    return current_user


async def require_power_user_or_admin(current_user: Member = Depends(get_current_user)) -> Member:
    """파워유저 이상 권한 필요"""
    if current_user.role not in [UserRole.POWER_USER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="파워유저 이상 권한이 필요합니다"
        )
    return current_user


async def require_authenticated(current_user: Member = Depends(get_current_user)) -> Member:
    """로그인한 사용자만 허용"""
    return current_user


def can_edit_member(current_user: Member, target_member_id: int) -> bool:
    """팀원 정보 수정 권한 체크"""
    # 관리자는 모든 팀원 수정 가능
    if current_user.role == UserRole.ADMIN:
        return True
    
    # 파워유저는 모든 팀원 수정 가능 (단, 삭제는 불가)
    if current_user.role == UserRole.POWER_USER:
        return True
    
    # 일반 사용자는 자신의 프로필만 수정 가능
    if current_user.role == UserRole.USER:
        return current_user.id == target_member_id
    
    return False


def can_delete_member(current_user: Member, target_member_id: int) -> bool:
    """팀원 삭제 권한 체크"""
    # 관리자만 삭제 가능
    if current_user.role != UserRole.ADMIN:
        return False
    
    # 자기 자신은 삭제 불가
    if current_user.id == target_member_id:
        return False
    
    return True


def can_create_notice(current_user: Member, priority: str = 'normal') -> bool:
    """공지사항 생성 권한 체크"""
    # 관리자와 파워유저는 모든 우선순위 공지 생성 가능
    if current_user.role in [UserRole.ADMIN, UserRole.POWER_USER]:
        return True
    
    # 일반 사용자는 일반 우선순위만 생성 가능
    if current_user.role == UserRole.USER:
        return priority == 'normal'
    
    return False


def can_manage_customers(current_user: Member) -> bool:
    """고객사 관리 권한 체크 (모든 사용자 가능)"""
    return current_user.is_active


def get_allowed_member_fields_for_update(current_user: Member, target_member_id: int) -> list:
    """사용자별 수정 가능한 필드 목록 반환"""
    # 관리자는 모든 필드 수정 가능
    if current_user.role == UserRole.ADMIN:
        return ['name', 'email', 'phone', 'position', 'team', 'skills', 'join_date', 'profile_image', 'is_active', 'role']
    
    # 파워유저는 권한 변경 제외하고 모든 필드 수정 가능
    if current_user.role == UserRole.POWER_USER:
        return ['name', 'email', 'phone', 'position', 'team', 'skills', 'join_date', 'profile_image', 'is_active']
    
    # 일반 사용자는 자신의 기본 정보만 수정 가능
    if current_user.role == UserRole.USER and current_user.id == target_member_id:
        return ['email', 'phone', 'skills', 'profile_image']
    
    return []