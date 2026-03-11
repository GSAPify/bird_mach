resource "aws_ecr_repository" "mach_ecr_repository" {
      tags = {
        Name        = "mach-ecr_repository"
        Environment = "production"
        Project     = "mach"
      }
    }

    output "mach_ecr_repository_id" {
      value = aws_ecr_repository.mach_ecr_repository.id
    }
