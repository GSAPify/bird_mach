resource "aws_ecs_cluster" "mach_ecs_cluster" {
      tags = {
        Name        = "mach-ecs_cluster"
        Environment = "production"
        Project     = "mach"
      }
    }

    output "mach_ecs_cluster_id" {
      value = aws_ecs_cluster.mach_ecs_cluster.id
    }
