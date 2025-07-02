# TS Portal 리팩토링 계획

## ✅ 완료된 작업
1. **shared/types.py 제거**
   - 실제 사용되지 않는 공통 타입 정의 파일 제거
   - validation 스크립트 수정 완료
   - 각 서비스가 자체적으로 타입 관리하도록 변경

## 🚀 다음 개선 작업

### 1. UserRole Enum 중복 정의 문제
- **현재 상황**: 
  - auth-service/models.py
  - member-service/models.py
  - shared/types.py (삭제됨)
  에서 각각 정의되어 있음
- **개선 방안**:
  - member-service를 source of truth로 지정
  - auth-service는 member-service의 enum 사용
  - 데이터베이스 enum과 동기화

### 2. 데이터베이스 설정 중복
- **현재 상황**: 
  - 6개 서비스가 거의 동일한 database.py 파일 보유
  - DATABASE_URL, pool_size 등 설정 중복
- **개선 방안**:
  - shared/database.py로 공통 설정 추출
  - 환경변수 기반 설정 통합
  - 서비스별 커스텀 설정만 개별 관리

### 3. pyproject.toml 표준화
- **현재 상황**:
  - 서비스마다 다른 개발 도구 설정
  - 일관성 없는 의존성 관리
- **개선 방안**:
  - 공통 개발 도구 설정 템플릿화
  - 의존성 버전 통일
  - CI/CD 파이프라인 통합

### 4. Auth Service Raw SQL 개선
- **현재 상황**:
  - auth-service만 Raw SQL 사용
  - 다른 서비스는 SQLAlchemy ORM 사용
- **개선 방안**:
  - ORM으로 전환
  - 쿼리 성능 최적화
  - 코드 일관성 확보

### 5. Member 모델 중복
- **현재 상황**:
  - auth-service와 member-service에 동일 모델 존재
- **개선 방안**:
  - member-service를 primary 서비스로 지정
  - auth-service는 member-service API 사용
  - 모델 정의 단일화

### 6. feeds-service 아키텍처 개선
- **현재 상황**:
  - 다른 서비스와 다른 아키텍처
  - 상태 저장 없음
- **개선 방안**:
  - 캐싱 레이어 추가
  - 성능 모니터링 추가
  - 에러 처리 강화

### 7. Customer Service FK 문제
- **현재 상황**:
  - member_id를 단순 Integer로 저장
  - 참조 무결성 없음
- **개선 방안**:
  - 이벤트 기반 동기화 도입
  - 멤버 삭제 시 처리 로직 추가
  - 정합성 체크 추가

### 8. JWT 설정 보안 강화
- **현재 상황**:
  - 기본값이 하드코딩됨
  - 보안에 취약한 설정 존재
- **개선 방안**:
  - 환경변수 필수화
  - 시크릿 로테이션 구현
  - 토큰 관리 정책 수립

## 📋 우선순위
1. UserRole Enum 중복 정의 해결 (높음)
2. 데이터베이스 설정 중복 제거 (높음)
3. Member 모델 중복 해결 (높음)
4. JWT 설정 보안 강화 (중간)
5. pyproject.toml 표준화 (중간)
6. Auth Service Raw SQL 개선 (낮음)
7. Customer Service FK 문제 해결 (낮음)
8. feeds-service 아키텍처 개선 (낮음)

## ⚠️ 리스크
- 서비스 간 의존성 변경으로 인한 장애 가능성
- 데이터베이스 스키마 변경 필요
- 배포 프로세스 영향
- 기존 기능 호환성 유지 필요

## 📝 다음 단계
1. UserRole Enum 중복 정의 해결 시작
   - member-service를 source of truth로 지정
   - auth-service의 UserRole 제거
   - 데이터베이스 enum 동기화 확인 