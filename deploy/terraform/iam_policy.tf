resource "aws_iam_policy" "mach_iam_policy" {
      tags = {
        Name        = "mach-iam_policy"
        Environment = "production"
        Project     = "mach"
      }
    }

    output "mach_iam_policy_id" {
      value = aws_iam_policy.mach_iam_policy.id
    }
