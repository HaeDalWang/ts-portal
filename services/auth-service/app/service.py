"""
Auth Service - 비즈니스 로직

JWT 토큰 관리, 인증/인가 핵심 비즈니스 로직 구현
"""

import logging
import hashlib
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from .models import Member, UserRole
from .schemas import LoginRequest, TokenResponse, JWTPayload

logger = logging.getLogger(__name__)

# JWT 설정
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "1440"))  # 24시간


class AuthService:
    """인증/인가 서비스"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def hash_password(self, password: str) -> str:
        """비밀번호 해싱"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """비밀번호 검증"""
        return hashlib.sha256(password.encode()).hexdigest() == password_hash
    
    def create_access_token(self, user: Member) -> Dict[str, Any]:
        """
        JWT 액세스 토큰 생성
        
        Args:
            user: 사용자 객체
            
        Returns:
            Dict: 토큰 정보 (token, expires_in, user_info)
        """
        try:
            # 토큰 만료 시간 계산
            expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
            
            # JWT 페이로드 생성
            payload = {
                "user_id": user.id,
                "email": user.email,
                "role": user.role.value,
                "exp": expire,
                "iat": datetime.utcnow()
            }
            
            # JWT 토큰 생성
            token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
            
            return {
                "access_token": token,
                "token_type": "bearer",
                "expires_in": JWT_EXPIRE_MINUTES * 60,  # 초 단위
                "user": user.to_dict()
            }
            
        except Exception as e:
            logger.error(f"토큰 생성 실패: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="토큰 생성 중 오류가 발생했습니다."
            )
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        JWT 토큰 검증
        
        Args:
            token: JWT 토큰
            
        Returns:
            Dict: 토큰 페이로드 또는 None
        """
        try:
            # JWT 토큰 디코딩
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            
            # 사용자 존재 확인
            user = self.get_user_by_id(payload.get("user_id"))
            if not user or not user.is_active:
                return None
            
            return {
                "valid": True,
                "user_id": payload.get("user_id"),
                "email": payload.get("email"),
                "role": payload.get("role"),
                "expires_at": datetime.fromtimestamp(payload.get("exp")),
                "user": user
            }
            
        except ExpiredSignatureError:
            logger.warning("만료된 토큰")
            return {"valid": False, "message": "토큰이 만료되었습니다."}
        except InvalidTokenError as e:
            logger.warning(f"유효하지 않은 토큰: {e}")
            return {"valid": False, "message": "유효하지 않은 토큰입니다."}
        except Exception as e:
            logger.error(f"토큰 검증 실패: {e}")
            return {"valid": False, "message": "토큰 검증 중 오류가 발생했습니다."}
    
    def authenticate_user(self, login_data: LoginRequest) -> Optional[Member]:
        """
        사용자 인증
        
        Args:
            login_data: 로그인 요청 데이터
            
        Returns:
            Member: 인증된 사용자 객체 또는 None
        """
        try:
            # 이메일로 사용자 조회
            user = self.db.query(Member).filter(
                Member.email == login_data.email,
                Member.is_active == True
            ).first()
            
            if not user:
                logger.warning(f"존재하지 않는 사용자: {login_data.email}")
                return None
            
            # 비밀번호 검증
            if not self.verify_password(login_data.password, user.password_hash):
                logger.warning(f"비밀번호 불일치: {login_data.email}")
                return None
            
            # 마지막 로그인 시간 업데이트
            user.last_login = datetime.utcnow()
            self.db.commit()
            
            logger.info(f"사용자 인증 성공: {user.email}")
            return user
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"사용자 인증 실패: {e}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Member]:
        """ID로 사용자 조회"""
        try:
            return self.db.query(Member).filter(
                Member.id == user_id,
                Member.is_active == True
            ).first()
        except Exception as e:
            logger.error(f"사용자 조회 실패: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Member]:
        """이메일로 사용자 조회"""
        try:
            return self.db.query(Member).filter(
                Member.email == email,
                Member.is_active == True
            ).first()
        except Exception as e:
            logger.error(f"사용자 조회 실패: {e}")
            return None
    
    def login(self, login_data: LoginRequest) -> TokenResponse:
        """
        로그인 처리
        
        Args:
            login_data: 로그인 요청 데이터
            
        Returns:
            TokenResponse: 토큰 응답
            
        Raises:
            HTTPException: 인증 실패 시
        """
        # 사용자 인증
        user = self.authenticate_user(login_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 일치하지 않습니다.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # JWT 토큰 생성
        token_data = self.create_access_token(user)
        
        return TokenResponse(**token_data)
    
    def logout(self, token: str) -> bool:
        """
        로그아웃 처리
        
        현재는 단순히 토큰 검증만 수행
        향후 토큰 블랙리스트 기능 추가 가능
        
        Args:
            token: 로그아웃할 토큰
            
        Returns:
            bool: 성공 여부
        """
        try:
            token_data = self.verify_token(token)
            if token_data and token_data.get("valid"):
                logger.info(f"사용자 로그아웃: {token_data.get('email')}")
                return True
            return False
        except Exception as e:
            logger.error(f"로그아웃 처리 실패: {e}")
            return False
    
    def get_current_user_from_token(self, token: str) -> Optional[Member]:
        """
        토큰에서 현재 사용자 정보 추출
        
        Args:
            token: JWT 토큰
            
        Returns:
            Member: 사용자 객체 또는 None
        """
        token_data = self.verify_token(token)
        if token_data and token_data.get("valid"):
            return token_data.get("user")
        return None
    
    def extract_token_from_header(self, authorization: str) -> Optional[str]:
        """
        Authorization 헤더에서 토큰 추출
        
        Args:
            authorization: Authorization 헤더 값 (Bearer <token>)
            
        Returns:
            str: 토큰 또는 None
        """
        if not authorization:
            return None
        
        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                return None
            return token
        except ValueError:
            return None 