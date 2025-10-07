import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class AppConfig:
    # S3
    s3_bucket: str = os.getenv("S3_BUCKET", "fiap-bigdata0110")
    aws_region: str = os.getenv("AWS_REGION", "sa-east-1")

    # PostgreSQL
    pg_user: str = os.getenv("POSTGRES_USER_PNAD", "")
    pg_pass: str = os.getenv("POSTGRES_PASSWORD_PNAD", "")
    pg_host: str = os.getenv("POSTGRES_HOST_PNAD", "")
    pg_port: str = os.getenv("POSTGRES_PORT_PNAD", "5432")
    pg_db:   str = os.getenv("POSTGRES_DB_PNAD", "postgres")

    # Table name
    table_name: str = os.getenv("POSTGRES_TABLE_PNAD", "questionario_pnad_covid")

    # IBGE source (directory listing for PNAD microdados)
    ibge_base_url: str = (
        "https://ftp.ibge.gov.br/Trabalho_e_Rendimento/"
        "Pesquisa_Nacional_por_Amostra_de_Domicilios_PNAD_COVID19/"
        "Microdados/Dados/"
    )

    # IBGE page to scrape UF codes (instead of static CSV)
    ibge_uf_page_url: str = "https://www.ibge.gov.br/explica/codigos-dos-municipios.php"

    # Layer prefixes
    bronze_prefix: str = "bronze"
    silver_prefix: str = "silver"
    gold_prefix:   str = "gold"

    # Filenames
    silver_file: str = "pnad_consolidado_enriquecido.parquet"
    gold_file:   str = "pnad_final_tratado.parquet"

    @property
    def storage_options(self):
        return {
            "key": os.getenv("AWS_ACCESS_KEY_ID"),
            "secret": os.getenv("AWS_SECRET_ACCESS_KEY"),
            "token": os.getenv("AWS_SESSION_TOKEN"),
        }

