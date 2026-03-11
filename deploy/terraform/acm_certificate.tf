resource "aws_acm_certificate" "mach_acm_certificate" {
      tags = {
        Name        = "mach-acm_certificate"
        Environment = "production"
        Project     = "mach"
      }
    }

    output "mach_acm_certificate_id" {
      value = aws_acm_certificate.mach_acm_certificate.id
    }
