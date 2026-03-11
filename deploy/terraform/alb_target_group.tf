resource "aws_alb_target_group" "mach_alb_target_group" {
      tags = {
        Name        = "mach-alb_target_group"
        Environment = "production"
        Project     = "mach"
      }
    }

    output "mach_alb_target_group_id" {
      value = aws_alb_target_group.mach_alb_target_group.id
    }
