resource "aws_route_table" "mach_route_table" {
      tags = {
        Name        = "mach-route_table"
        Environment = "production"
        Project     = "mach"
      }
    }

    output "mach_route_table_id" {
      value = aws_route_table.mach_route_table.id
    }
