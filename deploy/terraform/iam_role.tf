resource "aws_iam_role" "mach_iam_role" {
      tags = {
        Name        = "mach-iam_role"
        Environment = "production"
        Project     = "mach"
      }
    }

    output "mach_iam_role_id" {
      value = aws_iam_role.mach_iam_role.id
    }
