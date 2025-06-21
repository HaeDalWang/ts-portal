# TS Portal EC2 Infrastructure 🏗️

Terraform을 사용한 TS Portal 백엔드 서비스용 EC2 인프라 구성

## 📋 인프라 구성

### EC2 인스턴스
- **인스턴스 타입**: t3.small (2 vCPU, 2GB RAM)
- **OS**: Amazon Linux 2023
- **스토리지**: 30GB gp3 (암호화 적용)
- **키페어**: seungdobae
- **Elastic IP**: 고정 IP 할당
- **도메인**: tsapi.seungdobae.com

### IAM 권한
- **SSM**: Systems Manager 접근 (원격 관리)
- **CloudWatch**: 모니터링 에이전트
- **S3**: ts-portal.seungdobae.com 버킷 읽기/쓰기

### 보안 그룹
- **인바운드**: HTTP(80), HTTPS(443), SSH(22)
- **아웃바운드**: 모든 트래픽 허용

### 백엔드 설정
- **State 저장**: S3 버킷 `ts-portal.seungdobae.com`
- **State 잠금**: DynamoDB 테이블 `ts-portal`

## 🚀 배포 방법

### 1. 초기 설정

```bash
cd ts-portal/terraform

# Terraform 초기화
terraform init

# 계획 확인
terraform plan
```

### 2. 인프라 배포

```bash
# 인프라 생성
terraform apply

# 확인 후 'yes' 입력
```

### 3. 배포 완료 후 출력 확인

```bash
# 출력 값 확인
terraform output

# 예시 출력:
# ec2_public_ip = "3.35.123.456"
# ssh_command = "ssh -i ~/.ssh/seungdobae.pem ec2-user@3.35.123.456"
# ssm_command = "aws ssm start-session --target i-1234567890abcdef0 --region ap-northeast-2"
```

## 🔧 EC2 접속 방법

### SSH 접속
```bash
# 키페어 파일 권한 설정 (최초 1회)
chmod 400 ~/.ssh/seungdobae.pem

# SSH 접속
ssh -i ~/.ssh/seungdobae.pem ec2-user@[PUBLIC_IP]
```

### SSM Session Manager 접속 (권장)
```bash
# AWS CLI 설정 필요
aws ssm start-session --target [INSTANCE_ID] --region ap-northeast-2
```

## 📦 Docker 환경 설정

EC2 접속 후 다음 명령어로 Docker 환경을 구성하세요:

```bash
# Docker 설치
sudo yum update -y
sudo yum install -y docker git
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user

# Docker Compose 설치
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 재로그인 (Docker 그룹 권한 적용)
exit
```

## 🌐 TS Portal 서비스 배포

```bash
# 프로젝트 디렉토리 생성
mkdir -p /home/ec2-user/ts-portal
cd /home/ec2-user/ts-portal

# 소스코드 업로드 (Git 또는 scp)
git clone [YOUR_REPO] .

# 또는 로컬에서 scp로 업로드
# scp -i ~/.ssh/seungdobae.pem -r ./ts-portal ec2-user@[PUBLIC_IP]:/home/ec2-user/

# 디렉토리 구조 설정
./setup-directories.sh

# SSL 인증서 설정
./ssl-setup.sh

# 서비스 시작
docker-compose up -d
```

## 📊 리소스 정보

### 예상 비용 (서울 리전)
- **EC2 t3.small**: ~$16.8/월
- **EBS gp3 30GB**: ~$2.4/월
- **Elastic IP**: 무료 (인스턴스 연결 시)
- **Route53 A 레코드**: ~$0.5/월
- **총 예상 비용**: ~$19.7/월

### 성능 사양
- **CPU**: 2 vCPU (버스트 가능)
- **메모리**: 2GB
- **네트워크**: 최대 5Gbps
- **스토리지**: 30GB gp3 (3,000 IOPS)
- **도메인**: tsapi.seungdobae.com

## 🔧 관리 명령어

### Terraform 관리
```bash
# 상태 확인
terraform show

# 특정 리소스 정보 확인
terraform state show aws_instance.ts_portal

# 인프라 수정 (파일 수정 후)
terraform plan
terraform apply

# 인프라 삭제 (주의!)
terraform destroy
```

### EC2 관리
```bash
# 인스턴스 재시작
aws ec2 reboot-instances --instance-ids [INSTANCE_ID] --region ap-northeast-2

# 인스턴스 중지/시작
aws ec2 stop-instances --instance-ids [INSTANCE_ID] --region ap-northeast-2
aws ec2 start-instances --instance-ids [INSTANCE_ID] --region ap-northeast-2
```

## 🚨 주의사항

1. **키페어 보안**: seungdobae.pem 파일을 안전하게 보관하세요
2. **Elastic IP**: 인스턴스 삭제 시 EIP도 함께 해제됩니다
3. **백업**: 중요한 데이터는 S3에 백업하세요
4. **모니터링**: CloudWatch로 인스턴스 상태를 모니터링하세요

## 📈 확장 계획

향후 트래픽 증가 시 다음과 같이 확장 가능합니다:

1. **수직 확장**: t3.medium, t3.large로 인스턴스 타입 변경
2. **수평 확장**: Auto Scaling Group + Application Load Balancer
3. **데이터베이스**: RDS로 SQLite 대체
4. **캐싱**: ElastiCache Redis 클러스터

---

**배포 완료 후 tsapi.seungdobae.com 도메인이 자동으로 설정됩니다!** 🎉

## 🌐 서비스 접속 URL

배포 완료 후 다음 URL로 서비스에 접속할 수 있습니다:

- **HoneyBox API**: https://tsapi.seungdobae.com/api/feeds/
- **TS Portal DB API**: https://tsapi.seungdobae.com/api/db/
- **Health Check**: https://tsapi.seungdobae.com/health

SSL 인증서는 Let's Encrypt를 통해 자동으로 발급됩니다. 