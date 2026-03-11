resource "aws_s3_bucket" "mach_s3_bucket" {
      tags = {
        Name        = "mach-s3_bucket"
        Environment = "production"
        Project     = "mach"
      }
    }

    output "mach_s3_bucket_id" {
      value = aws_s3_bucket.mach_s3_bucket.id
    }
