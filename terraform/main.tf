module "card_cdn" {
  source      = "./modules/card_cdn"
  bucket_name = var.bucket_name
}

output "cloudfront_domain" {
  description = "CloudFront distribution domain name"
  value       = module.card_cdn.cloudfront_domain_name
}

output "s3_bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = module.card_cdn.s3_bucket_arn
}
