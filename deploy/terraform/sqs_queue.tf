resource "aws_sqs_queue" "mach_sqs_queue" {
      tags = {
        Name        = "mach-sqs_queue"
        Environment = "production"
        Project     = "mach"
      }
    }

    output "mach_sqs_queue_id" {
      value = aws_sqs_queue.mach_sqs_queue.id
    }
