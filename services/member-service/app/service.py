"""
Member Service - 비즈니스 로직

팀원 관리 핵심 비즈니스 로직 구현
"""

import logging
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, text
from fastapi import HTTPException, status

from .models import Member, UserRole
from .schemas import (
    MemberCreate, MemberUpdate, PasswordChange, RoleChange,
    MemberFilter, MemberStats
)

logger = logging.getLogger(__name__)


class MemberService:
    """멤버 관리 서비스"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def hash_password(self, password: str) -> str:
        """비밀번호 해싱"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """비밀번호 검증"""
        return hashlib.sha256(password.encode()).hexdigest() == password_hash
    
    def create_member(self, member_data: MemberCreate) -> Member:
        """
        새 멤버 생성
        
        Args:
            member_data: 멤버 생성 데이터
            
        Returns:
            Member: 생성된 멤버 객체
            
        Raises:
            HTTPException: 이메일 중복 시
        """
        try:
            # 이메일 중복 확인
            existing_member = self.db.query(Member).filter(
                Member.email == member_data.email
            ).first()
            
            if existing_member:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="이미 존재하는 이메일입니다."
                )
            
            # 비밀번호 해싱
            password_hash = self.hash_password(member_data.password)
            
            # 멤버 객체 생성
            db_member = Member(
                name=member_data.name,
                email=member_data.email,
                phone=member_data.phone,
                password_hash=password_hash,
                role=member_data.role,
                position=member_data.position,
                team=member_data.team,
                skills=member_data.skills,
                join_date=member_data.join_date,
                profile_image=member_data.profile_image,
                is_active=member_data.is_active
            )
            
            self.db.add(db_member)
            self.db.commit()
            self.db.refresh(db_member)
            
            logger.info(f"새 멤버 생성 완료: {db_member.email}")
            return db_member
            
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"멤버 생성 실패: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="멤버 생성 중 오류가 발생했습니다."
            )
    
    def get_member_by_id(self, member_id: int) -> Optional[Member]:
        """ID로 멤버 조회"""
        return self.db.query(Member).filter(Member.id == member_id).first()
    
    def get_member_by_email(self, email: str) -> Optional[Member]:
        """이메일로 멤버 조회"""
        return self.db.query(Member).filter(Member.email == email).first()
    
    def get_members(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[MemberFilter] = None
    ) -> tuple[List[Member], int]:
        """
        멤버 목록 조회 (필터링 및 페이지네이션)
        
        Args:
            skip: 건너뛸 개수
            limit: 조회할 개수
            filters: 검색 필터
            
        Returns:
            tuple: (멤버 리스트, 전체 개수)
        """
        query = self.db.query(Member)
        
        # 필터 적용
        if filters:
            if filters.name:
                query = query.filter(Member.name.ilike(f"%{filters.name}%"))
            if filters.email:
                query = query.filter(Member.email.ilike(f"%{filters.email}%"))
            if filters.team:
                query = query.filter(Member.team == filters.team)
            if filters.position:
                query = query.filter(Member.position.ilike(f"%{filters.position}%"))
            if filters.role:
                query = query.filter(Member.role == filters.role)
            if filters.is_active is not None:
                query = query.filter(Member.is_active == filters.is_active)
            if filters.skills:
                query = query.filter(Member.skills.ilike(f"%{filters.skills}%"))
        
        # 전체 개수 조회
        total = query.count()
        
        # 페이지네이션 적용하여 결과 조회
        members = query.order_by(Member.created_at.desc()).offset(skip).limit(limit).all()
        
        return members, total
    
    def update_member(self, member_id: int, member_data: MemberUpdate) -> Optional[Member]:
        """
        멤버 정보 업데이트
        
        Args:
            member_id: 멤버 ID
            member_data: 업데이트할 데이터
            
        Returns:
            Member: 업데이트된 멤버 객체
        """
        try:
            db_member = self.get_member_by_id(member_id)
            if not db_member:
                return None
            
            # 변경된 필드만 업데이트
            update_data = member_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_member, field, value)
            
            db_member.updated_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(db_member)
            
            logger.info(f"멤버 정보 업데이트 완료: {db_member.email}")
            return db_member
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"멤버 업데이트 실패: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="멤버 정보 업데이트 중 오류가 발생했습니다."
            )
    
    def change_password(self, member_id: int, password_data: PasswordChange) -> bool:
        """
        비밀번호 변경
        
        Args:
            member_id: 멤버 ID
            password_data: 비밀번호 변경 데이터
            
        Returns:
            bool: 성공 여부
        """
        try:
            db_member = self.get_member_by_id(member_id)
            if not db_member:
                return False
            
            # 현재 비밀번호 확인
            if not self.verify_password(password_data.current_password, db_member.password_hash):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="현재 비밀번호가 일치하지 않습니다."
                )
            
            # 새 비밀번호 해싱 및 저장
            db_member.password_hash = self.hash_password(password_data.new_password)
            db_member.updated_at = datetime.utcnow()
            
            self.db.commit()
            
            logger.info(f"비밀번호 변경 완료: {db_member.email}")
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"비밀번호 변경 실패: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="비밀번호 변경 중 오류가 발생했습니다."
            )
    
    def change_role(self, member_id: int, role_data: RoleChange) -> Optional[Member]:
        """
        멤버 권한 변경 (관리자만)
        
        Args:
            member_id: 멤버 ID
            role_data: 권한 변경 데이터
            
        Returns:
            Member: 업데이트된 멤버 객체
        """
        try:
            db_member = self.get_member_by_id(member_id)
            if not db_member:
                return None
            
            db_member.role = role_data.role
            db_member.updated_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(db_member)
            
            logger.info(f"멤버 권한 변경 완료: {db_member.email} -> {role_data.role}")
            return db_member
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"권한 변경 실패: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="권한 변경 중 오류가 발생했습니다."
            )
    
    def delete_member(self, member_id: int) -> bool:
        """
        멤버 삭제 (비활성화)
        
        Args:
            member_id: 멤버 ID
            
        Returns:
            bool: 성공 여부
        """
        try:
            db_member = self.get_member_by_id(member_id)
            if not db_member:
                return False
            
            # 실제 삭제 대신 비활성화
            db_member.is_active = False
            db_member.updated_at = datetime.utcnow()
            
            self.db.commit()
            
            logger.info(f"멤버 비활성화 완료: {db_member.email}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"멤버 삭제 실패: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="멤버 삭제 중 오류가 발생했습니다."
            )
    
    def update_last_login(self, member_id: int) -> bool:
        """
        마지막 로그인 시간 업데이트
        
        Args:
            member_id: 멤버 ID
            
        Returns:
            bool: 성공 여부
        """
        try:
            db_member = self.get_member_by_id(member_id)
            if not db_member:
                return False
            
            db_member.last_login = datetime.utcnow()
            self.db.commit()
            
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"로그인 시간 업데이트 실패: {e}")
            return False
    
    def get_all_skills(self) -> List[str]:
        """모든 기술 목록 조회"""
        try:
            skills_data = self.db.query(Member.skills).filter(
                Member.skills.isnot(None),
                Member.is_active == True
            ).all()
            
            all_skills = set()
            for (skills_str,) in skills_data:
                if skills_str:
                    skills = [skill.strip() for skill in skills_str.split(",") if skill.strip()]
                    all_skills.update(skills)
            
            return sorted(list(all_skills))
            
        except Exception as e:
            logger.error(f"기술 목록 조회 실패: {e}")
            return []
    
    def get_member_stats(self) -> MemberStats:
        """멤버 통계 조회"""
        try:
            # 기본 통계
            total_members = self.db.query(Member).count()
            active_members = self.db.query(Member).filter(Member.is_active == True).count()
            inactive_members = total_members - active_members
            
            # 팀별 통계
            team_stats = self.db.query(
                Member.team,
                func.count(Member.id)
            ).filter(Member.is_active == True).group_by(Member.team).all()
            by_team = {team: count for team, count in team_stats}
            
            # 권한별 통계
            role_stats = self.db.query(
                Member.role,
                func.count(Member.id)
            ).filter(Member.is_active == True).group_by(Member.role).all()
            by_role = {role.value: count for role, count in role_stats}
            
            # 직급별 통계
            position_stats = self.db.query(
                Member.position,
                func.count(Member.id)
            ).filter(
                Member.is_active == True,
                Member.position.isnot(None)
            ).group_by(Member.position).all()
            by_position = {position: count for position, count in position_stats}
            
            # 최근 7일 로그인 수
            week_ago = datetime.utcnow() - timedelta(days=7)
            recent_logins = self.db.query(Member).filter(
                Member.last_login >= week_ago
            ).count()
            
            return MemberStats(
                total_members=total_members,
                active_members=active_members,
                inactive_members=inactive_members,
                by_team=by_team,
                by_role=by_role,
                by_position=by_position,
                recent_logins=recent_logins
            )
            
        except Exception as e:
            logger.error(f"멤버 통계 조회 실패: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="통계 조회 중 오류가 발생했습니다."
            ) 