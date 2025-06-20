"""
TS Portal 데이터베이스 샘플 데이터 생성 스크립트
"""

import os
import sys
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import Base, get_db
from app.models.member import Member
from app.models.customer import Customer
from app.models.assignment import Assignment
from app.models.event import Event

def create_sample_data():
    """샘플 데이터 생성"""
    
    # 데이터베이스 연결
    engine = create_engine("sqlite:///./data/ts_portal.db")
    Base.metadata.create_all(bind=engine)
    
    db = Session(bind=engine)
    
    try:
        print("✅ 데이터베이스 초기화 완료: /Users/seungdo/work/ts-portal/ts-portal-db/data/ts_portal.db")
        print("🚀 샘플 데이터 생성 시작...")
        
        # 1. 팀원 데이터 생성 (실제 팀 구조 반영)
        print("👥 팀원 데이터 생성 중...")
        
        members = [
            # Leaf 파트
            Member(
                name="이주엽",
                email="juyeop.lee@saltware.co.kr",
                phone="010-1111-0001",
                position="책임",
                team="Leaf",
                skills="AWS, DevOps, CI/CD, Jenkins, Docker",
                join_date=date(2021, 3, 15),
                profile_image="https://via.placeholder.com/150",
                is_active=True
            ),
            Member(
                name="정장훈",
                email="janghun.jung@saltware.co.kr", 
                phone="010-1111-0002",
                position="선임",
                team="Leaf",
                skills="Kubernetes, AWS EKS, Terraform, Python",
                join_date=date(2022, 1, 10),
                profile_image="https://via.placeholder.com/150",
                is_active=True
            ),
            Member(
                name="김이현",
                email="ihyeon.kim@saltware.co.kr",
                phone="010-1111-0003", 
                position="주임",
                team="Leaf",
                skills="Frontend, Vue.js, React, TypeScript",
                join_date=date(2023, 6, 1),
                profile_image="https://via.placeholder.com/150",
                is_active=True
            ),
            Member(
                name="임종현",
                email="jonghyeon.lim@saltware.co.kr",
                phone="010-1111-0004",
                position="사원",
                team="Leaf", 
                skills="Backend, Node.js, Python, Database",
                join_date=date(2024, 2, 15),
                profile_image="https://via.placeholder.com/150",
                is_active=True
            ),
            
            # Tiger 파트
            Member(
                name="김범중",
                email="beomjung.kim@saltware.co.kr",
                phone="010-2222-0001",
                position="책임",
                team="Tiger",
                skills="AWS Solutions Architecture, MSA, Spring Boot",
                join_date=date(2020, 8, 1),
                profile_image="https://via.placeholder.com/150",
                is_active=True
            ),
            Member(
                name="김성호",
                email="seongho.kim@saltware.co.kr",
                phone="010-2222-0002",
                position="선임", 
                team="Tiger",
                skills="Cloud Infrastructure, AWS, Monitoring",
                join_date=date(2021, 11, 20),
                profile_image="https://via.placeholder.com/150",
                is_active=True
            ),
            Member(
                name="이용태",
                email="yongtae.lee@saltware.co.kr",
                phone="010-2222-0003",
                position="선임",
                team="Tiger",
                skills="DevSecOps, Security, Compliance, AWS Security",
                join_date=date(2022, 4, 10),
                profile_image="https://via.placeholder.com/150",
                is_active=True
            ),
            Member(
                name="배승도",
                email="seungdo.bae@saltware.co.kr",
                phone="010-2222-0004",
                position="선임",
                team="Tiger",
                skills="AWS, Kubernetes, Terraform, Python, EKS",
                join_date=date(2022, 3, 15),
                profile_image="https://via.placeholder.com/150",
                is_active=True
            ),
            Member(
                name="서채운",
                email="chaewoon.seo@saltware.co.kr",
                phone="010-2222-0005",
                position="주임",
                team="Tiger",
                skills="Cloud Native, Kubernetes, GitOps, ArgoCD",
                join_date=date(2023, 9, 1),
                profile_image="https://via.placeholder.com/150",
                is_active=True
            ),
            
            # Aqua 파트  
            Member(
                name="김희수",
                email="heesu.kim@saltware.co.kr",
                phone="010-3333-0001",
                position="책임",
                team="Aqua",
                skills="Data Engineering, Big Data, Apache Spark, Kafka",
                join_date=date(2020, 5, 15),
                profile_image="https://via.placeholder.com/150",
                is_active=True
            ),
            Member(
                name="정지우",
                email="jiwoo.jung@saltware.co.kr",
                phone="010-3333-0002",
                position="선임",
                team="Aqua", 
                skills="Machine Learning, AI/ML, Python, TensorFlow",
                join_date=date(2021, 7, 1),
                profile_image="https://via.placeholder.com/150",
                is_active=True
            ),
            Member(
                name="권하빈",
                email="habin.kwon@saltware.co.kr",
                phone="010-3333-0003",
                position="주임",
                team="Aqua",
                skills="Data Analytics, SQL, Business Intelligence",
                join_date=date(2023, 3, 20),
                profile_image="https://via.placeholder.com/150",
                is_active=True
            ),
            Member(
                name="조수현",
                email="suhyeon.cho@saltware.co.kr",
                phone="010-3333-0004",
                position="사원",
                team="Aqua",
                skills="Data Visualization, Tableau, Power BI, Python",
                join_date=date(2024, 1, 8),
                profile_image="https://via.placeholder.com/150",
                is_active=True
            ),
            
            # 상무님 (파트 없음)
            Member(
                name="함인용",
                email="inyong.ham@saltware.co.kr",
                phone="010-9999-0001",
                position="상무",
                team="TS팀",
                skills="Business Strategy, Technology Leadership, Digital Transformation",
                join_date=date(2018, 1, 1),
                profile_image="https://via.placeholder.com/150",
                is_active=True
            )
        ]
        
        for member in members:
            db.add(member)
            
        db.commit()
        print(f"✅ {len(members)}명의 팀원 데이터 생성 완료")
        
        # 2. 고객사 데이터 생성 (실제 업무에 맞게 수정)
        print("🏢 고객사 데이터 생성 중...")
        
        customers = [
            Customer(
                company_name="네이버클라우드플랫폼",
                contact_person="김클라우드",
                contact_email="cloud.kim@ncp.com",
                contact_phone="02-1234-5678",
                contract_type="Full MSP",
                contract_start=date(2024, 1, 1),
                contract_end=date(2024, 12, 31),
                status="Active",
                notes="클라우드 네이티브 전환 프로젝트. Kubernetes 기반 MSA 구축"
            ),
            Customer(
                company_name="카카오엔터프라이즈",
                contact_person="이엔터",
                contact_email="enterprise.lee@kakao.com", 
                contact_phone="02-2345-6789",
                contract_type="Consulting",
                contract_start=date(2024, 3, 15),
                contract_end=date(2024, 9, 15),
                status="Active",
                notes="AI/ML 플랫폼 구축 컨설팅. AWS Bedrock 및 SageMaker 활용"
            ),
            Customer(
                company_name="삼성SDS",
                contact_person="박솔루션",
                contact_email="solution.park@samsungsds.com",
                contact_phone="02-3456-7890",
                contract_type="Support",
                contract_start=date(2023, 10, 1),
                contract_end=date(2025, 9, 30),
                status="Active",
                notes="클라우드 인프라 24/7 운영 지원. 멀티 클라우드 환경 관리"
            ),
            Customer(
                company_name="LG CNS",
                contact_person="최디지털",
                contact_email="digital.choi@lgcns.com",
                contact_phone="02-4567-8901",
                contract_type="Project",
                contract_start=date(2024, 6, 1),
                contract_end=date(2024, 11, 30),
                status="Active",
                notes="디지털 트랜스포메이션 프로젝트. 레거시 시스템 클라우드 마이그레이션"
            ),
            Customer(
                company_name="SK텔레콤",
                contact_person="정텔레콤",
                contact_email="telecom.jung@sktelecom.com",
                contact_phone="02-5678-9012",
                contract_type="Full MSP",
                contract_start=date(2023, 7, 1),
                contract_end=date(2024, 6, 30),
                status="Expired",
                notes="5G 서비스 플랫폼 클라우드 운영. 계약 갱신 협의 중"
            ),
            Customer(
                company_name="현대오토에버",
                contact_person="김오토",
                contact_email="auto.kim@hyundai-autoever.com",
                contact_phone="02-6789-0123",
                contract_type="Consulting",
                contract_start=date(2024, 4, 1),
                contract_end=date(2024, 10, 31),
                status="Active",
                notes="자동차 소프트웨어 플랫폼 클라우드 구축. DevOps 체계 수립"
            )
        ]
        
        for customer in customers:
            db.add(customer)
            
        db.commit()
        print(f"✅ {len(customers)}개 고객사 데이터 생성 완료")
        
        # 3. 담당 배정 데이터 생성 (실제 팀 구조 반영)
        print("📋 담당 배정 데이터 생성 중...")
        
        # 팀원과 고객사 ID 조회
        ham_sangmu = db.query(Member).filter(Member.name == "함인용").first()
        
        # Leaf 파트
        lee_juyeop = db.query(Member).filter(Member.name == "이주엽").first()
        jung_janghun = db.query(Member).filter(Member.name == "정장훈").first()
        kim_ihyeon = db.query(Member).filter(Member.name == "김이현").first()
        lim_jonghyeon = db.query(Member).filter(Member.name == "임종현").first()
        
        # Tiger 파트
        kim_beomjung = db.query(Member).filter(Member.name == "김범중").first()
        kim_seongho = db.query(Member).filter(Member.name == "김성호").first()
        lee_yongtae = db.query(Member).filter(Member.name == "이용태").first()
        bae_seungdo = db.query(Member).filter(Member.name == "배승도").first()
        seo_chaewoon = db.query(Member).filter(Member.name == "서채운").first()
        
        # Aqua 파트
        kim_heesu = db.query(Member).filter(Member.name == "김희수").first()
        jung_jiwoo = db.query(Member).filter(Member.name == "정지우").first()
        kwon_habin = db.query(Member).filter(Member.name == "권하빈").first()
        cho_suhyeon = db.query(Member).filter(Member.name == "조수현").first()
        
        # 고객사
        ncp = db.query(Customer).filter(Customer.company_name == "네이버클라우드플랫폼").first()
        kakao = db.query(Customer).filter(Customer.company_name == "카카오엔터프라이즈").first()
        samsung = db.query(Customer).filter(Customer.company_name == "삼성SDS").first()
        lg = db.query(Customer).filter(Customer.company_name == "LG CNS").first()
        skt = db.query(Customer).filter(Customer.company_name == "SK텔레콤").first()
        hyundai = db.query(Customer).filter(Customer.company_name == "현대오토에버").first()
        
        assignments = [
            # 네이버클라우드플랫폼 - Tiger 파트 주도
            Assignment(
                member_id=kim_beomjung.id,
                customer_id=ncp.id,
                role="Primary",
                assigned_date=date(2024, 1, 1),
                is_primary=True,
                responsibilities="전체 프로젝트 리드, 아키텍처 설계, 고객 관계 관리"
            ),
            Assignment(
                member_id=bae_seungdo.id,
                customer_id=ncp.id,
                role="Secondary",
                assigned_date=date(2024, 1, 1),
                is_primary=False,
                responsibilities="EKS 클러스터 구축, Kubernetes 운영, CI/CD 파이프라인"
            ),
            
            # 카카오엔터프라이즈 - Aqua 파트 주도
            Assignment(
                member_id=kim_heesu.id,
                customer_id=kakao.id,
                role="Primary", 
                assigned_date=date(2024, 3, 15),
                is_primary=True,
                responsibilities="AI/ML 플랫폼 아키텍처 설계, 데이터 파이프라인 구축"
            ),
            Assignment(
                member_id=jung_jiwoo.id,
                customer_id=kakao.id,
                role="Secondary",
                assigned_date=date(2024, 3, 15),
                is_primary=False,
                responsibilities="ML 모델 서빙, SageMaker 구축, 모델 최적화"
            ),
            
            # 삼성SDS - Leaf 파트 주도
            Assignment(
                member_id=lee_juyeop.id,
                customer_id=samsung.id,
                role="Primary",
                assigned_date=date(2023, 10, 1),
                is_primary=True,
                responsibilities="인프라 운영 총괄, DevOps 체계 구축, 모니터링"
            ),
            Assignment(
                member_id=jung_janghun.id,
                customer_id=samsung.id,
                role="Secondary",
                assigned_date=date(2023, 10, 1),
                is_primary=False,
                responsibilities="Terraform 인프라 코드 관리, 자동화 스크립트 개발"
            ),
            
            # LG CNS - Tiger + Leaf 협업
            Assignment(
                member_id=kim_seongho.id,
                customer_id=lg.id,
                role="Primary",
                assigned_date=date(2024, 6, 1),
                is_primary=True,
                responsibilities="클라우드 마이그레이션 계획 수립, 인프라 구축"
            ),
            Assignment(
                member_id=kim_ihyeon.id,
                customer_id=lg.id,
                role="Secondary",
                assigned_date=date(2024, 6, 1),
                is_primary=False,
                responsibilities="프론트엔드 애플리케이션 마이그레이션, UI/UX 개선"
            ),
            
            # 현대오토에버 - Tiger 파트
            Assignment(
                member_id=lee_yongtae.id,
                customer_id=hyundai.id,
                role="Primary",
                assigned_date=date(2024, 4, 1),
                is_primary=True,
                responsibilities="보안 체계 구축, DevSecOps 파이프라인, 컴플라이언스"
            ),
            Assignment(
                member_id=seo_chaewoon.id,
                customer_id=hyundai.id,
                role="Secondary",
                assigned_date=date(2024, 4, 1),
                is_primary=False,
                responsibilities="GitOps 구축, ArgoCD 운영, 배포 자동화"
            )
        ]
        
        for assignment in assignments:
            db.add(assignment)
            
        db.commit()
        print(f"✅ {len(assignments)}개 담당 배정 데이터 생성 완료")
        
        # 4. 팀 일정 데이터 생성 (실제 팀 구조 반영)
        print("📅 팀 일정 데이터 생성 중...")
        
        # 2025년 5월, 6월, 7월에 다양한 이벤트 생성
        events = [
            # === 2025년 5월 이벤트들 ===
            Event(
                title="TS팀 전체 회의",
                description="월간 전체 회의 - 프로젝트 현황 공유 및 이슈 논의",
                event_type="meeting",
                start_time=datetime(2025, 5, 6, 10, 0),
                end_time=datetime(2025, 5, 6, 11, 30),
                location="대회의실",
                created_by=ham_sangmu.id,
                all_day=False,
                participants="전체 팀원"
            ),
            Event(
                title="함인용 상무 - 임원 회의",
                description="월간 임원 회의 참석",
                event_type="meeting",
                start_time=datetime(2025, 5, 7, 14, 0),
                end_time=datetime(2025, 5, 7, 16, 0),
                location="임원 회의실",
                created_by=ham_sangmu.id,
                all_day=False,
                participants="임원진"
            ),
            Event(
                title="이주엽 - 연차",
                description="개인 휴가",
                event_type="vacation",
                start_time=datetime(2025, 5, 8, 0, 0),
                end_time=datetime(2025, 5, 9, 23, 59),
                location="",
                created_by=lee_juyeop.id,
                all_day=True
            ),
            Event(
                title="AWS re:Invent 2025 준비 회의",
                description="올해 AWS re:Invent 참석 계획 및 세션 선정",
                event_type="meeting",
                start_time=datetime(2025, 5, 12, 14, 0),
                end_time=datetime(2025, 5, 12, 15, 30),
                location="회의실 B",
                created_by=kim_beomjung.id,
                all_day=False,
                participants="Tiger 파트 전체"
            ),
            Event(
                title="김성호 - 재택근무",
                description="집중 개발 업무",
                event_type="remote",
                start_time=datetime(2025, 5, 14, 9, 0),
                end_time=datetime(2025, 5, 14, 18, 0),
                location="자택",
                created_by=kim_seongho.id,
                all_day=True
            ),
            Event(
                title="네이버클라우드플랫폼 고객사 미팅",
                description="Q3 인프라 확장 계획 논의 및 아키텍처 리뷰",
                event_type="meeting",
                start_time=datetime(2025, 5, 15, 15, 0),
                end_time=datetime(2025, 5, 15, 16, 30),
                location="NCP 본사",
                created_by=kim_beomjung.id,
                all_day=False,
                participants="김범중, 배승도, NCP 개발팀"
            ),
            Event(
                title="Terraform 모듈화 교육",
                description="인프라 코드 모듈화 및 베스트 프랙티스 교육",
                event_type="education",
                start_time=datetime(2025, 5, 20, 13, 0),
                end_time=datetime(2025, 5, 20, 17, 0),
                location="교육실",
                created_by=jung_janghun.id,
                all_day=False,
                participants="Leaf 파트, Tiger 파트"
            ),
            Event(
                title="권하빈 - 대전 출장",
                description="고객사 데이터 분석 프로젝트 지원",
                event_type="business_trip",
                start_time=datetime(2025, 5, 22, 9, 0),
                end_time=datetime(2025, 5, 23, 18, 0),
                location="대전",
                created_by=kwon_habin.id,
                all_day=True
            ),

            # === 2025년 6월 이벤트들 ===
            Event(
                title="TS팀 전체 회의",
                description="월간 전체 회의 - 상반기 성과 점검",
                event_type="meeting",
                start_time=datetime(2025, 6, 3, 10, 0),
                end_time=datetime(2025, 6, 3, 11, 30),
                location="대회의실",
                created_by=ham_sangmu.id,
                all_day=False,
                participants="전체 팀원"
            ),
            Event(
                title="AWS 신규 서비스 교육",
                description="Amazon Bedrock 및 생성형 AI 서비스 교육",
                event_type="education",
                start_time=datetime(2025, 6, 5, 14, 0),
                end_time=datetime(2025, 6, 5, 17, 0),
                location="온라인 (Zoom)",
                created_by=kim_heesu.id,
                all_day=False,
                participants="Aqua 파트 전체"
            ),
            Event(
                title="김희수 - 연차",
                description="가족 여행",
                event_type="vacation",
                start_time=datetime(2025, 6, 9, 0, 0),
                end_time=datetime(2025, 6, 11, 23, 59),
                location="",
                created_by=kim_heesu.id,
                all_day=True
            ),
            Event(
                title="EKS 운영 심화 교육",
                description="Kubernetes 클러스터 운영 및 트러블슈팅 교육",
                event_type="education",
                start_time=datetime(2025, 6, 12, 13, 0),
                end_time=datetime(2025, 6, 12, 15, 0),
                location="교육실",
                created_by=bae_seungdo.id,
                all_day=False,
                participants="Tiger 파트, Leaf 파트"
            ),
            Event(
                title="이용태 - 부산 출장",
                description="부산 지역 고객사 보안 컨설팅",
                event_type="business_trip",
                start_time=datetime(2025, 6, 16, 9, 0),
                end_time=datetime(2025, 6, 17, 18, 0),
                location="부산",
                created_by=lee_yongtae.id,
                all_day=True
            ),
            Event(
                title="카카오엔터프라이즈 프로젝트 검토",
                description="AI/ML 플랫폼 구축 진행 상황 점검",
                event_type="project",
                start_time=datetime(2025, 6, 18, 14, 0),
                end_time=datetime(2025, 6, 18, 16, 0),
                location="카카오 판교 오피스",
                created_by=kim_heesu.id,
                all_day=False,
                participants="김희수, 정지우, 카카오 AI팀"
            ),
            Event(
                title="정장훈 - 재택근무",
                description="인프라 코드 리팩토링 작업",
                event_type="remote",
                start_time=datetime(2025, 6, 20, 9, 0),
                end_time=datetime(2025, 6, 20, 18, 0),
                location="자택",
                created_by=jung_janghun.id,
                all_day=True
            ),
            Event(
                title="AWS Well-Architected 리뷰",
                description="고객사 인프라 아키텍처 검토 및 개선안 도출",
                event_type="meeting",
                start_time=datetime(2025, 6, 23, 10, 0),
                end_time=datetime(2025, 6, 23, 12, 0),
                location="회의실 C",
                created_by=kim_beomjung.id,
                all_day=False,
                participants="Tiger 파트 전체"
            ),
            Event(
                title="상반기 팀 워크샵",
                description="팀 빌딩 및 하반기 계획 수립",
                event_type="meeting",
                start_time=datetime(2025, 6, 26, 9, 0),
                end_time=datetime(2025, 6, 26, 18, 0),
                location="연수원",
                created_by=ham_sangmu.id,
                all_day=True,
                participants="전체 팀원"
            ),

            # === 2025년 7월 이벤트들 ===
            Event(
                title="TS팀 전체 회의",
                description="월간 전체 회의 - 하반기 사업 계획 공유",
                event_type="meeting",
                start_time=datetime(2025, 7, 1, 10, 0),
                end_time=datetime(2025, 7, 1, 11, 30),
                location="대회의실",
                created_by=ham_sangmu.id,
                all_day=False,
                participants="전체 팀원"
            ),
            Event(
                title="조수현 - 여름휴가",
                description="여름 휴가",
                event_type="vacation",
                start_time=datetime(2025, 7, 3, 0, 0),
                end_time=datetime(2025, 7, 7, 23, 59),
                location="",
                created_by=cho_suhyeon.id,
                all_day=True
            ),
            Event(
                title="컨테이너 보안 교육",
                description="Kubernetes 보안 강화 및 컨테이너 보안 교육",
                event_type="education",
                start_time=datetime(2025, 7, 10, 9, 0),
                end_time=datetime(2025, 7, 10, 17, 0),
                location="교육실",
                created_by=lee_yongtae.id,
                all_day=False,
                participants="전체 팀원"
            ),
            Event(
                title="삼성SDS 정기 점검",
                description="인프라 상태 점검 및 성능 최적화",
                event_type="project",
                start_time=datetime(2025, 7, 14, 13, 0),
                end_time=datetime(2025, 7, 14, 17, 0),
                location="삼성SDS IDC",
                created_by=lee_juyeop.id,
                all_day=False,
                participants="이주엽, 정장훈"
            ),
            Event(
                title="김이현 - 재택근무",
                description="프론트엔드 개발 집중 업무",
                event_type="remote",
                start_time=datetime(2025, 7, 16, 9, 0),
                end_time=datetime(2025, 7, 16, 18, 0),
                location="자택",
                created_by=kim_ihyeon.id,
                all_day=True
            ),
            Event(
                title="FinOps 워크샵",
                description="클라우드 비용 최적화 및 FinOps 전략 수립",
                event_type="education",
                start_time=datetime(2025, 7, 18, 14, 0),
                end_time=datetime(2025, 7, 18, 17, 0),
                location="회의실 B",
                created_by=ham_sangmu.id,
                all_day=False,
                participants="파트장급 이상"
            ),
            Event(
                title="서채운 - AWS Summit 참석",
                description="AWS Summit Korea 2025 참석",
                event_type="business_trip",
                start_time=datetime(2025, 7, 22, 9, 0),
                end_time=datetime(2025, 7, 22, 18, 0),
                location="코엑스",
                created_by=seo_chaewoon.id,
                all_day=False,
                participants="서채운"
            ),
            Event(
                title="Q2 성과 발표",
                description="2분기 프로젝트 성과 발표 및 Q3 계획 수립",
                event_type="meeting",
                start_time=datetime(2025, 7, 25, 14, 0),
                end_time=datetime(2025, 7, 25, 17, 0),
                location="대회의실",
                created_by=ham_sangmu.id,
                all_day=False,
                participants="전체 팀원"
            ),
            Event(
                title="여름 휴가 일정 조율",
                description="팀원별 여름 휴가 일정 최종 조율",
                event_type="meeting",
                start_time=datetime(2025, 7, 29, 15, 0),
                end_time=datetime(2025, 7, 29, 16, 0),
                location="회의실 A",
                created_by=ham_sangmu.id,
                all_day=False,
                participants="전체 팀원"
            )
        ]
        
        for event in events:
            db.add(event)
            
        db.commit()
        print(f"✅ {len(events)}개 팀 일정 데이터 생성 완료")
        
        print("\n🎉 모든 샘플 데이터 생성이 완료되었습니다!")
        print("\n📊 생성된 데이터 요약:")
        print(f"   👥 팀원: {len(members)}명")
        print(f"      - Leaf 파트: 4명 (이주엽, 정장훈, 김이현, 임종현)")
        print(f"      - Tiger 파트: 5명 (김범중, 김성호, 이용태, 배승도, 서채운)")
        print(f"      - Aqua 파트: 4명 (김희수, 정지우, 권하빈, 조수현)")
        print(f"      - 상무: 1명 (함인용)")
        print(f"   🏢 고객사: {len(customers)}개")
        print(f"   📋 담당 배정: {len(assignments)}개")
        print(f"   📅 팀 일정: {len(events)}개")
        print("\n🔗 확인 방법:")
        print("   - API 통계: http://localhost:8001/stats")
        print("   - API 문서: http://localhost:8001/docs")
        print("   - 팀 대시보드: http://localhost:5173/dashboard")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data() 