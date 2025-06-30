-- TS Portal 데이터베이스 초기 설정 스크립트
-- 모든 마이크로서비스가 공유하는 스키마와 타입을 정의합니다

-- =================================
-- 1. 스키마 생성
-- =================================

CREATE SCHEMA IF NOT EXISTS auth_schema;
CREATE SCHEMA IF NOT EXISTS member_schema;
CREATE SCHEMA IF NOT EXISTS notice_schema;
CREATE SCHEMA IF NOT EXISTS calendar_schema;
CREATE SCHEMA IF NOT EXISTS customer_schema;
CREATE SCHEMA IF NOT EXISTS feeds_schema;

-- =================================
-- 2. ENUM 타입 정의 (전체 시스템 공통)
-- =================================

-- 사용자 권한 레벨
DO $$ BEGIN
    CREATE TYPE public.userrole AS ENUM ('ADMIN', 'POWER_USER', 'USER');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 공지사항 우선순위
DO $$ BEGIN
    CREATE TYPE public.noticepriority AS ENUM ('HIGH', 'MEDIUM', 'LOW');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 일정 유형
DO $$ BEGIN
    CREATE TYPE public.eventtype AS ENUM ('MEETING', 'PERSONAL', 'PROJECT', 'DEADLINE', 'HOLIDAY');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 고객 상태
DO $$ BEGIN
    CREATE TYPE public.customerstatus AS ENUM ('ACTIVE', 'INACTIVE', 'PENDING', 'SUSPENDED');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 고객 담당자 역할
DO $$ BEGIN
    CREATE TYPE public.assignmentrole AS ENUM ('PRIMARY', 'SECONDARY', 'CONSULTANT');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- =================================
-- 3. 공통 함수 정의
-- =================================

-- 업데이트 시간 자동 설정 함수
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- =================================
-- 4. 권한 설정
-- =================================

-- tsportal 사용자에게 모든 스키마 접근 권한 부여
GRANT USAGE ON SCHEMA auth_schema TO tsportal;
GRANT USAGE ON SCHEMA member_schema TO tsportal;
GRANT USAGE ON SCHEMA notice_schema TO tsportal;
GRANT USAGE ON SCHEMA calendar_schema TO tsportal;
GRANT USAGE ON SCHEMA customer_schema TO tsportal;
GRANT USAGE ON SCHEMA feeds_schema TO tsportal;

-- 각 스키마에 대한 테이블 생성/수정/삭제 권한
GRANT CREATE ON SCHEMA auth_schema TO tsportal;
GRANT CREATE ON SCHEMA member_schema TO tsportal;
GRANT CREATE ON SCHEMA notice_schema TO tsportal;
GRANT CREATE ON SCHEMA calendar_schema TO tsportal;
GRANT CREATE ON SCHEMA customer_schema TO tsportal;
GRANT CREATE ON SCHEMA feeds_schema TO tsportal;

-- =================================
-- 5. 설정 확인 쿼리
-- =================================

-- 생성된 스키마 확인
SELECT schema_name FROM information_schema.schemata 
WHERE schema_name LIKE '%_schema';

-- 생성된 enum 타입 확인
SELECT typname, enumlabel 
FROM pg_type t 
JOIN pg_enum e ON t.oid = e.enumtypid
WHERE typname IN ('userrole', 'noticepriority', 'eventtype', 'customerstatus', 'assignmentrole')
ORDER BY typname, enumlabel; 