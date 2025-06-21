#!/usr/bin/env python3
"""
인증 시스템 초기화 스크립트
- 데이터베이스 테이블 업데이트
- 기본 관리자 계정 생성
- 기존 멤버들에 대한 기본 권한 설정
"""

import os
import sys
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 현재 스크립트의 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from app.database import Base, SQLALCHEMY_DATABASE_URL
from app.models.member import Member, UserRole
from app.services.auth_service import AuthService


def init_auth_system():
    """인증 시스템 초기화"""
    print("🚀 TS Portal 인증 시스템 초기화 시작...")
    
    # 데이터베이스 연결
    database_url = SQLALCHEMY_DATABASE_URL
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # 테이블 생성/업데이트
    print("📊 데이터베이스 테이블 업데이트 중...")
    Base.metadata.create_all(bind=engine)
    print("✅ 데이터베이스 테이블 업데이트 완료")
    
    # 세션 생성
    db = SessionLocal()
    auth_service = AuthService(db)
    
    try:
        # 1. 기존 멤버들의 권한 설정
        print("👥 기존 멤버들의 권한 설정 중...")
        members = db.query(Member).all()
        
        for member in members:
            if member.role is None:
                # 기본 권한을 USER로 설정
                member.role = UserRole.USER
                print(f"  - {member.name} ({member.email}): USER 권한 설정")
        
        db.commit()
        print(f"✅ {len(members)}명의 멤버 권한 설정 완료")
        
        # 2. 기본 관리자 계정 생성
        print("🔑 기본 관리자 계정 설정 중...")
        
        # 관리자 계정 정보 (환경변수 또는 기본값 사용)
        admin_email = os.getenv("ADMIN_EMAIL", "admin@saltware.co.kr")
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123!")
        admin_name = os.getenv("ADMIN_NAME", "관리자")
        
        # 관리자 계정 생성 또는 업데이트
        admin_user = db.query(Member).filter(Member.email == admin_email).first()
        
        if admin_user:
            # 기존 계정이 있으면 관리자 권한으로 업데이트
            admin_user.role = UserRole.ADMIN
            if not admin_user.password_hash:
                admin_user.password_hash = auth_service.hash_password(admin_password)
            print(f"  - 기존 계정 업데이트: {admin_user.name} ({admin_user.email})")
        else:
            # 새 관리자 계정 생성
            admin_user = auth_service.create_default_admin(
                email=admin_email,
                password=admin_password,
                name=admin_name
            )
            print(f"  - 새 관리자 계정 생성: {admin_user.name} ({admin_user.email})")
        
        db.commit()
        print("✅ 관리자 계정 설정 완료")
        
        # 3. 권한별 통계 출력
        print("\n📊 권한별 멤버 통계:")
        for role in UserRole:
            count = db.query(Member).filter(Member.role == role, Member.is_active == True).count()
            print(f"  - {role.value}: {count}명")
        
        print(f"\n🎉 인증 시스템 초기화 완료!")
        print(f"📝 관리자 로그인 정보:")
        print(f"   이메일: {admin_email}")
        print(f"   비밀번호: {admin_password}")
        print(f"⚠️  보안을 위해 초기 비밀번호를 변경해주세요!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_auth_system() 