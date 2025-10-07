# main.py
import os
from config import AppConfig
from aws_utils import make_s3, show_identity, list_prefix_count, s3_uri_exists
from s3_layout import ensure_prefixes
from bronze import load_bronze_from_ibge
from silver import build_silver
from gold import build_gold
from db_load import make_engine, test_connection, ensure_schema_no_drop, load_gold_to_db
from utils import display, start_timer, end_timer


def run():
    cfg = AppConfig()
    overwrite = os.getenv("OVERWRITE", "false").lower() == "true"

    # AWS
    show_identity(cfg.aws_region)
    s3 = make_s3(cfg.aws_region)
    ensure_prefixes(s3, cfg.s3_bucket, [cfg.bronze_prefix, cfg.silver_prefix, cfg.gold_prefix])

    # URIs S3
    silver_uri = f"s3://{cfg.s3_bucket}/{cfg.silver_prefix}/{cfg.silver_file}"
    gold_uri   = f"s3://{cfg.s3_bucket}/{cfg.gold_prefix}/{cfg.gold_file}"

    # DB
    engine = make_engine(cfg.pg_user, cfg.pg_pass, cfg.pg_host, cfg.pg_port, cfg.pg_db)
    test_connection(engine)

    t0 = start_timer()

    load_bronze_from_ibge(
        ibge_base_url=cfg.ibge_base_url,
        s3=s3,
        bucket=cfg.s3_bucket,
        bronze_prefix=cfg.bronze_prefix,
        overwrite=overwrite,
    )

    df_silver = build_silver(
        s3=s3,
        bucket=cfg.s3_bucket,
        bronze_prefix=cfg.bronze_prefix,
        ibge_uf_page_url=cfg.ibge_uf_page_url,
        silver_uri=silver_uri,
        storage_options=cfg.storage_options,
        overwrite=overwrite,
    )
    print("\nSilver head/tail")
    display(df_silver.head(5)); display(df_silver.tail(5))

    df_gold = build_gold(
        s3=s3,
        silver_uri=silver_uri,
        gold_uri=gold_uri,
        storage_options=cfg.storage_options,
        overwrite=overwrite,
    )
    print("\nGold head/tail")
    display(df_gold.head(5)); display(df_gold.tail(5))

    print("\nVerificação rápida no S3:")
    print("Bronze objects:", list_prefix_count(s3, cfg.s3_bucket, f"{cfg.bronze_prefix}/"))
    print("Silver exists?:", s3_uri_exists(s3, silver_uri))
    print("Gold exists?:",   s3_uri_exists(s3, gold_uri))

    ensure_schema_no_drop(engine, cfg.table_name, df_gold.head(0))
    load_gold_to_db(engine, cfg.table_name, gold_uri, cfg.storage_options)

    end_timer(t0)


if __name__ == "__main__":
    run()
