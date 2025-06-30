-- TS Portal - 팀원 더미 데이터 삽입
-- 생성일: 2025-06-29
-- 설명: TS팀 실제 조직도 기반 더미 데이터

-- 기존 데이터 정리 (개발용)
DELETE FROM member_schema.members WHERE team IN ('Leaf팀', 'Tiger팀', 'Aqua팀', 'TS팀');

-- 비밀번호 해시 (test123 -> SHA256)
-- echo -n "test123" | sha256sum
-- ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae

-- 팀장 (상무)
INSERT INTO member_schema.members (
    name, username, email, password_hash, role, position, team, 
    is_active, join_date, created_at, updated_at
) VALUES (
    '함인용', 'haminnyong', 'haminnyong@saltware.co.kr', 
    'ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae',
    'admin', '상무', 'TS팀', 
    true, '2020-01-01', NOW(), NOW()
);

-- Leaf팀 (4명)
INSERT INTO member_schema.members (
    name, username, email, password_hash, role, position, team, 
    is_active, join_date, created_at, updated_at
) VALUES 
-- 선임매니저
(
    '이주엽', 'leejuyeop', 'leejuyeop@saltware.co.kr',
    'ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae',
    'power_user', '선임매니저', 'Leaf팀',
    true, '2021-03-01', NOW(), NOW()
),
-- 매니저들
(
    '정장훈', 'jungjanghoon', 'jungjanghoon@saltware.co.kr',
    'ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae',
    'user', '매니저', 'Leaf팀',
    true, '2022-01-15', NOW(), NOW()
),
(
    '김이현', 'kimihyeon', 'kimihyeon@saltware.co.kr',
    'ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae',
    'user', '매니저', 'Leaf팀',
    true, '2022-06-01', NOW(), NOW()
),
(
    '임종현', 'limjonghyeon', 'limjonghyeon@saltware.co.kr',
    'ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae',
    'user', '매니저', 'Leaf팀',
    true, '2023-02-01', NOW(), NOW()
);

-- Tiger팀 (5명)
INSERT INTO member_schema.members (
    name, username, email, password_hash, role, position, team, 
    is_active, join_date, created_at, updated_at
) VALUES 
-- 선임매니저들
(
    '김범중', 'kimbeomjung', 'kimbeomjung@saltware.co.kr',
    'ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae',
    'power_user', '선임매니저', 'Tiger팀',
    true, '2020-08-01', NOW(), NOW()
),
(
    '김성호', 'kimseongho', 'kimseongho@saltware.co.kr',
    'ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae',
    'power_user', '선임매니저', 'Tiger팀',
    true, '2021-01-15', NOW(), NOW()
),
-- 매니저들
(
    '이용태', 'leeyongtae', 'leeyongtae@saltware.co.kr',
    'ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae',
    'user', '매니저', 'Tiger팀',
    true, '2022-03-01', NOW(), NOW()
),
(
    '배승도', 'baeseungdo', 'baeseungdo@saltware.co.kr',
    'ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae',
    'user', '매니저', 'Tiger팀',
    true, '2022-07-01', NOW(), NOW()
),
(
    '서채운', 'seochaeeun', 'seochaeeun@saltware.co.kr',
    'ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae',
    'user', '매니저', 'Tiger팀',
    true, '2023-01-01', NOW(), NOW()
);

-- Aqua팀 (4명)
INSERT INTO member_schema.members (
    name, username, email, password_hash, role, position, team, 
    is_active, join_date, created_at, updated_at
) VALUES 
-- 선임매니저
(
    '김희수', 'kimheesu', 'kimheesu@saltware.co.kr',
    'ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae',
    'power_user', '선임매니저', 'Aqua팀',
    true, '2020-11-01', NOW(), NOW()
),
-- 매니저들
(
    '정지우', 'jungjiwoo', 'jungjiwoo@saltware.co.kr',
    'ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae',
    'user', '매니저', 'Aqua팀',
    true, '2022-04-01', NOW(), NOW()
),
(
    '권하빈', 'kwonhabin', 'kwonhabin@saltware.co.kr',
    'ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae',
    'user', '매니저', 'Aqua팀',
    true, '2022-09-01', NOW(), NOW()
),
(
    '조수현', 'josuhyeon', 'josuhyeon@saltware.co.kr',
    'ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae',
    'user', '매니저', 'Aqua팀',
    true, '2023-03-01', NOW(), NOW()
);

-- 기존 admin 계정 업데이트 (개발용)
UPDATE member_schema.members 
SET name = '관리자', position = '시스템관리자', team = 'TS팀'
WHERE username = 'admin';

-- 삽입 결과 확인
SELECT 
    team,
    position,
    name,
    username,
    email,
    role,
    is_active
FROM member_schema.members 
WHERE team IN ('Leaf팀', 'Tiger팀', 'Aqua팀', 'TS팀')
ORDER BY 
    CASE team 
        WHEN 'TS팀' THEN 1 
        WHEN 'Leaf팀' THEN 2 
        WHEN 'Tiger팀' THEN 3 
        WHEN 'Aqua팀' THEN 4 
    END,
    CASE position 
        WHEN '상무' THEN 1 
        WHEN '선임매니저' THEN 2 
        WHEN '매니저' THEN 3 
        WHEN '시스템관리자' THEN 4
    END,
    name;

-- 통계 정보
SELECT 
    team,
    COUNT(*) as 인원수,
    COUNT(CASE WHEN role = 'admin' THEN 1 END) as 관리자,
    COUNT(CASE WHEN role = 'power_user' THEN 1 END) as 파워유저,
    COUNT(CASE WHEN role = 'user' THEN 1 END) as 일반유저
FROM member_schema.members 
WHERE team IN ('Leaf팀', 'Tiger팀', 'Aqua팀', 'TS팀')
GROUP BY team
ORDER BY team; 