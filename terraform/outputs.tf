# EC2 인스턴스 정보 출력
output "ec2_instance_id" {
  description = "EC2 인스턴스 ID"
  value       = aws_instance.ts_portal.id
}

output "ec2_public_ip" {
  description = "EC2 인스턴스 퍼블릭 IP"
  value       = aws_eip.ts_portal.public_ip
}

output "ec2_private_ip" {
  description = "EC2 인스턴스 프라이빗 IP"
  value       = aws_instance.ts_portal.private_ip
}

output "ec2_public_dns" {
  description = "EC2 인스턴스 퍼블릭 DNS"
  value       = aws_instance.ts_portal.public_dns
}

output "security_group_id" {
  description = "보안 그룹 ID"
  value       = aws_security_group.ec2_sg.id
}

output "iam_role_arn" {
  description = "EC2 IAM 역할 ARN"
  value       = aws_iam_role.ec2_role.arn
}

# SSH 접속 명령어
output "ssh_command" {
  description = "SSH 접속 명령어"
  value       = "ssh -i ~/.ssh/seungdobae.pem ec2-user@${aws_eip.ts_portal.public_ip}"
}

# SSM Session Manager 접속 명령어
output "ssm_command" {
  description = "SSM Session Manager 접속 명령어"
  value       = "aws ssm start-session --target ${aws_instance.ts_portal.id} --region ${local.region}"
} 