# s3_layout.py
from botocore.exceptions import ClientError

def ensure_prefixes(s3, bucket: str, prefixes: list[str]):
    print(f"\nValidando as subpastas no bucket '{bucket}'")
    for name in prefixes:
        key = name if name.endswith("/") else name + "/"
        try:
            s3.head_object(Bucket=bucket, Key=key)
            print(f"➡️  Pasta '{key}' já existe")
        except ClientError as e:
            code = e.response.get("Error", {}).get("Code", "")
            if code in ("404", "NoSuchKey", "NotFound"):
                try:
                    s3.put_object(Bucket=bucket, Key=key, Body=b"")
                    print(f"✅ Pasta '{key}' criada com sucesso")
                except Exception as ce:
                    print(f"❌ Falha ao criar a pasta '{key}': {ce}")
            elif code in ("403", "AccessDenied"):
                print(f"❌ Sem permissão para verificar/criar '{key}'. Revise bucket policy/SCP.")
            else:
                print(f"❌ Erro ao verificar '{key}': {e}")

