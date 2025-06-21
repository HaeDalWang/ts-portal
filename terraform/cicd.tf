# ################################################################################
# # Role & Policy & Connection
# ################################################################################

# # GitHub에 있는 리포지토리와 연결
# resource "aws_codestarconnections_connection" "this" {
#   name          = "${local.name}-github-connection"
#   provider_type = "GitHub"
# }
# # 코드 파이프라인에서 사용할 버킷
# resource "aws_s3_bucket" "codepipeline" {
#   bucket = "${local.name}-codepipeline-storage"

#   force_destroy = true
# }

# # 코드 파이프라인에서 사용할 IAM 역할
# resource "aws_iam_policy" "codepipeline" {
#   name = "${local.name}-codepipeline-policy"

#   policy = <<-POLICY
#     {
#       "Version": "2012-10-17",
#       "Statement": [
#         {
#           "Action": [
#             "s3:*",
#             "codestar-connections:UseConnection",
#             "codebuild:*"
#           ],
#           "Effect": "Allow",
#           "Resource": "*"
#         }
#       ]
#     }
#   POLICY
# }
# resource "aws_iam_role" "codepipeline" {
#   name = "${local.name}-codepipeline-service-role"
#   path = "/service-role/"

#   assume_role_policy = <<-POLICY
#     {
#       "Version": "2012-10-17",
#       "Statement": [
#         {
#           "Action": "sts:AssumeRole",
#           "Effect": "Allow",
#           "Principal": {
#             "Service": "codepipeline.amazonaws.com"
#           }
#         }
#       ]
#     }
#   POLICY
# }
# resource "aws_iam_role_policy_attachment" "codepipeline" {
#   role       = aws_iam_role.codepipeline.name
#   policy_arn = aws_iam_policy.codepipeline.arn
# }

# # 코드 빌드에서 사용할 IAM 역할
# resource "aws_iam_policy" "codebuild" {
#   name = "${local.name}-codebuild-policy"

#   policy = <<-POLICY
#     {
#       "Version": "2012-10-17",
#       "Statement": [
#         {
#           "Sid": "CloudWatchLogsPolicy",
#           "Effect": "Allow",
#           "Action": [
#             "logs:CreateLogGroup",
#             "logs:CreateLogStream",
#             "logs:PutLogEvents"
#           ],
#           "Resource": "*"
#         },
#         {
#           "Sid": "CodeStartPolicy",
#           "Effect": "Allow",
#           "Action": [
#             "codestar-connections:UseConnection"
#           ],
#           "Resource": "*"
#         },
#         {
#           "Sid": "S3GetObjectPolicy",
#           "Effect": "Allow",
#           "Action": [
#             "s3:GetObject",
#             "s3:GetObjectVersion"
#           ],
#           "Resource": "*"
#         },
#         {
#           "Sid": "S3PutObjectPolicy",
#           "Effect": "Allow",
#           "Action": [
#             "s3:PutObject"
#           ],
#           "Resource": "*"
#         },
#         {
#           "Sid": "ECRPolicy",
#           "Effect": "Allow",
#           "Action": [
#             "ecr:GetDownloadUrlForLayer",
#             "ecr:BatchGetImage",
#             "ecr:BatchCheckLayerAvailability",
#             "ecr:CompleteLayerUpload",
#             "ecr:GetAuthorizationToken",
#             "ecr:InitiateLayerUpload",
#             "ecr:PutImage",
#             "ecr:DescribeImages",
#             "ecr:UploadLayerPart"
#           ],
#           "Resource": "*"
#         },
#         {
#           "Sid": "S3BucketIdentity",
#           "Effect": "Allow",
#           "Action": [
#             "s3:GetBucketAcl",
#             "s3:GetBucketLocation"
#           ],
#           "Resource": "*"
#         },
#         {
#           "Sid": "SecretManagerPolicy",
#           "Effect": "Allow",
#           "Action": [
#             "secretsmanager:GetSecretValue"
#           ],
#           "Resource": "*"
#         },
#         {
#           "Sid": "CodePipelinePolicy",
#           "Effect": "Allow",
#           "Action": [
#             "codepipeline:ListPipelineExecutions"
#           ],
#           "Resource": "*"
#         },
#         {
#           "Sid": "STSPolicy",
#           "Effect": "Allow",
#           "Action": [
#             "sts:AssumeRole"
#           ],
#           "Resource": "*"
#         },
#         {
#           "Sid": "VpcPolicy",
#           "Effect": "Allow",
#           "Action": [
#             "ec2:CreateNetworkInterface",
#             "ec2:DescribeDhcpOptions",
#             "ec2:DescribeNetworkInterfaces",
#             "ec2:DeleteNetworkInterface",
#             "ec2:DescribeSubnets",
#             "ec2:DescribeSecurityGroups",
#             "ec2:DescribeVpcs",
#             "ec2:CreateNetworkInterfacePermission"
#           ],
#           "Resource": "*"
#         }
#       ]
#     }
#   POLICY
# }
# # 코드 빌드에서 사용할 IAM 역할
# resource "aws_iam_role" "codebuild" {
#   name = "${local.name}-codebuild-service-role"
#   path = "/service-role/"

#   assume_role_policy = <<-POLICY
#     {
#       "Version": "2012-10-17",
#       "Statement": [
#         {
#           "Effect": "Allow",
#           "Principal": {
#             "Service": "codebuild.amazonaws.com"
#           },
#           "Action": "sts:AssumeRole"
#         }
#       ]
#     }
#   POLICY

#   lifecycle {
#     ignore_changes = [
#       # 자동으로 추가되는 정책 삭제 방지
#       managed_policy_arns
#     ]
#   }
# }
# resource "aws_iam_role_policy_attachment" "codebuild" {
#   role       = aws_iam_role.codebuild.name
#   policy_arn = aws_iam_policy.codebuild.arn
# }

# ################################################################################
# # CodeBuild
# ################################################################################
# # 코드 빌드 로그를 저장할 로그 그룹
# resource "aws_cloudwatch_log_group" "this" {
#   name              = "/aws/codebuild/${local.name}"
#   retention_in_days = 7
# }
# # 코드 빌드 프로젝트
# resource "aws_codebuild_project" "this" {
#   name         = "${local.name}"
#   service_role = aws_iam_role.codebuild.arn

#   artifacts {
#     type = "NO_ARTIFACTS"
#   }

#   environment {
#     compute_type    = "BUILD_GENERAL1_SMALL"
#     image           = "aws/codebuild/standard:5.0"
#     privileged_mode = "true"
#     type            = "LINUX_CONTAINER"
#   }

#   logs_config {
#     cloudwatch_logs {
#       status     = "ENABLED"
#       group_name = aws_cloudwatch_log_group.this.name
#     }
#   }

#   source {
#     type      = "GITHUB"
#     location  = "https://github.com/HaeDalWang/${local.name}.git"
#     buildspec = file("${path.module}/buildspec/${local.name}.yaml")
#   }
# }

# ################################################################################
# # CodePipeline
# ################################################################################
# resource "aws_codepipeline" "this" {
#   name          = "${local.name}-pipeline"
#   pipeline_type = "V2"
#   role_arn      = aws_iam_role.codepipeline.arn

#   artifact_store {
#     type     = "S3"
#     location = aws_s3_bucket.codepipeline.bucket
#   }

#   stage {
#     name = "Source"
#     action {
#       name             = "Source"
#       category         = "Source"
#       owner            = "AWS"
#       provider         = "CodeStarSourceConnection"
#       version          = "1"
#       namespace        = "SourceVariables"
#       output_artifacts = ["SourceArtifact"]

#       configuration = {
#         ConnectionArn        = aws_codestarconnections_connection.this.arn
#         FullRepositoryId     = "HaedalWang/${local.name}"
#         BranchName           = "main"
#       }
#     }
#   }

#   stage {
#     name = "Build"
#     action {
#       category = "Build"
#       configuration = {
#         ProjectName = each.key
#         EnvironmentVariables = jsonencode(concat(
#           [
#             {
#               name  = "FULL_REPOSITORY_NAME"
#               value = "#{SourceVariables.FullRepositoryName}"
#               type  = "PLAINTEXT"
#             },
#             {
#               name  = "AUTHOR_EMAIL"
#               value = "#{SourceVariables.AuthorEmail}"
#               type  = "PLAINTEXT"
#             },
#             {
#               name  = "AUTHOR_ID"
#               value = "#{SourceVariables.AuthorId}"
#               type  = "PLAINTEXT"
#             }
#           ]
#         ))
#       }

#       input_artifacts  = ["SourceArtifact"]
#       name             = "Build"
#       namespace        = "BuildVariables"
#       output_artifacts = ["BuildArtifact"]
#       owner            = "AWS"
#       provider         = "CodeBuild"
#       version          = "1"
#     }
#   }

#   trigger {
#     provider_type = "CodeStarSourceConnection"

#     git_configuration {
#       source_action_name = "Source"

#       push {
#         branches {
#           includes = ["main"]
#         }
#       }
#     }
#   }
# }