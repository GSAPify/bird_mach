resource "aws_cloudfront_distribution" "mach_cloudfront_distribution" {
      tags = {
        Name        = "mach-cloudfront_distribution"
        Environment = "production"
        Project     = "mach"
      }
    }

    output "mach_cloudfront_distribution_id" {
      value = aws_cloudfront_distribution.mach_cloudfront_distribution.id
    }
