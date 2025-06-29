# TS Portal Feeds Service

AWS 소식 수집 마이크로서비스 (경량화 버전)

## 🚀 개요

**TS Portal Feeds Service**는 AWS 공식 블로그와 소식을 실시간으로 수집하는 경량화된 마이크로서비스입니다.

### ✨ 주요 특징
- **🏃‍♂️ 경량화**: 단일 파일 구조로 최적화
- **⚡ UV 기반**: 최신 Python 패키지 관리자 사용
- **🔄 비동기**: httpx + feedparser로 고성능 RSS 처리
- **🐳 컨테이너화**: Docker 최적화 및 헬스체크 지원
- **📊 RESTful API**: 간단하고 직관적인 엔드포인트

## 📋 수집 피드

| 피드 ID | 이름 | 설명 |
|---------|------|------|
| `aws-blog` | AWS Blog | AWS 공식 블로그 |
| `aws-news` | AWS What's New | AWS 최신 소식 |
| `aws-security` | AWS Security Blog | AWS 보안 블로그 |

## 🛠 기술 스택

- **언어**: Python 3.11+
- **프레임워크**: FastAPI
- **패키지 관리**: UV (Rust 기반)
- **HTTP 클라이언트**: httpx (비동기)
- **RSS 파서**: feedparser
- **컨테이너**: Docker + 헬스체크

## 📡 API 엔드포인트

### 기본 정보
- `GET /` - 서비스 정보 및 엔드포인트 목록
- `GET /health` - 헬스체크

### 피드 관련
- `GET /feeds` - 사용 가능한 피드 목록
- `GET /feeds/all` - 모든 피드 최신 소식 (기본 5개씩)
- `GET /feeds/{feed_id}` - 특정 피드 조회 (기본 10개)
- `GET /feeds/latest` - 오늘의 AWS 소식 (기본 3개)

### 쿼리 파라미터
- `limit`: 반환할 아이템 수 (기본값: 엔드포인트별 상이)

## 🚀 빠른 시작

### 1. UV 환경 설정
```bash
# UV 설치 (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 의존성 설치
uv sync

# 개발 서버 실행
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Docker 실행
```bash
# 이미지 빌드
docker build -t ts-portal-feeds-service .

# 컨테이너 실행
docker run -p 8000:8000 ts-portal-feeds-service
```

### 3. Docker Compose (권장)
```bash
# 전체 TS Portal 스택과 함께 실행
docker-compose up -d feeds-service
```

## 📊 사용 예시

### 기본 정보 확인
```bash
curl http://localhost:8000/
```

### 모든 피드 최신 소식
```bash
curl "http://localhost:8000/feeds/all?limit=3"
```

### 특정 피드 조회
```bash
curl "http://localhost:8000/feeds/aws-news?limit=5"
```

### 오늘의 AWS 소식
```bash
curl http://localhost:8000/feeds/latest
```

## 🏗 아키텍처

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   API Gateway   │───▶│  Feeds Service   │───▶│   AWS Feeds     │
│   (Port 8080)   │    │   (Port 8000)    │    │   (RSS/HTTP)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Feed Parser    │
                       │   (feedparser)   │
                       └──────────────────┘
```

## 🔧 환경 변수

| 변수명 | 기본값 | 설명 |
|--------|--------|------|
| `PYTHONPATH` | `/app` | Python 경로 |
| `UV_NO_CACHE` | `1` | UV 캐시 비활성화 |
| `UV_CACHE_DIR` | `/dev/null` | UV 캐시 디렉토리 |

## 📈 성능 특징

- **시작 시간**: 2-3초 (UV 최적화)
- **메모리 사용량**: ~50MB (경량화)
- **응답 시간**: 100-500ms (피드별)
- **동시 처리**: 비동기 처리로 고성능

## 🔍 모니터링

### 헬스체크
```bash
curl http://localhost:8000/health
```

### Docker 헬스체크
```bash
docker ps  # HEALTHY 상태 확인
```

### 로그 확인
```bash
docker logs ts-portal-feeds-service
```

## 🤝 기존 HoneyBox와의 차이점

| 항목 | HoneyBox (기존) | Feeds Service (신규) |
|------|-----------------|---------------------|
| **구조** | 복잡한 모듈 구조 | 단일 파일 경량화 |
| **패키지 관리** | pip + requirements.txt | UV + pyproject.toml |
| **의존성** | 8개 패키지 + Redis | 6개 패키지만 |
| **코드 라인** | 600+ 라인 | 200 라인 |
| **시작 시간** | 10-15초 | 2-3초 |
| **메모리** | ~100MB | ~50MB |
| **복잡도** | 높음 (설정, 번역, 캐시) | 낮음 (RSS만 집중) |

## 🔄 마이그레이션

기존 HoneyBox에서 마이그레이션:

1. **API 호환성**: 기본 엔드포인트 유지
2. **데이터 형식**: JSON 응답 구조 동일
3. **Docker**: 포트 8000 동일 사용
4. **API Gateway**: 자동 라우팅 지원

## 🛠 개발

### 코드 구조
```
feeds-service/
├── app/
│   └── main.py          # 메인 애플리케이션 (단일 파일)
├── pyproject.toml       # UV 프로젝트 설정
├── uv.lock             # 의존성 잠금
├── Dockerfile          # UV 최적화 컨테이너
└── README.md           # 문서
```

### 의존성 관리
```bash
# 의존성 추가
uv add package-name

# 개발 의존성 추가
uv add --dev package-name

# 의존성 업데이트
uv lock --upgrade
```

## 📚 관련 문서

- [TS Portal 전체 아키텍처](../README.md)
- [API Gateway 문서](../api-gateway/README.md)
- [Docker Compose 가이드](../../README.md)

---

**TS Portal Feeds Service** - 경량화된 AWS 소식 수집 서비스 ⚡ 