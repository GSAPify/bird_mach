resource "aws_waf_web_acl" "mach_waf_web_acl" {
      tags = {
        Name        = "mach-waf_web_acl"
        Environment = "production"
        Project     = "mach"
      }
    }

    output "mach_waf_web_acl_id" {
      value = aws_waf_web_acl.mach_waf_web_acl.id
    }
