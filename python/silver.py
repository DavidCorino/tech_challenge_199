# silver.py
import pandas as pd
from aws_utils import s3_uri_exists
from uf_fetch import fetch_uf_dataframe  # make sure uf_fetch.py exists

def build_silver(
    s3,
    bucket: str,
    bronze_prefix: str,
    silver_uri: str,
    storage_options: dict,
    overwrite: bool = False,
    ibge_uf_page_url: str | None = None,  # NEW
    uf_csv_url: str | None = None,        # fallback
):
    """
    Consolida CSVs da camada Bronze, enriquece com UF e grava Parquet na Silver.
    - Se silver_uri já existir e overwrite=False, apenas lê e retorna.
    - UF source: prioriza ibge_uf_page_url; se não vier, usa uf_csv_url.
    """
    if not overwrite and s3_uri_exists(s3, silver_uri):
        print(f"⏭️  Silver já existe: {silver_uri} (pulado)")
        return pd.read_parquet(silver_uri, storage_options=storage_options)

    resp = s3.list_objects_v2(Bucket=bucket, Prefix=f"{bronze_prefix}/")
    contents = resp.get("Contents", [])
    csv_keys = [o["Key"] for o in contents if o["Key"].lower().endswith(".csv")]
    if not csv_keys:
        raise RuntimeError("Nenhum CSV encontrado na camada Bronze.")

    dfs = []
    for key in csv_keys:
        uri = f"s3://{bucket}/{key}"
        print(f"Lendo {uri}")
        dfs.append(pd.read_csv(uri, storage_options=storage_options, sep=","))

    df_consolidado = pd.concat(dfs, ignore_index=True)
    print(f"Consolidado: {len(df_consolidado)} linhas | {len(df_consolidado.columns)} colunas")

    if ibge_uf_page_url:
        df_uf = fetch_uf_dataframe(ibge_uf_page_url)
    elif uf_csv_url:
        df_uf = pd.read_csv(uf_csv_url)
    else:
        raise ValueError("Forneça ibge_uf_page_url ou uf_csv_url.")

    df_consolidado["UF"] = pd.to_numeric(df_consolidado["UF"], errors="coerce").astype("Int64").astype(str)
    df_uf["Código"]       = pd.to_numeric(df_uf["Código"],       errors="coerce").astype("Int64").astype(str)

    df_consolidado = df_consolidado[df_consolidado["UF"] != "<NA>"].copy()
    df_uf          = df_uf[df_uf["Código"] != "<NA>"].copy()
    
    df_silver = pd.merge(
        df_consolidado,
        df_uf,
        how="left",
        left_on="UF",
        right_on="Código",
    )
    # Ajustes
    if "Código" in df_silver.columns:
        df_silver = df_silver.drop(columns=["Código"])
    df_silver = df_silver.rename(columns={"UF_x": "UF", "UF_y": "UF_Nome", "Região": "Regiao"})

    # Salvar Silver
    print(f"Salvando Silver em: {silver_uri}")
    df_silver.to_parquet(silver_uri, index=False, storage_options=storage_options)
    print(f"✅ Silver salvo ({len(df_silver)} linhas)")

    return df_silver

