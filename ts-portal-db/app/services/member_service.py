"""
팀원 관련 서비스 레이어
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from ..models.member import Member
from ..schemas.member import MemberCreate, MemberUpdate


class MemberService:
    """팀원 관련 비즈니스 로직"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_member(self, member_id: int) -> Optional[Member]:
        """팀원 단일 조회"""
        return self.db.query(Member).filter(Member.id == member_id).first()
    
    def get_member_by_email(self, email: str) -> Optional[Member]:
        """이메일로 팀원 조회"""
        return self.db.query(Member).filter(Member.email == email).first()
    
    def get_members(self, skip: int = 0, limit: int = 100, active_only: bool = False) -> List[Member]:
        """팀원 목록 조회"""
        query = self.db.query(Member)
        
        if active_only:
            query = query.filter(Member.is_active == True)
        
        return query.offset(skip).limit(limit).all()
    
    def get_members_count(self, active_only: bool = False) -> int:
        """팀원 총 개수"""
        query = self.db.query(Member)
        
        if active_only:
            query = query.filter(Member.is_active == True)
        
        return query.count()
    
    def create_member(self, member_data: MemberCreate) -> Member:
        """팀원 생성"""
        # 이메일 중복 체크
        existing_member = self.get_member_by_email(member_data.email)
        if existing_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"이메일 '{member_data.email}'은 이미 사용 중입니다."
            )
        
        try:
            # 새 팀원 생성
            db_member = Member(**member_data.model_dump())
            self.db.add(db_member)
            self.db.commit()
            self.db.refresh(db_member)
            return db_member
        
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="팀원 생성 중 데이터 무결성 오류가 발생했습니다."
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="팀원 생성 중 오류가 발생했습니다."
            )
    
    def update_member(self, member_id: int, member_data: MemberUpdate) -> Optional[Member]:
        """팀원 정보 수정"""
        db_member = self.get_member(member_id)
        if not db_member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ID {member_id}인 팀원을 찾을 수 없습니다."
            )
        
        # 이메일 중복 체크 (본인 제외)
        if member_data.email:
            existing_member = self.get_member_by_email(member_data.email)
            if existing_member and existing_member.id != member_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"이메일 '{member_data.email}'은 이미 사용 중입니다."
                )
        
        try:
            # 수정할 필드만 업데이트
            update_data = member_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_member, field, value)
            
            self.db.commit()
            self.db.refresh(db_member)
            return db_member
        
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="팀원 정보 수정 중 데이터 무결성 오류가 발생했습니다."
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="팀원 정보 수정 중 오류가 발생했습니다."
            )
    
    def delete_member(self, member_id: int) -> bool:
        """팀원 삭제 (소프트 삭제 - is_active를 False로 변경)"""
        db_member = self.get_member(member_id)
        if not db_member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ID {member_id}인 팀원을 찾을 수 없습니다."
            )
        
        try:
            # 소프트 삭제 (is_active = False)
            db_member.is_active = False
            self.db.commit()
            return True
        
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="팀원 삭제 중 오류가 발생했습니다."
            )
    
    def restore_member(self, member_id: int) -> Optional[Member]:
        """팀원 복구 (is_active를 True로 변경)"""
        db_member = self.get_member(member_id)
        if not db_member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ID {member_id}인 팀원을 찾을 수 없습니다."
            )
        
        try:
            db_member.is_active = True
            self.db.commit()
            self.db.refresh(db_member)
            return db_member
        
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="팀원 복구 중 오류가 발생했습니다."
            )
    
    def search_members(self, query: str, active_only: bool = False) -> List[Member]:
        """팀원 검색 (이름, 이메일, 직급으로 검색)"""
        db_query = self.db.query(Member)
        
        if active_only:
            db_query = db_query.filter(Member.is_active == True)
        
        # 이름, 이메일, 직급에서 검색
        search_filter = (
            Member.name.contains(query) |
            Member.email.contains(query) |
            Member.position.contains(query)
        )
        
        return db_query.filter(search_filter).all() 