module "card_cdn" {
  source      = "./modules/card_cdn"
  bucket_name = var.bucket_name
}

output "cloudfront_url" { 
  description = "CloudFront distribution url" 
  value       = module.card_cdn.cloudfront_url
}
