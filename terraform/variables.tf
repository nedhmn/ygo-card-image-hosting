# Input variables with .auto.tfvars
# ref: https://developer.hashicorp.com/terraform/language/values/variables

variable "aws_region" {
  type     = string
  nullable = false
}

variable "aws_access_key_id" {
  type     = string
  nullable = false
}

variable "aws_secret_access_key" {
  type     = string
  nullable = false
}

variable "bucket_name" {
  type     = string
  nullable = false
}
