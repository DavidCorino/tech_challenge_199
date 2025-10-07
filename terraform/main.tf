resource "aws_db_subnet_group" "this" {
  name       = "pg-sandbox-subnets"
  subnet_ids = data.aws_subnets.default_vpc_subnets.ids
  tags = {
    Name = "pg-sandbox-subnets"
  }
}

resource "aws_security_group" "pg" {
  name        = "pg-sandbox-sg"
  description = "Allow public PostgreSQL access (sandbox)"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "PostgreSQL"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "pg-sandbox-sg"
  }
}

resource "random_password" "postgres" {
  length           = 20
  special          = true
  override_special = "!#%^*-_=+."
  # (optional but recommended to guarantee character classes)
  min_upper   = 1
  min_lower   = 1
  min_numeric = 1
  min_special = 1
}


locals {
  postgres_password = length(var.postgres_password_override) > 0 ? var.postgres_password_override : random_password.postgres.result
}

resource "aws_db_instance" "postgres_sandbox" {
  identifier = "postgres-tc" # Identificador da instância
  engine     = "postgres"    # Tipo de banco: PostgreSQL
  # engine_version       = "15"                   # Optional; omit to get latest 15.x
  instance_class    = "db.t3.micro" # Tipo de instância
  allocated_storage = 20            # 20 GB
  storage_type      = "gp3"         # SSD General Purpose
  db_name           = "pnad_covid"  # Nome do banco inicial
  username          = "postgres"    # Usuário
  password          = local.postgres_password
  port              = 5432

  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = [aws_security_group.pg.id]
  publicly_accessible    = true # Acesso público: Sim

  backup_retention_period  = 0 # Sandbox (no backups)
  delete_automated_backups = true
  deletion_protection      = false
  skip_final_snapshot      = true
  apply_immediately        = true

  # Minor version upgrades automatically (recommended for sandbox)
  auto_minor_version_upgrade = true

  tags = {
    Name        = "postgres-tc"
    Environment = "sandbox"
  }
}
