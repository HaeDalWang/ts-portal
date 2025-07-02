# 🚨 TS Portal 트러블슈팅 가이드

> 문제 발생 시 빠른 해결을 위한 완전한 가이드

## 📋 목차

1. [Calendar Service 문제들](#calendar-service-문제들)
2. [Kong Gateway 문제들](#kong-gateway-문제들)
3. [SQLAlchemy 및 Database 문제들](#sqlalchemy-및-database-문제들)
4. [FastAPI & Pydantic 문제들](#fastapi--pydantic-문제들)
5. [일반적인 Docker 문제들](#일반적인-docker-문제들)
6. [프론트엔드 API 연동 문제들](#프론트엔드-api-연동-문제들)

---

## 🎯 Calendar Service 문제들

### ❌ 문제 1: `column events.participants does not exist`

**증상:**
```bash
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedColumn) 
column events.participants does not exist
```

**원인:**
- SQLAlchemy 모델에서 `@property` 정의된 `participants` 속성이 실제 데이터베이스 컬럼으로 인식됨
- 데이터베이스에는 `attendees` (JSONB) 컬럼만 존재
- Pydantic 스키마에서 `from_attributes = True` 설정 시 모든 모델 속성을 컬럼으로 스캔

**해결 과정:**
1. **모델에서 `@property` 완전 제거**
   ```python
   # ❌ 문제 코드
   @property
   def participants(self):
       return ', '.join(self.attendees) if self.attendees else ''
   
   # ✅ 해결: 완전 제거
   # participants property 삭제
   ```

2. **Service 레이어에서 직접 처리**
   ```python
   def _to_response(self, event: Event) -> EventResponse:
       # 하위 호환성을 위한 participants 문자열 계산
       participants_str = ""
       if event.attendees:
           if isinstance(event.attendees, list):
               participants_str = ', '.join(str(attendee) for attendee in event.attendees if attendee)
       
       return EventResponse(
           # ... 다른 필드들
           participants=participants_str,  # 직접 설정
       )
   ```

3. **컨테이너 완전 재구성**
   ```bash
   # SQLAlchemy 메타데이터 캐시 완전 제거
   docker-compose stop calendar-service
   docker-compose rm -f calendar-service
   docker-compose build calendar-service
   docker-compose up -d calendar-service
   ```

### ❌ 문제 2: `all_day` vs `is_all_day` 필드 불일치

**증상:**
- 프론트엔드에서 `all_day` 사용
- 데이터베이스에서 `is_all_day` 컬럼 사용
- API 호출 시 필드명 불일치로 인한 오류

**해결:**
1. **데이터베이스 스키마에 맞게 통일**
   ```python
   # 모델
   is_all_day = Column(Boolean, default=False)
   
   # 스키마
   is_all_day: bool = Field(default=False)
   
   # 하위 호환성 필드 추가
   all_day: bool = Field(default=False, description="하위 호환용")
   ```

2. **프론트엔드에서 변환 처리**
   ```typescript
   const requestData = {
     ...eventData,
     is_all_day: eventData.is_all_day ?? eventData.all_day ?? false
   }
   ```

### ❌ 문제 3: `end_time` NOT NULL 제약 조건 위반

**증상:**
- 데이터베이스에서 `end_time NOT NULL`
- 스키마에서 `Optional[datetime]`로 정의
- 이벤트 생성 시 500 오류

**해결:**
```python
# ❌ 문제 코드
end_time: Optional[datetime] = Field(None, description="종료 시간")

# ✅ 해결 코드
end_time: datetime = Field(..., description="종료 시간")  # 필수 필드로 변경
```

---

## 🌐 Kong Gateway 문제들

### ❌ 문제 4: Trailing Slash 리다이렉트 문제

**증상:**
```bash
GET /api/events → 307 Temporary Redirect → calendar-service:8000/api/events/
```
- 브라우저에서 internal hostname에 접근 불가
- `Failed to fetch` 오류 발생

**원인:**
- FastAPI의 자동 trailing slash 리다이렉트
- Kong에서 `/api/events`와 `/api/events/` 경로 처리 불일치

**해결:**
```yaml
# kong/kong.yml
- name: calendar-service
  url: http://calendar-service:8000
  routes:
    - name: calendar-routes
      paths: ["/api/events"]
      strip_path: false
      preserve_host: true
      methods: [GET, POST, PUT, DELETE, OPTIONS]
      plugins:
        - name: request-transformer
          config:
            replace:
              uri: "/api/events/"
    - name: calendar-routes-subpath
      paths: ["/api/events/"]
      strip_path: false
      preserve_host: true
      methods: [GET, POST, PUT, DELETE, OPTIONS]
```

**적용:**
```bash
docker-compose restart kong
```

---

## 🗄️ SQLAlchemy 및 Database 문제들

### ❌ 문제 5: 모델과 데이터베이스 스키마 불일치

**체크리스트:**
1. **데이터베이스 스키마 확인**
   ```bash
   docker-compose exec postgres psql -U tsportal -d tsportal -c "\d calendar_schema.events"
   ```

2. **컬럼명 정확히 일치시키기**
   ```python
   # 모델의 모든 Column이 실제 DB 컬럼과 일치해야 함
   attendees = Column(JSONB, nullable=True)  # DB: attendees (jsonb)
   is_all_day = Column(Boolean, default=False)  # DB: is_all_day (boolean)
   end_time = Column(DateTime, nullable=False)  # DB: end_time (NOT NULL)
   ```

3. **@property와 실제 컬럼 구분**
   ```python
   # ✅ 계산된 속성은 @property 사용 가능
   @property
   def duration_minutes(self):
       return int((self.end_time - self.start_time).total_seconds() / 60)
   
   # ❌ 존재하지 않는 DB 컬럼은 @property 사용 금지
   # @property
   # def participants(self):  # DB에 participants 컬럼 없음
   ```

### ❌ 문제 6: SQLAlchemy 메타데이터 캐싱 문제

**증상:**
- 모델 수정 후에도 이전 컬럼 참조 오류 지속
- 컨테이너 재시작만으로는 해결 안됨

**해결:**
```bash
# 1. 완전한 컨테이너 재구성
docker-compose stop calendar-service
docker-compose rm -f calendar-service
docker-compose build calendar-service
docker-compose up -d calendar-service

# 2. 확인
docker-compose logs calendar-service
curl -s "http://localhost:8084/health" | jq
```

---

## 🔧 FastAPI & Pydantic 문제들

### ❌ 문제 7: Pydantic `computed_field` vs SQLAlchemy 충돌

**문제 코드:**
```python
class EventResponse(BaseModel):
    # ... 기본 필드들
    
    @computed_field
    @property
    def participants(self) -> str:
        return ', '.join(self.attendees) if self.attendees else ''
    
    class Config:
        from_attributes = True  # ← 이것이 문제 원인
```

**문제 원인:**
- `from_attributes = True`와 `computed_field`가 충돌
- SQLAlchemy 모델의 모든 속성을 스캔하려고 시도

**해결:**
```python
class EventResponse(BaseModel):
    # 기본 필드들만 정의
    attendees: Optional[List[str]] = None
    
    # 하위 호환성 필드는 service에서 직접 설정
    participants: str = Field(default="", description="하위 호환용")

# service.py에서
def _to_response(self, event: Event) -> EventResponse:
    participants_str = ', '.join(event.attendees) if event.attendees else ''
    return EventResponse(
        attendees=event.attendees,
        participants=participants_str,  # 직접 계산해서 설정
        # ...
    )
```

---

## 🐳 일반적인 Docker 문제들

### 서비스 재시작 명령어 모음

```bash
# 1. 일반적인 재시작
docker-compose restart <service-name>

# 2. 로그 확인
docker-compose logs -f <service-name>

# 3. 특정 서비스만 다시 빌드
docker-compose build <service-name>

# 4. 캐시 없이 완전 재빌드
docker-compose build --no-cache <service-name>

# 5. 완전한 재구성 (권장)
docker-compose stop <service-name>
docker-compose rm -f <service-name>
docker-compose build <service-name>
docker-compose up -d <service-name>

# 6. 전체 시스템 재시작
docker-compose down
docker-compose up -d
```

### 서비스 상태 확인

```bash
# 서비스 상태
docker-compose ps

# 특정 서비스 헬스체크
curl -s "http://localhost:8084/health" | jq

# 로그에서 오류 찾기
docker-compose logs calendar-service | grep -i error

# 실시간 로그 모니터링
docker-compose logs -f calendar-service
```

---

## 🌐 프론트엔드 API 연동 문제들

### ❌ 문제 8: API 호출 시 헤더 누락

**증상:**
```
❌ API 에러 [422]: X-User-ID header required
```

**해결:**
```typescript
// services/api.ts
class KongApiClient {
  async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const headers = {
      'Content-Type': 'application/json',
      'X-User-ID': this.getUserId(),      // 필수 헤더
      'X-User-Role': this.getUserRole(),  // 필수 헤더
      ...options.headers,
    }
    
    const response = await fetch(this.baseUrl + endpoint, {
      ...options,
      headers,
    })
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${await response.text()}`)
    }
    
    return response.json()
  }
}
```

### ❌ 문제 9: 타입 불일치 오류

**해결 방법:**
1. **백엔드 스키마와 프론트엔드 타입 동기화**
   ```typescript
   // types/calendar.ts
   export interface EventResponse {
     // 백엔드 EventResponse와 정확히 일치해야 함
     id: number
     title: string
     is_all_day: boolean  // ← 백엔드와 동일한 필드명
     attendees?: string[] | Record<string, any>[]
     
     // 하위 호환성 필드
     all_day?: boolean
     participants?: string
   }
   ```

2. **API 호출 시 필드 변환**
   ```typescript
   const requestData = {
     ...eventData,
     is_all_day: eventData.is_all_day ?? eventData.all_day ?? false,
     attendees: eventData.attendees || (eventData.participants ? [eventData.participants] : undefined)
   }
   ```

---

## 🚀 문제 해결 프로세스

### 1. 문제 발생 시 체크리스트

1. **로그 확인**
   ```bash
   docker-compose logs -f <문제-서비스>
   ```

2. **서비스 상태 확인**
   ```bash
   docker-compose ps
   curl -s "http://localhost:8084/health"
   ```

3. **데이터베이스 연결 확인**
   ```bash
   docker-compose exec postgres psql -U tsportal -d tsportal -c "SELECT 1"
   ```

4. **Kong 라우팅 확인**
   ```bash
   curl -v "http://localhost:8000/api/events/types"
   ```

### 2. 단계별 문제 해결

1. **경미한 문제**: 서비스 재시작
   ```bash
   docker-compose restart calendar-service
   ```

2. **코드 변경 후**: 리빌드
   ```bash
   docker-compose build calendar-service
   docker-compose restart calendar-service
   ```

3. **심각한 문제**: 완전 재구성
   ```bash
   docker-compose stop calendar-service
   docker-compose rm -f calendar-service
   docker-compose build calendar-service
   docker-compose up -d calendar-service
   ```

4. **전체 시스템 문제**: 전체 재시작
   ```bash
   docker-compose down
   docker-compose up -d
   ```

### 3. 디버깅 팁

```bash
# 1. 실시간 로그 모니터링하면서 API 호출
docker-compose logs -f calendar-service &
curl -H "X-User-ID: 1" -H "X-User-Role: admin" "http://localhost:8000/api/events/stats"

# 2. 데이터베이스 스키마 확인
docker-compose exec postgres psql -U tsportal -d tsportal -c "\d calendar_schema.events"

# 3. Kong 라우팅 테스트
curl -v "http://localhost:8000/api/events/types"

# 4. 직접 서비스 호출 (Kong 우회)
curl -H "X-User-ID: 1" -H "X-User-Role: admin" "http://localhost:8084/api/events/stats"
```

---

## 📝 경험한 주요 문제 요약

### 🔥 2025-07-02 Calendar Service 대규모 수정

**문제:** Calendar Service 500 Internal Server Error 대량 발생

**근본 원인:**
1. SQLAlchemy 모델의 `@property` 속성이 실제 DB 컬럼으로 인식
2. 데이터베이스 스키마와 모델 정의 불일치 (`participants` vs `attendees`)
3. Kong Gateway의 trailing slash 리다이렉트 문제
4. Pydantic `computed_field`와 SQLAlchemy `from_attributes` 충돌

**해결 과정:**
1. ✅ 데이터베이스 스키마 정확히 파악
2. ✅ SQLAlchemy 모델을 DB 스키마와 100% 일치시킴
3. ✅ `@property` 제거하고 service 레이어에서 처리
4. ✅ Kong에 request-transformer 플러그인 추가
5. ✅ 컨테이너 완전 재구성으로 캐시 제거
6. ✅ 하위 호환성 유지하면서 안정성 확보

**결과:** Calendar Service 완전 안정화 ✅

---

**문서 마지막 업데이트**: 2025-07-02  
**작성자**: Seungdo Bae (with AI Assistant)  
**버전**: 1.0.0

> 💡 **팁**: 문제 발생 시 이 문서를 먼저 확인하고, 해결되지 않으면 로그를 첨부하여 문의하세요! 