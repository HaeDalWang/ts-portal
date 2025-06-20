"""
TS Portal Database API
팀원 프로필, MSP 관리, 팀 대시보드를 위한 데이터베이스 API 서버
"""

import logging
from datetime import datetime
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from .database import get_db, init_db, get_db_info
from .models import Member, Customer, Assignment, Event, Notice
from .routers import members_router, customers_router

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="TS Portal Database API",
    version="1.0.0",
    description="Saltware CSG TS팀 포털을 위한 데이터베이스 API 서버",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 환경에서는 모든 오리진 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CRUD 라우터 등록
from .routers import events as events_router, notices as notices_router

app.include_router(members_router)
app.include_router(customers_router)
app.include_router(events_router.router)
app.include_router(notices_router.router)


@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 데이터베이스 초기화"""
    logger.info("TS Portal Database API 시작 중...")
    init_db()
    logger.info("✅ 데이터베이스 초기화 완료")


@app.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 실행"""
    logger.info("TS Portal Database API 종료")


@app.get("/")
async def root():
    """API 기본 정보"""
    return {
        "message": "TS Portal Database API에 오신 것을 환영합니다!",
        "version": "1.0.0",
        "description": "Saltware CSG TS팀 포털 데이터베이스 API",
        "endpoints": {
            "/": "API 기본 정보",
            "/health": "헬스 체크",
            "/db-info": "데이터베이스 정보",
            "/stats": "데이터베이스 통계",
            "/members": "팀원 목록 조회",
            "/customers": "고객사 목록 조회",
            "/assignments": "담당 배정 목록 조회",
            "/events": "팀 일정 목록 조회",
            "/docs": "API 문서 (Swagger UI)",
            "/redoc": "API 문서 (ReDoc)"
        },
        "features": [
            "팀원 프로필 관리",
            "MSP 고객사 관리", 
            "담당 배정 관리",
            "팀 일정 관리"
        ]
    }


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "TS Portal Database API"
    }


@app.get("/db-info")
async def database_info():
    """데이터베이스 정보 조회"""
    return get_db_info()


@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """데이터베이스 통계 정보"""
    try:
        stats = {
            "members": {
                "total": db.query(Member).count(),
                "active": db.query(Member).filter(Member.is_active == True).count(),
            },
            "customers": {
                "total": db.query(Customer).count(),
                "active": db.query(Customer).filter(Customer.status == "Active").count(),
            },
            "assignments": {
                "total": db.query(Assignment).count(),
                "primary": db.query(Assignment).filter(Assignment.is_primary == True).count(),
            },
            "events": {
                "total": db.query(Event).count(),
                "upcoming": db.query(Event).filter(Event.start_time > datetime.now()).count(),
            }
        }
        return stats
    except Exception as e:
        logger.error(f"통계 조회 중 오류: {e}")
        return {"error": "통계 정보를 가져올 수 없습니다."}


@app.get("/members")
async def get_members(db: Session = Depends(get_db)):
    """팀원 목록 조회"""
    try:
        members = db.query(Member).all()
        return {
            "total": len(members),
            "members": [
                {
                    "id": member.id,
                    "name": member.name,
                    "email": member.email,
                    "phone": member.phone,
                    "position": member.position,
                    "team": member.team,
                    "skills": member.skills_list,
                    "join_date": member.join_date.isoformat() if member.join_date else None,
                    "is_active": member.is_active,
                    "created_at": member.created_at.isoformat()
                }
                for member in members
            ]
        }
    except Exception as e:
        logger.error(f"팀원 조회 중 오류: {e}")
        return {"error": "팀원 정보를 가져올 수 없습니다."}


@app.get("/customers")
async def get_customers(db: Session = Depends(get_db)):
    """고객사 목록 조회"""
    try:
        customers = db.query(Customer).all()
        return {
            "total": len(customers),
            "customers": [
                {
                    "id": customer.id,
                    "company_name": customer.company_name,
                    "contact_person": customer.contact_person,
                    "contact_email": customer.contact_email,
                    "contact_phone": customer.contact_phone,
                    "contract_type": customer.contract_type,
                    "contract_start": customer.contract_start.isoformat() if customer.contract_start else None,
                    "contract_end": customer.contract_end.isoformat() if customer.contract_end else None,
                    "status": customer.status,
                    "notes": customer.notes,
                    "is_active": customer.is_active,
                    "contract_days_remaining": customer.contract_days_remaining,
                    "created_at": customer.created_at.isoformat()
                }
                for customer in customers
            ]
        }
    except Exception as e:
        logger.error(f"고객사 조회 중 오류: {e}")
        return {"error": "고객사 정보를 가져올 수 없습니다."}


@app.get("/assignments")
async def get_assignments(db: Session = Depends(get_db)):
    """담당 배정 목록 조회"""
    try:
        assignments = db.query(Assignment).all()
        return {
            "total": len(assignments),
            "assignments": [
                {
                    "id": assignment.id,
                    "member": {
                        "id": assignment.member.id,
                        "name": assignment.member.name,
                        "position": assignment.member.position
                    },
                    "customer": {
                        "id": assignment.customer.id,
                        "company_name": assignment.customer.company_name,
                        "status": assignment.customer.status
                    },
                    "role": assignment.role,
                    "assigned_date": assignment.assigned_date.isoformat() if assignment.assigned_date else None,
                    "end_date": assignment.end_date.isoformat() if assignment.end_date else None,
                    "is_primary": assignment.is_primary,
                    "is_active": assignment.is_active,
                    "responsibilities": assignment.responsibilities,
                    "duration_days": assignment.duration_days,
                    "created_at": assignment.created_at.isoformat()
                }
                for assignment in assignments
            ]
        }
    except Exception as e:
        logger.error(f"담당 배정 조회 중 오류: {e}")
        return {"error": "담당 배정 정보를 가져올 수 없습니다."}


@app.get("/events")
async def get_events(db: Session = Depends(get_db)):
    """팀 일정 목록 조회"""
    try:
        events = db.query(Event).all()
        return {
            "total": len(events),
            "events": [
                {
                    "id": event.id,
                    "title": event.title,
                    "description": event.description,
                    "event_type": event.event_type,
                    "start_time": event.start_time.isoformat(),
                    "end_time": event.end_time.isoformat(),
                    "location": event.location,
                    "creator": {
                        "id": event.creator.id,
                        "name": event.creator.name,
                        "position": event.creator.position
                    },
                    "duration_minutes": event.duration_minutes,
                    "is_today": event.is_today,
                    "is_upcoming": event.is_upcoming,
                    "is_ongoing": event.is_ongoing,
                    "status": event.status,
                    "created_at": event.created_at.isoformat()
                }
                for event in events
            ]
        }
    except Exception as e:
        logger.error(f"팀 일정 조회 중 오류: {e}")
        return {"error": "팀 일정 정보를 가져올 수 없습니다."}


# 전역 예외 처리
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """전역 예외 처리기"""
    logger.error(f"처리되지 않은 예외: {exc}", exc_info=True)
    return {
        "detail": "내부 서버 오류가 발생했습니다.",
        "error": str(exc)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True) 