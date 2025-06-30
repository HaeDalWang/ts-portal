-- TS Portal 더미 데이터 삽입 스크립트
-- 모든 enum 값은 대문자를 사용합니다 (PostgreSQL enum과 일치)

-- 기존 데이터 삭제 (필요시)
TRUNCATE member_schema.members RESTART IDENTITY CASCADE;

-- 더미 데이터 삽입 (password_hash는 "test123"의 SHA256)
INSERT INTO member_schema.members (name, username, email, password_hash, role, position, team, is_active, created_at, updated_at) VALUES
-- TS팀 (관리자급)
('관리자', 'admin', 'admin@tsportal.com', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'ADMIN', '시스템관리자', 'TS팀', true, NOW(), NOW()),
('함인용', 'haminnyong', 'haminnyong@saltware.co.kr', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'ADMIN', '상무', 'TS팀', true, NOW(), NOW()),

-- Leaf팀 (이주엽 선임매니저 + 3명 매니저)
('이주엽', 'leejuyeop', 'leejuyeop@saltware.co.kr', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'POWER_USER', '선임매니저', 'Leaf팀', true, NOW(), NOW()),
('정장훈', 'jungjanghoon', 'jungjanghoon@saltware.co.kr', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'USER', '매니저', 'Leaf팀', true, NOW(), NOW()),
('김이현', 'kimihyeon', 'kimihyeon@saltware.co.kr', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'USER', '매니저', 'Leaf팀', true, NOW(), NOW()),
('임종현', 'limjonghyeon', 'limjonghyeon@saltware.co.kr', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'USER', '매니저', 'Leaf팀', true, NOW(), NOW()),

-- Tiger팀 (김범중, 김성호 선임매니저 + 3명 매니저)
('김범중', 'kimbeomjung', 'kimbeomjung@saltware.co.kr', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'POWER_USER', '선임매니저', 'Tiger팀', true, NOW(), NOW()),
('김성호', 'kimseongho', 'kimseongho@saltware.co.kr', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'POWER_USER', '선임매니저', 'Tiger팀', true, NOW(), NOW()),
('이용태', 'leeyongtae', 'leeyongtae@saltware.co.kr', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'USER', '매니저', 'Tiger팀', true, NOW(), NOW()),
('배승도', 'baeseungdo', 'baeseungdo@saltware.co.kr', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'USER', '매니저', 'Tiger팀', true, NOW(), NOW()),
('서채운', 'seochaeeun', 'seochaeeun@saltware.co.kr', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'USER', '매니저', 'Tiger팀', true, NOW(), NOW()),

-- Aqua팀 (김희수 선임매니저 + 3명 매니저)
('김희수', 'kimheesu', 'kimheesu@saltware.co.kr', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'POWER_USER', '선임매니저', 'Aqua팀', true, NOW(), NOW()),
('정지우', 'jungjiwoo', 'jungjiwoo@saltware.co.kr', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'USER', '매니저', 'Aqua팀', true, NOW(), NOW()),
('권하빈', 'kwonhabin', 'kwonhabin@saltware.co.kr', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'USER', '매니저', 'Aqua팀', true, NOW(), NOW()),
('조수현', 'josuhyeon', 'josuhyeon@saltware.co.kr', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'USER', '매니저', 'Aqua팀', true, NOW(), NOW());

-- 삽입 결과 확인
SELECT 
    id, 
    name, 
    username, 
    email, 
    role, 
    position, 
    team,
    is_active
FROM member_schema.members 
ORDER BY 
    CASE team 
        WHEN 'TS팀' THEN 1 
        WHEN 'Leaf팀' THEN 2 
        WHEN 'Tiger팀' THEN 3 
        WHEN 'Aqua팀' THEN 4 
    END, 
    CASE role 
        WHEN 'ADMIN' THEN 1 
        WHEN 'POWER_USER' THEN 2 
        WHEN 'USER' THEN 3 
    END; 