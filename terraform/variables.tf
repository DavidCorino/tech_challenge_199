variable "region" {
  description = "AWS region to deploy to"
  type        = string
  default     = "sa-east-1"
}

variable "allowed_cidr" {
  description = "CIDR(s) allowed to access PostgreSQL (TCP 5432)"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

# If you want to supply your own password, set this var and disable random_password below.
variable "postgres_password_override" {
  description = "Optional: provide your own postgres password"
  type        = string
  default     = ""
  sensitive   = true
}

variable "bucket_name" {
  type        = string
  description = "Globally unique S3 bucket name"
  default     = "terraform-fiap0110"
}

variable "bucket_name_bigdata" {
  type        = string
  description = "Globally unique S3 bucket name"
  default     = "fiap-bigdata0110"
}

variable "allowed_cidrs" {
  type        = list(string)
  description = "IP CIDRs allowed to access the bucket (e.g., [\"203.0.113.10/32\"])"
  default     = ["167.250.40.21/32"]
}

# Optional: allow access via specific VPC Endpoint(s) for S3 (Gateway/Interface)
# If you set this, requests coming through these endpoints bypass the IP allowlist check.
variable "allowed_vpce_ids" {
  type        = list(string)
  description = "Optional list of VPC Endpoint IDs allowed (e.g., [\"vpce-0123456789abcdef0\"])"
  default     = []
}

variable "account_id" {
  description = "AWS account ID whose IAM principals are exempt from the deny and allowed to manage the bucket policy"
  type        = string
  default     = "706676104942"
}
