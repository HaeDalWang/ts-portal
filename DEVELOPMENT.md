# TS Portal 개발 가이드 📚

> 이 문서는 TS Portal 프로젝트 개발자를 위한 상세한 가이드입니다.

## 📋 목차
- [프로젝트 구조 이해](#-프로젝트-구조-이해)
- [개발 환경 설정](#-개발-환경-설정)
- [코딩 스타일 가이드](#-코딩-스타일-가이드)
- [컴포넌트 개발 가이드](#-컴포넌트-개발-가이드)
- [API 개발 가이드](#-api-개발-가이드)
- [데이터베이스 가이드](#-데이터베이스-가이드)
- [테스트 가이드](#-테스트-가이드)
- [배포 가이드](#-배포-가이드)
- [문제 해결](#-문제-해결)

## 🏗️ 프로젝트 구조 이해

### 마이크로서비스 아키텍처
```
ts-portal/
├── 🎨 frontend/              # Vue 3 SPA (Single Page Application)
│   ├── src/
│   │   ├── components/       # 재사용 가능한 UI 컴포넌트
│   │   ├── views/           # 페이지 레벨 컴포넌트
│   │   ├── services/        # API 통신 로직
│   │   ├── types/           # TypeScript 타입 정의
│   │   ├── router/          # 라우팅 설정
│   │   └── assets/          # 정적 자원
│   └── public/              # 빌드시 복사될 파일들
│
├── 🍯 honeybox/             # RSS 수집 마이크로서비스
│   ├── app/
│   │   ├── routers/         # FastAPI 라우터
│   │   ├── services/        # 비즈니스 로직
│   │   ├── models/          # 데이터 모델
│   │   └── utils/           # 유틸리티 함수
│   └── requirements.txt     # Python 의존성
│
├── 🗄️ ts-portal-db/        # 데이터 관리 마이크로서비스
│   ├── app/
│   │   ├── models/          # SQLAlchemy ORM 모델
│   │   ├── routers/         # API 엔드포인트
│   │   ├── schemas/         # Pydantic 스키마
│   │   ├── services/        # 비즈니스 로직
│   │   └── database.py      # DB 연결 설정
│   └── data/                # SQLite 데이터베이스 파일
│
└── 🚀 terraform/           # Infrastructure as Code
    ├── cicd.tf             # CI/CD 파이프라인
    └── buildspec/          # CodeBuild 설정
```

### 서비스 간 통신
- **Frontend ↔ HoneyBox**: HTTP REST API (포트 8000)
- **Frontend ↔ TS Portal DB**: HTTP REST API (포트 8001)
- **HoneyBox ↔ Redis**: 캐싱 레이어
- **TS Portal DB ↔ SQLite**: 데이터 영속성

## 🛠️ 개발 환경 설정

### 필수 도구
```bash
# Node.js (권장: v18 이상)
node --version

# Python (권장: v3.9 이상)
python --version

# Redis (HoneyBox 캐싱용)
redis-server --version
```

### IDE 설정 (VS Code 권장)
```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "typescript.preferences.importModuleSpecifier": "relative",
  "python.defaultInterpreterPath": "./ts-portal-db/venv/bin/python"
}
```

### 권장 확장 프로그램
- **Vue**: Vue Language Features (Volar)
- **TypeScript**: TypeScript Importer
- **Python**: Python, Pylance
- **Tailwind**: Tailwind CSS IntelliSense
- **Git**: GitLens

## 📝 코딩 스타일 가이드

### Vue 3 + TypeScript 스타일

#### 컴포넌트 구조
```vue
<template>
  <!-- HTML 템플릿 -->
  <div class="container mx-auto px-4">
    <h1 class="text-2xl font-bold text-gray-800">{{ title }}</h1>
  </div>
</template>

<script setup lang="ts">
// 1. 타입 import
import type { Ref } from 'vue'
import type { Member } from '@/types'

// 2. 컴포넌트/함수 import
import { ref, computed, onMounted } from 'vue'
import { memberService } from '@/services/memberService'

// 3. Props 정의 (타입 포함)
interface Props {
  title: string
  members?: Member[]
}
const props = withDefaults(defineProps<Props>(), {
  members: () => []
})

// 4. Emits 정의
interface Emits {
  (e: 'update', member: Member): void
  (e: 'delete', id: number): void
}
const emit = defineEmits<Emits>()

// 5. 반응형 데이터
const isLoading: Ref<boolean> = ref(false)
const searchQuery: Ref<string> = ref('')

// 6. 계산된 속성
const filteredMembers = computed(() => {
  return props.members.filter(member => 
    member.name.includes(searchQuery.value)
  )
})

// 7. 메서드
const handleUpdate = async (member: Member) => {
  try {
    isLoading.value = true
    await memberService.updateMember(member)
    emit('update', member)
  } catch (error) {
    console.error('Failed to update member:', error)
  } finally {
    isLoading.value = false
  }
}

// 8. 라이프사이클 훅
onMounted(() => {
  // 초기화 로직
})
</script>

<style scoped>
/* 필요한 경우에만 커스텀 CSS */
.custom-class {
  @apply bg-purple-50 border border-purple-200;
}
</style>
```

#### TailwindCSS 클래스 순서
```html
<!-- 권장 순서: layout → spacing → typography → colors → effects -->
<div class="
  flex flex-col          <!-- layout -->
  p-4 m-2               <!-- spacing -->
  text-lg font-semibold <!-- typography -->
  text-gray-800 bg-white <!-- colors -->
  shadow-md rounded-lg   <!-- effects -->
">
```

### FastAPI Python 스타일

#### 라우터 구조
```python
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.member import Member, MemberCreate, MemberUpdate
from ..services.member_service import MemberService

router = APIRouter(prefix="/members", tags=["members"])

@router.get("/", response_model=List[Member])
async def get_members(
    skip: int = Query(0, ge=0, description="Skip records"),
    limit: int = Query(100, ge=1, le=1000, description="Limit records"),
    search: Optional[str] = Query(None, description="Search query"),
    db: Session = Depends(get_db)
) -> List[Member]:
    """
    팀원 목록을 조회합니다.
    
    Args:
        skip: 건너뛸 레코드 수
        limit: 조회할 최대 레코드 수
        search: 검색 쿼리
        db: 데이터베이스 세션
    
    Returns:
        팀원 목록
    """
    try:
        service = MemberService(db)
        return await service.get_members(skip=skip, limit=limit, search=search)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=Member, status_code=201)
async def create_member(
    member_data: MemberCreate,
    db: Session = Depends(get_db)
) -> Member:
    """팀원을 생성합니다."""
    try:
        service = MemberService(db)
        return await service.create_member(member_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### Pydantic 스키마
```python
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

class MemberBase(BaseModel):
    """팀원 기본 스키마"""
    name: str = Field(..., min_length=1, max_length=50, description="이름")
    email: EmailStr = Field(..., description="이메일")
    position: str = Field(..., min_length=1, max_length=50, description="직급")
    department: str = Field(..., min_length=1, max_length=50, description="부서")
    skills: List[str] = Field(default_factory=list, description="기술스택")
    phone: Optional[str] = Field(None, max_length=20, description="전화번호")

class MemberCreate(MemberBase):
    """팀원 생성 스키마"""
    pass

class MemberUpdate(BaseModel):
    """팀원 수정 스키마"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    position: Optional[str] = Field(None, min_length=1, max_length=50)
    department: Optional[str] = Field(None, min_length=1, max_length=50)
    skills: Optional[List[str]] = None
    phone: Optional[str] = Field(None, max_length=20)

class Member(MemberBase):
    """팀원 응답 스키마"""
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True
```

## 🧩 컴포넌트 개발 가이드

### 컴포넌트 분류

#### 1. 기본 컴포넌트 (Base Components)
```typescript
// components/base/BaseButton.vue
// components/base/BaseInput.vue
// components/base/BaseModal.vue
```

#### 2. 레이아웃 컴포넌트 (Layout Components)
```typescript
// components/layout/AppHeader.vue
// components/layout/AppSidebar.vue
// components/layout/AppFooter.vue
```

#### 3. 기능 컴포넌트 (Feature Components)
```typescript
// components/member/MemberCard.vue
// components/member/MemberTable.vue
// components/calendar/CalendarView.vue
```

### 컴포넌트 네이밍 규칙
- **Base Components**: `Base` + 기능명 (예: `BaseButton`, `BaseInput`)
- **Layout Components**: `App` + 위치명 (예: `AppHeader`, `AppSidebar`)
- **Feature Components**: 도메인 + 기능명 (예: `MemberCard`, `EventModal`)

### Props와 Events 설계
```typescript
// 좋은 예: 명확한 타입과 기본값
interface Props {
  modelValue: string
  placeholder?: string
  disabled?: boolean
  required?: boolean
  maxLength?: number
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: '',
  disabled: false,
  required: false,
  maxLength: 255
})

// Events는 구체적으로 정의
interface Emits {
  (e: 'update:modelValue', value: string): void
  (e: 'focus'): void
  (e: 'blur'): void
  (e: 'submit'): void
}
```

## 🔗 API 개발 가이드

### RESTful API 설계 원칙

#### URL 구조
```
GET    /members           # 목록 조회
GET    /members/{id}      # 단일 조회
POST   /members           # 생성
PUT    /members/{id}      # 전체 수정
PATCH  /members/{id}      # 부분 수정
DELETE /members/{id}      # 삭제

# 중첩 리소스
GET    /members/{id}/assignments  # 팀원의 담당 업무
POST   /members/{id}/assignments  # 담당 업무 추가
```

#### 응답 형식
```python
# 성공 응답
{
  "data": [...],
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 20
  }
}

# 오류 응답
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "입력값이 올바르지 않습니다.",
    "details": {
      "email": ["올바른 이메일 형식이 아닙니다."]
    }
  }
}
```

### 서비스 레이어 패턴
```python
# services/member_service.py
class MemberService:
    def __init__(self, db: Session):
        self.db = db

    async def get_members(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        search: Optional[str] = None
    ) -> List[Member]:
        """팀원 목록 조회 비즈니스 로직"""
        query = self.db.query(MemberModel)
        
        if search:
            query = query.filter(
                MemberModel.name.contains(search) |
                MemberModel.email.contains(search)
            )
        
        return query.offset(skip).limit(limit).all()

    async def create_member(self, member_data: MemberCreate) -> Member:
        """팀원 생성 비즈니스 로직"""
        # 중복 이메일 체크
        existing = self.db.query(MemberModel).filter(
            MemberModel.email == member_data.email
        ).first()
        
        if existing:
            raise ValueError("이미 존재하는 이메일입니다.")
        
        # 새 팀원 생성
        db_member = MemberModel(**member_data.dict())
        self.db.add(db_member)
        self.db.commit()
        self.db.refresh(db_member)
        
        return db_member
```

## 🗄️ 데이터베이스 가이드

### SQLAlchemy 모델 설계
```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    position = Column(String(50), nullable=False)
    department = Column(String(50), nullable=False)
    skills = Column(JSON, default=list)  # ["Python", "Vue.js", "AWS"]
    phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 관계 정의
    assignments = relationship("Assignment", back_populates="member")
    events = relationship("Event", back_populates="member")

    def __repr__(self):
        return f"<Member(id={self.id}, name='{self.name}')>"
```

### 마이그레이션 관리
```python
# alembic를 사용한 데이터베이스 마이그레이션
# alembic.ini 설정 후

# 새 마이그레이션 생성
alembic revision --autogenerate -m "Add member table"

# 마이그레이션 적용
alembic upgrade head

# 마이그레이션 롤백
alembic downgrade -1
```

## 🧪 테스트 가이드

### Frontend 테스트 (Vitest)
```typescript
// tests/components/MemberCard.test.ts
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import MemberCard from '@/components/member/MemberCard.vue'
import type { Member } from '@/types'

describe('MemberCard', () => {
  const mockMember: Member = {
    id: 1,
    name: '배승도',
    email: 'seungdo@example.com',
    position: '시니어',
    department: 'Tiger Part',
    skills: ['Python', 'Vue.js', 'AWS'],
    phone: '010-1234-5678',
    is_active: true,
    created_at: new Date(),
    updated_at: new Date()
  }

  it('팀원 정보를 올바르게 렌더링한다', () => {
    const wrapper = mount(MemberCard, {
      props: { member: mockMember }
    })

    expect(wrapper.text()).toContain('배승도')
    expect(wrapper.text()).toContain('seungdo@example.com')
    expect(wrapper.text()).toContain('Tiger Part')
  })

  it('기술스택을 태그로 표시한다', () => {
    const wrapper = mount(MemberCard, {
      props: { member: mockMember }
    })

    const skillTags = wrapper.findAll('.skill-tag')
    expect(skillTags).toHaveLength(3)
    expect(skillTags[0].text()).toBe('Python')
  })
})
```

### Backend 테스트 (pytest)
```python
# tests/test_member_api.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db, Base

# 테스트용 인메모리 데이터베이스
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_create_member(client):
    response = client.post(
        "/members/",
        json={
            "name": "테스트 유저",
            "email": "test@example.com",
            "position": "개발자",
            "department": "Tiger Part",
            "skills": ["Python", "FastAPI"]
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "테스트 유저"
    assert data["email"] == "test@example.com"

def test_get_members(client):
    # 테스트 데이터 생성
    client.post("/members/", json={
        "name": "팀원1",
        "email": "member1@example.com",
        "position": "개발자",
        "department": "Tiger Part"
    })
    
    response = client.get("/members/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "팀원1"
```

## 🚀 배포 가이드

### Docker 컨테이너화
```dockerfile
# frontend/Dockerfile
FROM node:18-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginx:alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

```dockerfile
# ts-portal-db/Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8001
CMD ["python", "main.py"]
```

### AWS ECS 배포
```bash
# 1. ECR에 이미지 푸시
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin <account>.dkr.ecr.ap-northeast-2.amazonaws.com

docker build -t ts-portal-frontend ./frontend
docker tag ts-portal-frontend:latest <account>.dkr.ecr.ap-northeast-2.amazonaws.com/ts-portal-frontend:latest
docker push <account>.dkr.ecr.ap-northeast-2.amazonaws.com/ts-portal-frontend:latest

# 2. Terraform으로 인프라 배포
cd terraform
terraform init
terraform plan
terraform apply
```

## 🔧 문제 해결

### 일반적인 이슈들

#### 1. CORS 오류
```python
# main.py에 CORS 미들웨어 추가
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 2. 포트 충돌
```bash
# 사용중인 포트 확인
lsof -i :8000
lsof -i :8001
lsof -i :5173

# 프로세스 종료
kill -9 <PID>
```

#### 3. 데이터베이스 연결 오류
```python
# SQLite 파일 권한 확인
ls -la data/ts_portal.db

# 권한 수정
chmod 664 data/ts_portal.db
```

#### 4. Redis 연결 실패
```bash
# Redis 서버 상태 확인
redis-cli ping

# Redis 서버 시작
redis-server
```

### 로그 확인 방법
```bash
# Frontend 빌드 로그
cd frontend && npm run build

# Backend 로그
cd ts-portal-db && python main.py

# Docker 컨테이너 로그
docker logs <container_id>
```

## 📚 추가 학습 자료

### 공식 문서
- [Vue 3 Composition API](https://vuejs.org/guide/extras/composition-api-faq.html)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [FastAPI User Guide](https://fastapi.tiangolo.com/tutorial/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)

### 권장 도서
- "Vue.js 3 완벽 가이드" - 프론트엔드 개발
- "FastAPI로 배우는 파이썬 웹 개발" - 백엔드 개발
- "클린 아키텍처" - 소프트웨어 설계

---

**이 가이드는 살아있는 문서입니다. 프로젝트가 발전함에 따라 지속적으로 업데이트됩니다.** 🚀 