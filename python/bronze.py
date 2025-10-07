import io
import re
import zipfile
import requests
import certifi
from urllib.parse import urljoin
from aws_utils import s3_key_exists

# Matches href="...zip" (directory listing)
ZIP_HREF_RE = re.compile(r'href="([^"]+\.zip)"', re.IGNORECASE)

def load_bronze_from_ibge(
    ibge_base_url: str,
    s3,
    bucket: str,
    bronze_prefix: str,
    overwrite: bool = False,
    only_matching: str | None = None,  # optional: regex to filter filenames
):
    """
    Lista a página do IBGE (autoindex), encontra .zip, baixa, extrai o primeiro CSV e envia ao S3.
    - ibge_base_url: ex.
      https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_PNAD_COVID19/Microdados/Dados/
    - overwrite=False: não envia se já existir no S3 com o mesmo nome.
    - only_matching: regex opcional para filtrar (ex.: r'2020|2021')
    """
    print(f"Listando arquivos em: {ibge_base_url}")
    resp = requests.get(ibge_base_url, timeout=60, verify=certifi.where())
    resp.raise_for_status()
    html = resp.text

    links = ZIP_HREF_RE.findall(html)
    if not links:
        print("⚠️ Nenhum .zip encontrado na listagem do IBGE.")
        return

    uploaded = 0
    skipped = 0

    for rel in links:
        zip_url = urljoin(ibge_base_url, rel)
        zip_name = rel.split("/")[-1]

        if only_matching and not re.search(only_matching, zip_name, flags=re.IGNORECASE):
            # pula se não casar com o filtro opcional
            continue

        print(f"\nProcessando: {zip_name}")
        r = requests.get(zip_url, timeout=300, stream=True, verify=certifi.where())
        r.raise_for_status()
        content = io.BytesIO(r.content)

        with zipfile.ZipFile(content) as zf:
            csvs = [n for n in zf.namelist() if n.lower().endswith(".csv")]
            if not csvs:
                print("⚠️ Zip sem CSV, pulando.")
                continue

            # pega só o nome-base do CSV (remove pastas internas do zip)
            csv_name = csvs[0]
            csv_basename = csv_name.split("/")[-1]
            key = f"{bronze_prefix}/{csv_basename}"

            # idempotência
            if not overwrite and s3_key_exists(s3, bucket, key):
                print(f"⏭️  Já existe: s3://{bucket}/{key} (pulado)")
                skipped += 1
                continue

            body = zf.read(csv_name)
            print(f"Enviando para s3://{bucket}/{key}")
            s3.put_object(Bucket=bucket, Key=key, Body=body)
            print("✅ Enviado")
            uploaded += 1

    print(f"\nBronze (IBGE) concluído. Uploads: {uploaded} | Pulados: {skipped}")
