locals {
  # resource name
  name = "ts-portal"
  region      = "ap-northeast-2"
  account_id  = data.aws_caller_identity.current.account_id
  tags = {
    Terraform = "true"
  }
}

# Terraform을 실행한 AWS 자격증명 정보 받아오기
data "aws_caller_identity" "current" {}

# Route53 호스트존
data "aws_route53_zone" "seungdobae" {
  name = "seungdobae.com."
}
