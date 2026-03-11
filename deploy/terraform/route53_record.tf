resource "aws_route53_record" "mach_route53_record" {
      tags = {
        Name        = "mach-route53_record"
        Environment = "production"
        Project     = "mach"
      }
    }

    output "mach_route53_record_id" {
      value = aws_route53_record.mach_route53_record.id
    }
