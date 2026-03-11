resource "aws_sns_topic" "mach_sns_topic" {
      tags = {
        Name        = "mach-sns_topic"
        Environment = "production"
        Project     = "mach"
      }
    }

    output "mach_sns_topic_id" {
      value = aws_sns_topic.mach_sns_topic.id
    }
