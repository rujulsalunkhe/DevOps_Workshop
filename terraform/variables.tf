variable "lambda_zip_path" {
  description = "Path to the Lambda deployment package"
  type        = string
  default     = "../lambda-deployment.zip"
}

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}
