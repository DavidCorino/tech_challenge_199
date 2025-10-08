terraform {
  backend "s3" {
    bucket  = "terraform-fiap0110"
    key     = "tech_challenge/terraform.tfstate"
    region  = "sa-east-1"
    encrypt = true

  }
}

