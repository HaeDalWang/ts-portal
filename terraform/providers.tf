# 요구되는 테라폼 제공자 목록
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.99.1"
    }
  }
}

provider "aws" {
  region = local.region
}