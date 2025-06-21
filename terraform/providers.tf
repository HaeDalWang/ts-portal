# 요구되는 테라폼 제공자 목록
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.99.1"
    }
  }
  
  # S3 백엔드 설정
  backend "s3" {
    bucket         = "ts-portal.seungdobae.com"
    key            = "terraform/ec2/terraform.tfstate"
    region         = "ap-northeast-2"
    dynamodb_table = "ts-portal"
    encrypt        = true
  }
}

provider "aws" {
  region = local.region
}