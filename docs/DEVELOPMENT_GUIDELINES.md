# TS Portal 마이크로서비스 개발 가이드라인

## 🎯 개요

이 문서는 TS Portal 마이크로서비스 개발 시 일관성과 안정성을 보장하기 위한 가이드라인입니다.

## 📋 필수 준수사항

### 1. 공통 타입 사용

**❌ 하지 말 것:**
```python
# 각 서비스에서 개별적으로 enum 정의
class UserRole(str, enum.Enum):
    ADMIN = "admin"  # 소문자 사용
    USER = "user"
```

**✅ 해야 할 것:**
```python
# 공통 타입 모듈에서 import
from shared.types import UserRole, DATABASE_SCHEMAS

# 모든 enum 값은 대문자 사용 (PostgreSQL enum과 일치)
```

### 2. 데이터베이스 테이블 생성 규칙

**❌ 하지 말 것:**
```python
# 모든 서비스에서 테이블 자동 생성
Base.metadata.create_all(bind=engine)
```

**✅ 해야 할 것:**
```python
# Auth Service만 테이블 생성, 나머지는 기존 테이블 사용
if os.getenv("SERVICE_NAME") == "auth-service":
    Base.metadata.create_all(bind=engine)
else:
    # 기존 테이블 사용
    pass
```

### 3. 스키마 네이밍 규칙

- **스키마명:** `{service_name}_schema` (예: `member_schema`, `notice_schema`)
- **테이블명:** 복수형 사용 (예: `members`, `notices`)
- **컬럼명:** snake_case 사용 (예: `created_at`, `profile_image_url`)

### 4. Enum 정의 규칙

- **PostgreSQL enum과 정확히 일치해야 함**
- **대문자만 사용** (예: `ADMIN`, `POWER_USER`, `USER`)
- **공통 타입 모듈에서 정의하고 import하여 사용**

## 🔧 개발 프로세스

### 새로운 서비스 생성 시

1. **공통 타입 확인**
   ```bash
   # 필요한 enum이 shared/types.py에 있는지 확인
   cat ts-portal/services/shared/types.py
   ```

2. **데이터베이스 스키마 설계**
   ```sql
   -- 새로운 enum이 필요한 경우 database_setup.sql에 추가
   CREATE TYPE public.new_enum AS ENUM ('VALUE1', 'VALUE2');
   ```

3. **모델 정의**
   ```python
   from shared.types import UserRole, DATABASE_SCHEMAS
   
   class MyModel(Base):
       __tablename__ = "my_table"
       __table_args__ = {"schema": DATABASE_SCHEMAS["my_service"]}
       
       role = Column(Enum(UserRole), nullable=False)
   ```

4. **테이블 생성 비활성화**
   ```python
   # main.py에서 테이블 자동 생성 비활성화
   # Base.metadata.create_all(bind=engine)  # 주석 처리
   ```

### 기존 서비스 수정 시

1. **enum 값 변경이 필요한 경우**
   - `shared/types.py` 수정
   - `database_setup.sql` 수정
   - 모든 서비스 재배포
   - 데이터 마이그레이션 스크립트 작성

2. **새로운 컬럼 추가 시**
   - 마이그레이션 스크립트 작성
   - 모든 관련 서비스 업데이트

## 🧪 테스트 규칙

### Enum 일관성 테스트

```python
# 각 서비스의 테스트에서 enum 일관성 검증
from shared.types import validate_enum_consistency

def test_enum_consistency():
    assert validate_enum_consistency() == True
```

### 데이터베이스 연결 테스트

```python
def test_database_connection():
    # 데이터베이스 연결 및 스키마 존재 확인
    assert check_database_connection() == True
    assert check_schema_exists() == True
```

## 📁 프로젝트 구조

```
ts-portal/
├── services/
│   ├── shared/
│   │   └── types.py              # 공통 타입 정의
│   ├── auth-service/             # 마스터 서비스 (테이블 생성)
│   ├── member-service/           # 기존 테이블 사용
│   ├── notice-service/           # 기존 테이블 사용
│   └── ...
├── scripts/
│   └── database_setup.sql        # 데이터베이스 초기 설정
└── docs/
    └── DEVELOPMENT_GUIDELINES.md # 이 문서
```

## 🚨 문제 발생 시 체크리스트

### API 500 에러 발생 시

1. **Enum 값 확인**
   ```sql
   SELECT enumlabel FROM pg_enum WHERE enumtypid = (
       SELECT oid FROM pg_type WHERE typname = 'userrole'
   );
   ```

2. **실제 데이터 확인**
   ```sql
   SELECT DISTINCT role FROM member_schema.members;
   ```

3. **Python enum과 비교**
   ```python
   from shared.types import UserRole
   print([role.value for role in UserRole])
   ```

### 테이블 생성 충돌 시

1. **테이블 자동 생성 비활성화 확인**
2. **스키마 권한 확인**
3. **기존 테이블 구조와 모델 일치 확인**

## 📝 변경 로그

| 날짜 | 변경사항 | 담당자 |
|------|----------|--------|
| 2025-06-29 | 초기 가이드라인 작성 | 배승도 |
| 2025-06-29 | Enum 일관성 규칙 추가 | 배승도 |

## 🔗 관련 문서

- [API 설계 가이드](./API_DESIGN_GUIDE.md)
- [데이터베이스 스키마 문서](./DATABASE_SCHEMA.md)
- [배포 가이드](./DEPLOYMENT_GUIDE.md) 