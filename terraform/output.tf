# ------- Outputs -------
output "rds_endpoint" {
  description = "RDS writer endpoint (host:port)"
  value       = aws_db_instance.postgres_sandbox.address
}

output "rds_port" {
  value = aws_db_instance.postgres_sandbox.port
}

output "postgres_username" {
  value = aws_db_instance.postgres_sandbox.username
}

output "postgres_password" {
  value     = local.postgres_password
  sensitive = true
}

output "bucket_name" {
  value = aws_s3_bucket.this.bucket
}

output "bucket_arn" {
  value = aws_s3_bucket.this.arn
}

output "bucket_name_bigdata" {
  value = aws_s3_bucket.bigdata.bucket
}

output "bucket_arn_bigdata" {
  value = aws_s3_bucket.bigdata.arn
}
