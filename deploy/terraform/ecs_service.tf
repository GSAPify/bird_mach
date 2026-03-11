resource "aws_ecs_service" "mach_ecs_service" {
      tags = {
        Name        = "mach-ecs_service"
        Environment = "production"
        Project     = "mach"
      }
    }

    output "mach_ecs_service_id" {
      value = aws_ecs_service.mach_ecs_service.id
    }
