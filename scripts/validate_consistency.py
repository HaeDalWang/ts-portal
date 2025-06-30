#!/usr/bin/env python3
"""
TS Portal 시스템 일관성 검증 스크립트

이 스크립트는 다음을 검증합니다:
1. Python enum과 PostgreSQL enum의 일치성
2. 데이터베이스 스키마 존재 여부
3. 서비스별 테이블 생성 설정
4. 공통 타입 사용 여부
"""

import os
import sys
import psycopg2
import importlib.util
from pathlib import Path


def check_database_enums():
    """PostgreSQL enum 타입들을 확인합니다"""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME", "tsportal"),
            user=os.getenv("DB_USER", "tsportal"),
            password=os.getenv("DB_PASSWORD", "tsportal123")
        )
        
        cursor = conn.cursor()
        
        # 모든 enum 타입과 값들 조회
        cursor.execute("""
            SELECT t.typname, e.enumlabel 
            FROM pg_type t 
            JOIN pg_enum e ON t.oid = e.enumtypid
            WHERE t.typname IN ('userrole', 'noticepriority', 'eventtype', 'customerstatus', 'assignmentrole')
            ORDER BY t.typname, e.enumlabel;
        """)
        
        db_enums = {}
        for typname, enumlabel in cursor.fetchall():
            if typname not in db_enums:
                db_enums[typname] = []
            db_enums[typname].append(enumlabel)
        
        cursor.close()
        conn.close()
        
        return db_enums
        
    except Exception as e:
        print(f"❌ 데이터베이스 연결 실패: {e}")
        return None


def check_python_enums():
    """Python enum 정의들을 확인합니다"""
    try:
        # shared/types.py 모듈 로드
        types_path = Path(__file__).parent.parent / "services" / "shared" / "types.py"
        
        if not types_path.exists():
            print(f"❌ 공통 타입 파일이 없습니다: {types_path}")
            return None
        
        spec = importlib.util.spec_from_file_location("shared.types", types_path)
        types_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(types_module)
        
        python_enums = {
            "userrole": [role.value for role in types_module.UserRole],
            "noticepriority": [priority.value for priority in types_module.NoticePriority],
            "eventtype": [event.value for event in types_module.EventType],
            "customerstatus": [status.value for status in types_module.CustomerStatus],
            "assignmentrole": [role.value for role in types_module.AssignmentRole]
        }
        
        return python_enums
        
    except Exception as e:
        print(f"❌ Python enum 로드 실패: {e}")
        return None


def check_service_table_creation():
    """각 서비스의 테이블 생성 설정을 확인합니다"""
    services_dir = Path(__file__).parent.parent / "services"
    issues = []
    
    for service_dir in services_dir.iterdir():
        if not service_dir.is_dir() or service_dir.name == "shared":
            continue
            
        main_py = service_dir / "app" / "main.py"
        if main_py.exists():
            content = main_py.read_text()
            
            # 테이블 자동 생성 코드 확인
            if "Base.metadata.create_all(bind=engine)" in content:
                if service_dir.name != "auth-service":
                    issues.append(f"❌ {service_dir.name}: 테이블 자동 생성이 활성화되어 있습니다")
                else:
                    print(f"✅ {service_dir.name}: 마스터 서비스로 테이블 생성 활성화")
            else:
                if service_dir.name == "auth-service":
                    issues.append(f"❌ {service_dir.name}: 마스터 서비스인데 테이블 생성이 비활성화되어 있습니다")
                else:
                    print(f"✅ {service_dir.name}: 테이블 자동 생성 비활성화")
    
    return issues


def check_common_types_usage():
    """공통 타입 사용 여부를 확인합니다"""
    services_dir = Path(__file__).parent.parent / "services"
    issues = []
    
    for service_dir in services_dir.iterdir():
        if not service_dir.is_dir() or service_dir.name == "shared":
            continue
            
        models_py = service_dir / "app" / "models.py"
        if models_py.exists():
            content = models_py.read_text()
            
            # 개별 enum 정의 확인
            if "class UserRole(str, enum.Enum):" in content:
                issues.append(f"❌ {service_dir.name}: UserRole을 개별 정의하고 있습니다")
            
            # 공통 타입 import 확인
            if "from ..shared.types import" in content:
                print(f"✅ {service_dir.name}: 공통 타입을 사용하고 있습니다")
            elif "UserRole" in content:
                issues.append(f"❌ {service_dir.name}: 공통 타입을 import하지 않고 있습니다")
    
    return issues


def main():
    """메인 검증 함수"""
    print("🔍 TS Portal 시스템 일관성 검증 시작\n")
    
    # 1. 데이터베이스 enum 확인
    print("1️⃣ 데이터베이스 enum 확인...")
    db_enums = check_database_enums()
    if db_enums:
        for enum_name, values in db_enums.items():
            print(f"   📋 {enum_name}: {values}")
    
    # 2. Python enum 확인
    print("\n2️⃣ Python enum 확인...")
    python_enums = check_python_enums()
    if python_enums:
        for enum_name, values in python_enums.items():
            print(f"   📋 {enum_name}: {values}")
    
    # 3. enum 일치성 확인
    print("\n3️⃣ Enum 일치성 확인...")
    if db_enums and python_enums:
        enum_issues = []
        for enum_name in python_enums.keys():
            if enum_name in db_enums:
                if sorted(python_enums[enum_name]) == sorted(db_enums[enum_name]):
                    print(f"   ✅ {enum_name}: 일치")
                else:
                    enum_issues.append(f"❌ {enum_name}: 불일치 - Python={python_enums[enum_name]}, DB={db_enums[enum_name]}")
            else:
                enum_issues.append(f"❌ {enum_name}: 데이터베이스에 enum이 없습니다")
        
        if enum_issues:
            for issue in enum_issues:
                print(f"   {issue}")
    
    # 4. 서비스별 테이블 생성 설정 확인
    print("\n4️⃣ 서비스별 테이블 생성 설정 확인...")
    table_issues = check_service_table_creation()
    for issue in table_issues:
        print(f"   {issue}")
    
    # 5. 공통 타입 사용 확인
    print("\n5️⃣ 공통 타입 사용 확인...")
    type_issues = check_common_types_usage()
    for issue in type_issues:
        print(f"   {issue}")
    
    # 결과 요약
    print("\n📊 검증 결과 요약:")
    total_issues = len(enum_issues if 'enum_issues' in locals() else []) + len(table_issues) + len(type_issues)
    
    if total_issues == 0:
        print("✅ 모든 검증을 통과했습니다!")
        return 0
    else:
        print(f"❌ {total_issues}개의 문제가 발견되었습니다.")
        print("\n🔧 해결 방법:")
        print("1. docs/DEVELOPMENT_GUIDELINES.md 참조")
        print("2. scripts/database_setup.sql 실행")
        print("3. 각 서비스의 models.py에서 공통 타입 사용")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 