resource "aws_security_group" "mach_security_group" {
      tags = {
        Name        = "mach-security_group"
        Environment = "production"
        Project     = "mach"
      }
    }

    output "mach_security_group_id" {
      value = aws_security_group.mach_security_group.id
    }
