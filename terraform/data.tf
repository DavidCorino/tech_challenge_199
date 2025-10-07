data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default_vpc_subnets" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

locals {
  acct_principal_pattern = "arn:aws:iam::${var.account_id}:*"
}

data "aws_iam_policy_document" "bucket_policy" {
  statement {
    sid     = "DenyRequestsNotFromAllowedIPsOrVPCE"
    effect  = "Deny"
    actions = ["s3:*"]

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
    resources = [
      aws_s3_bucket.this.arn,
      "${aws_s3_bucket.this.arn}/*"
    ]

    condition {
      test     = "NotIpAddress"
      variable = "aws:SourceIp"
      values   = length(var.allowed_cidrs) > 0 ? var.allowed_cidrs : ["0.0.0.0/32"]
    }

    condition {
      test     = "ArnNotLike"
      variable = "aws:PrincipalArn"
      values   = [local.acct_principal_pattern]
    }
  }

  statement {
    sid    = "AllowAccountPrincipalsToManageBucketPolicy"
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
    actions = [
      "s3:GetBucketPolicy",
      "s3:PutBucketPolicy",
      "s3:GetBucketPolicyStatus",
      "s3:GetBucketPublicAccessBlock",
      "s3:PutBucketPublicAccessBlock"
    ]

    resources = [
      aws_s3_bucket.this.arn
    ]

    condition {
      test     = "ArnLike"
      variable = "aws:PrincipalArn"
      values   = [local.acct_principal_pattern]
    }
  }
}

data "aws_iam_policy_document" "bucket_policy_bigdata" {
  statement {
    sid     = "DenyRequestsNotFromAllowedIPsOrVPCE"
    effect  = "Deny"
    actions = ["s3:*"]

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
    resources = [
      aws_s3_bucket.bigdata.arn,
      "${aws_s3_bucket.bigdata.arn}/*"
    ]

    condition {
      test     = "NotIpAddress"
      variable = "aws:SourceIp"
      values   = length(var.allowed_cidrs) > 0 ? var.allowed_cidrs : ["0.0.0.0/32"]
    }

    condition {
      test     = "ArnNotLike"
      variable = "aws:PrincipalArn"
      values   = [local.acct_principal_pattern]
    }
  }

  statement {
    sid    = "AllowAccountPrincipalsToManageBucketPolicy"
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
    actions = [
      "s3:GetBucketPolicy",
      "s3:PutBucketPolicy",
      "s3:GetBucketPolicyStatus",
      "s3:GetBucketPublicAccessBlock",
      "s3:PutBucketPublicAccessBlock"
    ]

    resources = [
      aws_s3_bucket.bigdata.arn
    ]

    condition {
      test     = "ArnLike"
      variable = "aws:PrincipalArn"
      values   = [local.acct_principal_pattern]
    }
  }
}
