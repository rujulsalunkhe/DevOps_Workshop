output "api_gateway_url" {
  description = "URL of the API Gateway"
  value       = "${aws_api_gateway_rest_api.flask_api.execution_arn}/prod"
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.flask_api.function_name
}

output "api_gateway_id" {
  description = "ID of the API Gateway"
  value       = aws_api_gateway_rest_api.flask_api.id
}
