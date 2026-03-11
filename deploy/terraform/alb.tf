resource "aws_alb" "mach_alb" {
      tags = {
        Name        = "mach-alb"
        Environment = "production"
        Project     = "mach"
      }
    }

    output "mach_alb_id" {
      value = aws_alb.mach_alb.id
    }
