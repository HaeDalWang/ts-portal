-- TS Portal 데이터베이스 초기 설정 스크립트
-- 모든 마이크로서비스가 공유하는 스키마와 타입을 정의합니다

-- =================================
-- 1. 스키마 생성
-- =================================

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
    CREATE TYPE public.noticepriority AS ENUM ('normal', 'caution', 'important');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 일정 유형
DO $$ BEGIN
    CREATE TYPE public.eventtype AS ENUM (
        'vacation',
        'remote',
        'business_trip',
        'project',
        'education',
        'meeting',
        'other'
    );
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
GRANT USAGE ON SCHEMA member_schema TO tsportal;
GRANT USAGE ON SCHEMA notice_schema TO tsportal;
GRANT USAGE ON SCHEMA calendar_schema TO tsportal;
GRANT USAGE ON SCHEMA customer_schema TO tsportal;
GRANT USAGE ON SCHEMA feeds_schema TO tsportal;

-- 각 스키마에 대한 테이블 생성/수정/삭제 권한
GRANT CREATE ON SCHEMA member_schema TO tsportal;
GRANT CREATE ON SCHEMA notice_schema TO tsportal;
GRANT CREATE ON SCHEMA calendar_schema TO tsportal;
GRANT CREATE ON SCHEMA customer_schema TO tsportal;
GRANT CREATE ON SCHEMA feeds_schema TO tsportal;

-- =================================
-- 5. 테이블 생성
-- =================================

-- 멤버 테이블
CREATE TABLE IF NOT EXISTS member_schema.members (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password_hash VARCHAR(255),
    role userrole NOT NULL DEFAULT 'USER',
    last_login TIMESTAMP WITH TIME ZONE,
    position VARCHAR(50),
    team VARCHAR(50) DEFAULT 'TS팀',
    skills TEXT,
    join_date DATE,
    is_active BOOLEAN DEFAULT true,
    profile_image_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 공지사항 테이블
CREATE TABLE IF NOT EXISTS notice_schema.notices (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    priority noticepriority DEFAULT 'normal',
    author_id INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT true,
    is_pinned BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 일정 테이블
CREATE TABLE IF NOT EXISTS calendar_schema.events (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    event_type eventtype DEFAULT 'other',
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    location VARCHAR(200),
    created_by INTEGER NOT NULL,
    attendees JSONB,
    is_all_day BOOLEAN DEFAULT false,
    is_recurring BOOLEAN DEFAULT false,
    recurrence_rule TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 고객사 테이블
CREATE TABLE IF NOT EXISTS customer_schema.customers (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL UNIQUE,
    contact_person VARCHAR(50),
    contact_email VARCHAR(100),
    contact_phone VARCHAR(20),
    contract_type VARCHAR(50),
    contract_start DATE,
    contract_end DATE,
    status customerstatus DEFAULT 'ACTIVE',
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 고객사 담당자 할당 테이블
CREATE TABLE IF NOT EXISTS customer_schema.assignments (
    id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL REFERENCES customer_schema.customers(id),
    role assignmentrole NOT NULL,
    assigned_date DATE DEFAULT CURRENT_DATE,
    end_date DATE,
    is_primary BOOLEAN DEFAULT true,
    responsibilities TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 업데이트 트리거 설정
CREATE TRIGGER update_member_updated_at
    BEFORE UPDATE ON member_schema.members
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_notice_updated_at
    BEFORE UPDATE ON notice_schema.notices
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_event_updated_at
    BEFORE UPDATE ON calendar_schema.events
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_customer_updated_at
    BEFORE UPDATE ON customer_schema.customers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_assignment_updated_at
    BEFORE UPDATE ON customer_schema.assignments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =================================
-- 6. 인덱스 생성
-- =================================

-- 멤버 인덱스
CREATE INDEX IF NOT EXISTS idx_members_email ON member_schema.members(email);
CREATE INDEX IF NOT EXISTS idx_members_username ON member_schema.members(username);
CREATE INDEX IF NOT EXISTS idx_members_role ON member_schema.members(role);

-- 공지사항 인덱스
CREATE INDEX IF NOT EXISTS idx_notices_author ON notice_schema.notices(author_id);
CREATE INDEX IF NOT EXISTS idx_notices_priority ON notice_schema.notices(priority);
CREATE INDEX IF NOT EXISTS idx_notices_created_at ON notice_schema.notices(created_at);

-- 일정 인덱스
CREATE INDEX IF NOT EXISTS idx_events_created_by ON calendar_schema.events(created_by);
CREATE INDEX IF NOT EXISTS idx_events_start_time ON calendar_schema.events(start_time);
CREATE INDEX IF NOT EXISTS idx_events_end_time ON calendar_schema.events(end_time);
CREATE INDEX IF NOT EXISTS idx_events_type ON calendar_schema.events(event_type);

-- 고객사 인덱스
CREATE INDEX IF NOT EXISTS idx_customers_status ON customer_schema.customers(status);
CREATE INDEX IF NOT EXISTS idx_customers_company ON customer_schema.customers(company_name);

-- 고객사 담당자 할당 인덱스
CREATE INDEX IF NOT EXISTS idx_assignments_member ON customer_schema.assignments(member_id);
CREATE INDEX IF NOT EXISTS idx_assignments_customer ON customer_schema.assignments(customer_id);
CREATE INDEX IF NOT EXISTS idx_assignments_role ON customer_schema.assignments(role);

-- =================================
-- 7. 설정 확인 쿼리
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