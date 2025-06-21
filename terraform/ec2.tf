# 최신 Amazon Linux 2023 AMI 조회
data "aws_ami" "amazon_linux_2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# 기본 VPC 조회
data "aws_vpc" "default" {
  default = true
}

# 기본 서브넷 조회
data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# EC2 인스턴스 IAM 역할
resource "aws_iam_role" "ec2_role" {
  name = "${local.name}-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = local.tags
}

# SSM 관리 정책 연결
resource "aws_iam_role_policy_attachment" "ssm_managed_instance_core" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# CloudWatch Agent 정책 연결
resource "aws_iam_role_policy_attachment" "cloudwatch_agent_server_policy" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}

# S3 버킷 읽기/쓰기 정책
resource "aws_iam_role_policy" "s3_access" {
  name = "${local.name}-s3-access"
  role = aws_iam_role.ec2_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::ts-portal.seungdobae.com",
          "arn:aws:s3:::ts-portal.seungdobae.com/*"
        ]
      }
    ]
  })
}

# EC2 인스턴스 프로파일
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "${local.name}-ec2-profile"
  role = aws_iam_role.ec2_role.name

  tags = local.tags
}

# 보안 그룹
resource "aws_security_group" "ec2_sg" {
  name_prefix = "${local.name}-ec2-"
  description = "Security group for TS Portal EC2 instance"
  vpc_id      = data.aws_vpc.default.id

  # HTTP 인바운드
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTPS 인바운드
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # SSH 인바운드 (관리용 - 필요시 IP 제한)
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # 필요시 특정 IP로 제한
  }

  # 아웃바운드 모든 트래픽 허용
  egress {
    description = "All outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.tags, {
    Name = "${local.name}-ec2-sg"
  })
}

# EC2 인스턴스
resource "aws_instance" "ts_portal" {
  ami                    = data.aws_ami.amazon_linux_2023.id
  instance_type          = "t3.small"
  key_name              = "seungdobae"
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]
  subnet_id             = data.aws_subnets.default.ids[0]
  iam_instance_profile  = aws_iam_instance_profile.ec2_profile.name

  # 루트 볼륨 설정 (gp3 20GB)
  root_block_device {
    volume_type           = "gp3"
    volume_size           = 30
    delete_on_termination = true
    encrypted             = true
    
    tags = merge(local.tags, {
      Name = "${local.name}-root-volume"
    })
  }

  # 메타데이터 설정 (보안 강화)
  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
    http_put_response_hop_limit = 1
  }

  tags = merge(local.tags, {
    Name = "${local.name}-ec2"
    Environment = "production"
    Service = "ts-portal-backend"
  })

  lifecycle {
    create_before_destroy = true
  }
}

# Elastic IP (고정 IP 필요시)
resource "aws_eip" "ts_portal" {
  instance = aws_instance.ts_portal.id
  domain   = "vpc"

  tags = merge(local.tags, {
    Name = "${local.name}-eip"
  })

  depends_on = [aws_instance.ts_portal]
} 