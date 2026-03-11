resource "aws_vpc" "mach_vpc" {
      tags = {
        Name        = "mach-vpc"
        Environment = "production"
        Project     = "mach"
      }
    }

    output "mach_vpc_id" {
      value = aws_vpc.mach_vpc.id
    }
