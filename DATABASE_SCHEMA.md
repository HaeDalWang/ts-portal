# TS Portal 데이터베이스 스키마

## 스키마 구조

```sql
CREATE SCHEMA member_schema;   -- 팀원 정보
CREATE SCHEMA notice_schema;   -- 공지사항
CREATE SCHEMA calendar_schema; -- 일정 관리
CREATE SCHEMA customer_schema; -- 고객사 관리
CREATE SCHEMA feeds_schema;    -- AWS 피드
```

## Enum 타입 정의

### UserRole (사용자 권한)
```sql
CREATE TYPE public.userrole AS ENUM (
    'ADMIN',       -- 관리자: 모든 권한
    'POWER_USER',  -- 파워유저: 데이터 조회/수정
    'USER'         -- 일반유저: 기본 조회만
);
```

### NoticePriority (공지사항 중요도)
```sql
CREATE TYPE public.noticepriority AS ENUM (
    'normal',    -- 일반
    'caution',   -- 주의
    'important'  -- 중요
);
```

### EventType (일정 유형)
```sql
CREATE TYPE public.eventtype AS ENUM (
    'vacation',       -- 휴가
    'remote',         -- 재택근무
    'business_trip',  -- 출장
    'project',        -- 프로젝트
    'education',      -- 교육/세미나
    'meeting',        -- 회의
    'other'          -- 기타
);
```

### CustomerStatus (고객사 상태)
```sql
CREATE TYPE public.customerstatus AS ENUM (
    'ACTIVE',     -- 활성
    'INACTIVE',   -- 비활성
    'PENDING',    -- 대기중
    'SUSPENDED'   -- 정지
);
```

### AssignmentRole (고객 담당자 역할)
```sql
CREATE TYPE public.assignmentrole AS ENUM (
    'PRIMARY',     -- 주담당자
    'SECONDARY',   -- 부담당자
    'CONSULTANT'   -- 컨설턴트
);
```

## 테이블 정의

### member_schema.members
```sql
CREATE TABLE member_schema.members (
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
```

### notice_schema.notices
```sql
CREATE TABLE notice_schema.notices (
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
```

### calendar_schema.events
```sql
CREATE TABLE calendar_schema.events (
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
```

### customer_schema.customers
```sql
CREATE TABLE customer_schema.customers (
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
```

### customer_schema.assignments
```sql
CREATE TABLE customer_schema.assignments (
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
```

## Frontend Type 정의 (TypeScript)

```typescript
// src/types/common.ts

export enum UserRole {
    ADMIN = "ADMIN",
    POWER_USER = "POWER_USER",
    USER = "USER"
}

export enum NoticePriority {
    NORMAL = "normal",
    CAUTION = "caution",
    IMPORTANT = "important"
}

export enum EventType {
    VACATION = "vacation",
    REMOTE = "remote",
    BUSINESS_TRIP = "business_trip",
    PROJECT = "project",
    EDUCATION = "education",
    MEETING = "meeting",
    OTHER = "other"
}

export enum CustomerStatus {
    ACTIVE = "ACTIVE",
    INACTIVE = "INACTIVE",
    PENDING = "PENDING",
    SUSPENDED = "SUSPENDED"
}

export enum AssignmentRole {
    PRIMARY = "PRIMARY",
    SECONDARY = "SECONDARY",
    CONSULTANT = "CONSULTANT"
}
```

## 주의사항

1. **대소문자 일관성**
   - UserRole: 대문자 (ADMIN, POWER_USER, USER)
   - NoticePriority: 소문자 (normal, caution, important)
   - EventType: 소문자 (vacation, remote, ...)
   - CustomerStatus: 대문자 (ACTIVE, INACTIVE, ...)
   - AssignmentRole: 대문자 (PRIMARY, SECONDARY, ...)

2. **시간대 처리**
   - 모든 timestamp 필드는 `WITH TIME ZONE` 사용
   - Frontend에서 UTC로 전송, 표시할 때 로컬 시간으로 변환

3. **NULL 허용**
   - 필수 필드는 `NOT NULL` 명시
   - 선택적 필드는 NULL 허용 (default 없음)

4. **인덱스**
   - 모든 PK는 자동으로 인덱스 생성
   - 검색/조인에 자주 사용되는 필드에 추가 인덱스 필요 