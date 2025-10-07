import boto3
from botocore.exceptions import BotoCoreError, ClientError

def make_s3(region_name: str):
    return boto3.client("s3", region_name=region_name)

def show_identity(region_name: str):
    try:
        sts = boto3.client("sts", region_name=region_name)
        who = sts.get_caller_identity()
        print("✅ Conectado à conta\nUserId:", who["UserId"], "\nAccount:", who["Account"], "\nArn:", who["Arn"])
    except (BotoCoreError, ClientError) as e:
        print("❌ Erro ao conectar à AWS. Verifique credenciais.", e)

def s3_key_exists(s3, bucket: str, key: str) -> bool:
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code", "")
        if code in ("404", "NoSuchKey", "NotFound"):
            return False
        raise  # rethrow real errors (e.g., AccessDenied)

def s3_uri_exists(s3, s3_uri: str) -> bool:
    # expects 's3://bucket/key'
    if not s3_uri.startswith("s3://"):
        raise ValueError(f"Invalid S3 URI: {s3_uri}")
    bucket_key = s3_uri[len("s3://"):]
    bucket, key = bucket_key.split("/", 1)
    return s3_key_exists(s3, bucket, key)

def list_prefix_count(s3, bucket: str, prefix: str) -> int:
    total, token = 0, None
    while True:
        kwargs = dict(Bucket=bucket, Prefix=prefix)
        if token:
            kwargs["ContinuationToken"] = token
        resp = s3.list_objects_v2(**kwargs)
        total += len(resp.get("Contents", []))
        if resp.get("IsTruncated"):
            token = resp.get("NextContinuationToken")
        else:
            break
    return total

