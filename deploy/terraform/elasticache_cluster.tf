resource "aws_elasticache_cluster" "mach_elasticache_cluster" {
      tags = {
        Name        = "mach-elasticache_cluster"
        Environment = "production"
        Project     = "mach"
      }
    }

    output "mach_elasticache_cluster_id" {
      value = aws_elasticache_cluster.mach_elasticache_cluster.id
    }
