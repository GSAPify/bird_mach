resource "aws_cloudwatch_log_group" "mach_cloudwatch_log_group" {
      tags = {
        Name        = "mach-cloudwatch_log_group"
        Environment = "production"
        Project     = "mach"
      }
    }

    output "mach_cloudwatch_log_group_id" {
      value = aws_cloudwatch_log_group.mach_cloudwatch_log_group.id
    }
