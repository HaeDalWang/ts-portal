# HoneyBox - AWS 소식 RSS 수집기 🍯

AWS 블로그들의 RSS를 수집하여 매일 하나씩 선별해서 보여주는 FastAPI 기반 서비스입니다.

## ✨ 주요 기능

- **일일 소식 선별**: 하이브리드 알고리즘으로 매일 최적의 AWS 소식을 선별
- **요일별 우선순위**: 요일에 따라 다른 카테고리를 우선적으로 선별
- **품질 평가**: 제목, 내용, 키워드 등을 기반으로 한 품질 점수 계산
- **한국어 지원**: AWS Korea Blog 우선 선별 + 선택적 번역 기능
- **캐싱 시스템**: 일일 결과 캐싱으로 성능 최적화
- **백업 로직**: 3단계 백업 시스템으로 안정적인 콘텐츠 제공

## 🏗️ 프로젝트 구조

```
honeybox/
├── app/                        # 메인 애플리케이션 패키지
│   ├── __init__.py
│   ├── main.py                 # FastAPI 앱 설정
│   ├── config.py               # 환경변수 및 설정 관리
│   ├── models/                 # 데이터 모델
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic 스키마들
│   ├── services/               # 비즈니스 로직 서비스들
│   │   ├── __init__.py
│   │   ├── rss_service.py      # RSS 피드 수집 및 파싱
│   │   ├── translation_service.py  # 번역 관련 로직
│   │   ├── quality_service.py      # 품질 평가 알고리즘
│   │   └── selection_service.py    # 일일 소식 선별 로직
│   ├── routers/                # API 라우터들
│   │   ├── __init__.py
│   │   ├── feeds.py            # RSS 피드 관련 엔드포인트
│   │   └── daily_news.py       # 일일 소식 엔드포인트
│   └── utils/                  # 유틸리티 함수들
│       ├── __init__.py
│       ├── cache.py            # 캐싱 관리
│       └── date_utils.py       # 날짜 처리 함수들
├── main.py                     # 실행 진입점
├── requirements.txt            # Python 의존성
├── README.md                   # 이 파일
└── main_old.py                 # 이전 단일 파일 버전 (백업)
```

## 🚀 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정 (선택사항)

```bash
# 번역 기능 활성화 (AWS Credentials 필요)
export ENABLE_TRANSLATION=true
export AWS_REGION=ap-northeast-2

# AWS Credentials 설정
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
```

### 3. 서버 실행

```bash
# 개발 모드 (코드 변경 시 자동 재시작)
python main.py

# 또는 직접 uvicorn 사용
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📡 API 엔드포인트

### 기본 정보
- `GET /` - API 기본 정보
- `GET /health` - 헬스 체크
- `GET /docs` - Swagger UI 문서
- `GET /redoc` - ReDoc 문서

### RSS 피드
- `GET /feeds` - 사용 가능한 RSS 피드 목록
- `GET /feeds/all?days_back=7` - 모든 피드에서 최신 게시물 수집
- `GET /feeds/{feed_id}?days_back=7` - 특정 피드 조회

### 일일 소식
- `GET /daily-tip` - 오늘의 AWS 소식 (원문)
- `GET /daily-tip?translate=true` - 오늘의 AWS 소식 (번역)

## 🎯 선별 알고리즘

### 하이브리드 선별 시스템
1. **요일별 우선순위**: 각 요일마다 다른 카테고리를 우선적으로 선별
2. **품질 평가**: 제목 길이, 내용 풍부함, 키워드 매칭 등으로 점수 계산
3. **결정적 선택**: 날짜를 시드로 한 해시 기반 결정적 선택

### 3단계 백업 로직
1. **1차**: 우선 카테고리에서 품질 기준 만족하는 항목 선택
2. **2차**: 모든 카테고리에서 품질 기준 만족하는 항목 선택
3. **3차**: 확장 검색으로 더 낮은 품질 기준 적용

### 요일별 우선순위
- **월요일**: AWS Korea Blog → Architecture → News
- **화요일**: AWS Korea Blog → Security → DevOps
- **수요일**: AWS Korea Blog → DevOps → Open Source
- **목요일**: AWS Korea Blog → News → What's New
- **금요일**: AWS Korea Blog → Architecture → Security
- **토요일**: AWS Korea Blog → Open Source → News
- **일요일**: AWS Korea Blog → What's New → DevOps

## 🔧 설정

### RSS 피드 소스
- AWS News Blog
- AWS Architecture Blog
- AWS DevOps Blog
- AWS Security Blog
- AWS Open Source Blog
- AWS What's New
- **AWS Korea Blog** (우선순위)

### 품질 평가 기준
- 제목 길이 (20-100자 최적)
- 요약 내용 (100자 이상 권장)
- 태그 수 (3개 이상 보너스)
- AWS 키워드 매칭
- 품질 지시어 포함 여부

### 번역 기능
- AWS Translate API 사용
- 영어 자동 감지 (ASCII 비율 70% 이상)
- 텍스트 길이 제한 (5000자)
- 제목 200자, 요약 1000자 제한

## 🐳 Docker 배포

```bash
# Docker 이미지 빌드
docker build -t honeybox .

# 컨테이너 실행
docker run -p 8000:8000 -e ENABLE_TRANSLATION=false honeybox

# 번역 기능과 함께 실행
docker run -p 8000:8000 \
  -e ENABLE_TRANSLATION=true \
  -e AWS_ACCESS_KEY_ID=your_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret \
  honeybox
```

## 📊 모니터링

### 로그 레벨
- 기본: INFO 레벨
- 개발: DEBUG 레벨 (상세한 품질 평가 과정)

### 캐시 상태
- 일일 캐시 자동 정리
- 번역/원문 별도 캐시
- 메모리 기반 캐싱

## 🔄 아키텍처 개선 사항

### 이전 버전 대비 개선점
1. **모듈화**: 단일 파일(660줄) → 체계적인 패키지 구조
2. **관심사 분리**: 각 기능별 독립적인 서비스 클래스
3. **테스트 용이성**: 서비스별 단위 테스트 가능
4. **확장성**: 새로운 피드/기능 추가 용이
5. **유지보수성**: 코드 구조 명확화 및 가독성 향상

### 설계 원칙
- **단일 책임 원칙**: 각 클래스/모듈이 하나의 책임만 가짐
- **의존성 주입**: 설정을 통한 유연한 구성
- **계층화 아키텍처**: Router → Service → Utils 구조
- **에러 처리**: 계층별 적절한 예외 처리

## 🤝 기여하기

1. 새로운 RSS 피드 추가: `config.py`의 `AWS_BLOG_FEEDS` 수정
2. 품질 평가 개선: `quality_service.py` 수정
3. 새로운 선별 로직: `selection_service.py` 확장
4. 번역 개선: `translation_service.py` 수정

## 📄 라이선스

MIT License

---

**HoneyBox** - 매일 새로운 AWS 소식을 달콤하게 전해드립니다! 🍯✨ 