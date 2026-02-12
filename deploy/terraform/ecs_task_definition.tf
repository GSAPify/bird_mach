resource "aws_ecs_task_definition" "mach_ecs_task_definition" {
      tags = {
        Name        = "mach-ecs_task_definition"
        Environment = "production"
        Project     = "mach"
      }
    }

    output "mach_ecs_task_definition_id" {
      value = aws_ecs_task_definition.mach_ecs_task_definition.id
    }
