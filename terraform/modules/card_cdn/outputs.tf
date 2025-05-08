output "cloudfront_url" { 
  description = "CloudFront distribution domain name (URL)" 
  value       = "https://${aws_cloudfront_distribution.s3_distribution.domain_name}"
}
