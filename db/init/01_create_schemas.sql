-- TS Portal Database Schema
-- PostgreSQL 초기화 스크립트

-- 스키마 생성 (MSA를 위한 논리적 분리)
CREATE SCHEMA IF NOT EXISTS member_schema;
CREATE SCHEMA IF NOT EXISTS customer_schema;
CREATE SCHEMA IF NOT EXISTS calendar_schema;
CREATE SCHEMA IF NOT EXISTS notice_schema;

-- 확장 기능 활성화
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Members 테이블 (member_schema)
CREATE TABLE IF NOT EXISTS member_schema.members (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    phone VARCHAR(20),
    position VARCHAR(100),
    team VARCHAR(100),
    skills TEXT,
    join_date DATE,
    birth_date DATE,
    emergency_contact VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('admin', 'power_user', 'user')),
    profile_image_url VARCHAR(500),
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customers 테이블 (customer_schema)
CREATE TABLE IF NOT EXISTS customer_schema.customers (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(100),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(20),
    address TEXT,
    contract_type VARCHAR(50),
    contract_start DATE,
    contract_end DATE,
    technical_support_level VARCHAR(20) DEFAULT 'Standard',
    monthly_fee DECIMAL(10, 2),
    status VARCHAR(20) DEFAULT 'Active',
    notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    primary_manager_id INTEGER,
    secondary_manager_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Assignments 테이블 (customer_schema)
CREATE TABLE IF NOT EXISTS customer_schema.assignments (
    id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    role VARCHAR(50),
    assigned_date DATE DEFAULT CURRENT_DATE,
    end_date DATE,
    is_primary BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    responsibilities TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(member_id, customer_id, is_active)
);

-- Events 테이블 (calendar_schema)
CREATE TABLE IF NOT EXISTS calendar_schema.events (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    event_type VARCHAR(50) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    location VARCHAR(200),
    created_by INTEGER NOT NULL,
    attendees JSONB,
    is_all_day BOOLEAN DEFAULT FALSE,
    is_recurring BOOLEAN DEFAULT FALSE,
    recurrence_rule TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Notices 테이블 (notice_schema)
CREATE TABLE IF NOT EXISTS notice_schema.notices (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    notice_type VARCHAR(50) DEFAULT 'general',
    priority VARCHAR(20) DEFAULT 'normal',
    author_id INTEGER NOT NULL,
    is_pinned BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    view_count INTEGER DEFAULT 0,
    tags JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP
);

-- 인덱스 생성
CREATE INDEX idx_members_email ON member_schema.members(email);
CREATE INDEX idx_members_active ON member_schema.members(is_active);
CREATE INDEX idx_customers_status ON customer_schema.customers(status);
CREATE INDEX idx_assignments_member ON customer_schema.assignments(member_id);
CREATE INDEX idx_assignments_customer ON customer_schema.assignments(customer_id);
CREATE INDEX idx_events_start ON calendar_schema.events(start_time);
CREATE INDEX idx_events_created_by ON calendar_schema.events(created_by);
CREATE INDEX idx_notices_author ON notice_schema.notices(author_id);
CREATE INDEX idx_notices_type ON notice_schema.notices(notice_type);

-- 업데이트 트리거 함수
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 각 테이블에 업데이트 트리거 적용
CREATE TRIGGER update_members_updated_at BEFORE UPDATE ON member_schema.members
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_customers_updated_at BEFORE UPDATE ON customer_schema.customers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_assignments_updated_at BEFORE UPDATE ON customer_schema.assignments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_events_updated_at BEFORE UPDATE ON calendar_schema.events
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_notices_updated_at BEFORE UPDATE ON notice_schema.notices
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 기본 관리자 계정 생성
INSERT INTO member_schema.members (name, email, password_hash, position, team, role, is_active)
VALUES ('관리자', 'admin@tsportal.com', 'temp_hash_will_be_updated', 'System Admin', 'Platform', 'admin', true)
ON CONFLICT (email) DO NOTHING; 