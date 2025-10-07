# gold.py
import pandas as pd
from aws_utils import s3_uri_exists

# All columns in lowercase (since we lowercase the dataframe columns)
FIXED_COLS = [
    "ano", "v1013", "v1012", "uf", "capital", "rm_ride", "uf_nome", "sigla", "regiao"
]
DESIRED_COLS = [
    "a002",      # idade
    "a003",      # sexo
    "a004",      # raça/cor
    "a005",      # escolaridade
    "c001",      # trabalhou/bico
    "c004",      # continuou remunerado
    "c007b",     # carteira assinada/servidor estatutário
    "c007c",     # tipo de trabalho/cargo/função
    "c007d",     # atividade da empresa
    "c0101",     # recebia/retirava em dinheiro
    "c01011",    # faixa do rendimento em dinheiro
    "c013",      # trabalho remoto
    "d0031",     # bolsa família
    "d0033",     # somatório bolsa família
    "d0061",     # seguro desemprego
    "d0063",     # somatório seguro desemprego
    "e001",      # solicitou empréstimo
    "a006",      # frequenta escola
    "a006a",     # escola pública/privada
    "b0011",     # febre
    "b0012",     # tosse
    "b0014",     # dificuldade para respirar
    "b0019",     # fadiga
    "b00111",    # perda de cheiro/sabor
    "b009a", 
    "b009b"             
]

def build_gold(s3, silver_uri: str, gold_uri: str, storage_options: dict, overwrite: bool = False):
    """
    Lê o parquet da camada Silver, seleciona/filtra colunas e grava a camada Gold (Parquet).
    Idempotente: se o Gold já existe e overwrite=False, apenas lê e retorna.
    """
    # Idempotência: não reprocessa se já existe
    if not overwrite and s3_uri_exists(s3, gold_uri):
        print(f"⏭️  Gold já existe: {gold_uri} (pulado)")
        return pd.read_parquet(gold_uri, storage_options=storage_options)

    # Ler Silver
    print(f"Lendo Silver: {silver_uri}")
    df_silver = pd.read_parquet(silver_uri, storage_options=storage_options)
    print(f"Silver lido: {len(df_silver)} linhas, {len(df_silver.columns)} colunas")

    # Normalizar e selecionar colunas
    dfe = df_silver.copy()
    dfe.columns = dfe.columns.map(str).str.lower()

    all_cols = list(dict.fromkeys([*FIXED_COLS, *DESIRED_COLS]))
    existing = [c for c in all_cols if c in dfe.columns]

    if "v1013" in dfe.columns:
        last3 = sorted(pd.unique(dfe["v1013"].dropna()))[-3:]
        final = dfe[dfe["v1013"].isin(last3)][existing].reset_index(drop=True)
    else:
        final = dfe[existing].reset_index(drop=True)

    missing = [c for c in all_cols if c not in dfe.columns]
    if missing:
        print(f"Atenção: colunas ausentes: {missing}")

    # Gravar Gold
    print(f"\nSalvando Gold: {gold_uri}")
    final.to_parquet(gold_uri, index=False, storage_options=storage_options)
    print(f"✅ Gold salvo ({len(final)} linhas)")
    return final

