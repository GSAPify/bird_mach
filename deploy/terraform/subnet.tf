resource "aws_subnet" "mach_subnet" {
      tags = {
        Name        = "mach-subnet"
        Environment = "production"
        Project     = "mach"
      }
    }

    output "mach_subnet_id" {
      value = aws_subnet.mach_subnet.id
    }
