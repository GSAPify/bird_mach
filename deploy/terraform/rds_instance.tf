resource "aws_rds_instance" "mach_rds_instance" {
      tags = {
        Name        = "mach-rds_instance"
        Environment = "production"
        Project     = "mach"
      }
    }

    output "mach_rds_instance_id" {
      value = aws_rds_instance.mach_rds_instance.id
    }
