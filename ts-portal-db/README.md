# TS Portal Database API

Saltware CSG TS팀 포털을 위한 데이터베이스 API 서버입니다.

## 🎯 주요 기능

- **팀원 프로필 관리**: 팀원 정보, 기술 스택, 연락처 관리
- **MSP 고객사 관리**: 고객사 정보, 계약 상태, 담당자 정보 관리
- **담당 배정 관리**: 팀원-고객사 매핑, 역할 및 책임 관리
- **팀 일정 관리**: 회의, 교육, 이벤트 등 팀 일정 관리

## 🏗️ 기술 스택

- **Backend**: FastAPI 0.104.1
- **Database**: SQLite (로컬), EFS + SQLite (배포)
- **ORM**: SQLAlchemy 2.0.23
- **Migration**: Alembic 1.13.1
- **Validation**: Pydantic 2.5.0

## 📊 데이터베이스 구조

### 테이블 관계
```
MEMBERS (팀원)
├── assignments → ASSIGNMENTS (담당 배정)
└── created_events → EVENTS (생성한 일정)

CUSTOMERS (고객사)
└── assignments → ASSIGNMENTS (담당 배정)

ASSIGNMENTS (담당 배정)
├── member → MEMBERS (담당 팀원)
└── customer → CUSTOMERS (담당 고객사)

EVENTS (일정)
└── creator → MEMBERS (생성자)
```

### 주요 테이블
- **members**: 팀원 정보 (이름, 이메일, 직급, 기술스택 등)
- **customers**: 고객사 정보 (회사명, 담당자, 계약정보 등)
- **assignments**: 담당 배정 (팀원-고객사 매핑, 역할, 책임)
- **events**: 팀 일정 (회의, 교육, 이벤트 등)

## 🚀 설치 및 실행

### 1. 의존성 설치
```bash
cd ts-portal/ts-portal-db
pip install -r requirements.txt
```

### 2. 개발 서버 실행
```bash
python main.py
```
→ http://localhost:8001 에서 확인 가능

### 3. API 문서 확인
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## 📡 API 엔드포인트

### 기본 정보
- `GET /` - API 기본 정보
- `GET /health` - 헬스 체크
- `GET /db-info` - 데이터베이스 정보
- `GET /stats` - 데이터베이스 통계

### 향후 추가 예정
- `GET /api/members` - 팀원 목록
- `POST /api/members` - 팀원 등록
- `GET /api/customers` - 고객사 목록
- `POST /api/customers` - 고객사 등록
- `GET /api/assignments` - 담당 배정 목록
- `POST /api/assignments` - 담당 배정
- `GET /api/events` - 일정 목록
- `POST /api/events` - 일정 등록

## 🗂️ 프로젝트 구조

```
ts-portal-db/
├── app/                        # 메인 애플리케이션
│   ├── __init__.py
│   ├── main.py                 # FastAPI 앱
│   ├── database.py             # DB 연결 설정
│   ├── models/                 # SQLAlchemy 모델들
│   │   ├── __init__.py
│   │   ├── member.py           # 팀원 모델
│   │   ├── customer.py         # 고객사 모델
│   │   ├── assignment.py       # 담당 배정 모델
│   │   └── event.py            # 일정 모델
│   ├── schemas/                # Pydantic 스키마들 (향후 추가)
│   ├── routers/                # API 라우터들 (향후 추가)
│   └── utils/                  # 유틸리티 함수들
├── data/                       # SQLite 데이터베이스 저장소
│   └── .gitkeep
├── requirements.txt            # Python 의존성
├── main.py                     # 실행 진입점
└── README.md                   # 이 파일
```

## 🔧 개발 가이드

### 데이터베이스 모델 수정 시
1. `app/models/` 디렉토리의 해당 모델 파일 수정
2. 애플리케이션 재시작 (개발 모드에서는 자동 재시작)
3. 필요시 `data/ts_portal.db` 파일 삭제 후 재생성

### 새로운 API 추가 시
1. `app/schemas/` 에 Pydantic 스키마 정의
2. `app/routers/` 에 라우터 생성
3. `app/main.py` 에 라우터 등록

## 🐳 배포 설정

### ECS + EFS 배포 시 고려사항
- 데이터베이스 파일 경로: `/app/data/ts_portal.db`
- EFS 마운트 포인트: `/app/data`
- 환경변수: `DATABASE_PATH` (선택적)

### Docker 빌드 (향후 추가 예정)
```bash
docker build -t ts-portal-db .
docker run -p 8001:8001 -v ./data:/app/data ts-portal-db
```

## 📝 개발 로드맵

### Phase 1: 기본 구조 (완료)
- ✅ 데이터베이스 모델 정의
- ✅ FastAPI 기본 설정
- ✅ SQLite 연결 설정

### Phase 2: API 개발 (진행 예정)
- [ ] Pydantic 스키마 정의
- [ ] CRUD API 엔드포인트 개발
- [ ] 데이터 검증 및 에러 처리

### Phase 3: 고급 기능 (향후)
- [ ] 사용자 인증 시스템
- [ ] 파일 업로드 (프로필 사진)
- [ ] 알림 시스템
- [ ] 데이터 백업/복구

## 🤝 기여하기

1. 새로운 모델 추가: `app/models/` 디렉토리에 파일 추가
2. API 엔드포인트 추가: `app/routers/` 디렉토리에 라우터 추가
3. 스키마 정의: `app/schemas/` 디렉토리에 Pydantic 모델 추가

---

**개발팀**: Saltware CSG TS Team  
**최초 생성**: 2024-12-18  
**포트**: 8001 (HoneyBox: 8000, Frontend: 5173) 