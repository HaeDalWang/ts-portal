#!/usr/bin/env python3
"""
TS Portal 시스템 일관성 검증 스크립트 (간단 버전)

psycopg2 없이 파일 기반으로 검증합니다.
"""

import sys
from pathlib import Path


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
            if "Base.metadata.create_all(bind=engine)" in content and "# Base.metadata.create_all" not in content:
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


def check_file_structure():
    """필수 파일들의 존재 여부를 확인합니다"""
    base_dir = Path(__file__).parent.parent
    required_files = [
        "scripts/database_setup.sql",
        "docs/DEVELOPMENT_GUIDELINES.md"
    ]
    
    issues = []
    for file_path in required_files:
        full_path = base_dir / file_path
        if full_path.exists():
            print(f"✅ {file_path}: 존재")
        else:
            issues.append(f"❌ {file_path}: 없음")
    
    return issues


def main():
    """메인 검증 함수"""
    print("🔍 TS Portal 시스템 일관성 검증 시작 (간단 버전)\n")
    
    # 1. 필수 파일 구조 확인
    print("1️⃣ 필수 파일 구조 확인...")
    file_issues = check_file_structure()
    
    # 2. 서비스별 테이블 생성 설정 확인
    print("\n2️⃣ 서비스별 테이블 생성 설정 확인...")
    table_issues = check_service_table_creation()
    for issue in table_issues:
        print(f"   {issue}")
    
    # 결과 요약
    print("\n📊 검증 결과 요약:")
    total_issues = len(file_issues) + len(table_issues)
    
    if total_issues == 0:
        print("✅ 모든 검증을 통과했습니다!")
        print("\n🎯 다음 단계:")
        print("1. 데이터베이스 enum 검증: docker-compose exec postgres psql -U tsportal -d tsportal -c \"SELECT typname, enumlabel FROM pg_type t JOIN pg_enum e ON t.oid = e.enumtypid WHERE typname = 'userrole';\"")
        print("2. Member Service API 테스트: curl http://localhost:8001/api/members/")
        return 0
    else:
        print(f"❌ {total_issues}개의 문제가 발견되었습니다.")
        print("\n🔧 해결 방법:")
        for issue in file_issues + table_issues:
            print(f"   {issue}")
        print("\n📖 참고: docs/DEVELOPMENT_GUIDELINES.md")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 