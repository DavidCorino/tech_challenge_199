import io
import os
import sys
from typing import Optional, Dict, Any

import pandas as pd
from sqlalchemy import create_engine, text
from psycopg2 import sql as _sql

# -------------------------------
# Conexão / Engine
# -------------------------------
def make_engine(user: str, pwd: str, host: str, port: str, db: str):
    url = f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}"
    return create_engine(url)

def test_connection(engine) -> None:
    try:
        with engine.connect() as conn:
            v = conn.execute(text("SELECT version();")).fetchone()
            print("✅ Conectado:", v[0])
    except Exception as e:
        print("Erro ao testar conexão:", e)
        try:
            engine.dispose()
        except Exception:
            pass
        sys.exit(1)

# -------------------------------
# Garantia de esquema (sem DROP)
# -------------------------------
_PANDAS2PG = {
    "int64": "BIGINT",
    "int32": "INTEGER",
    "float64": "DOUBLE PRECISION",
    "float32": "REAL",
    "bool": "BOOLEAN",
    "datetime64[ns]": "TIMESTAMPTZ",
    "object": "TEXT",
    "string": "TEXT",
}

def _pg_type(dtype) -> str:
    return _PANDAS2PG.get(str(dtype), "TEXT")

def ensure_schema_no_drop(engine, table_name: str, df_sample: pd.DataFrame) -> None:
    """
    Garante a existência e colunas da tabela sem executar DROP (não quebra views).
    - Cria a tabela se não existir.
    - Adiciona colunas ausentes, com tipos derivados do DataFrame.
    - Adiciona colunas de metadados (data_hora_carga, usuario_carga).
    """
    parts = [f'"{c}" {_pg_type(dt)}' for c, dt in zip(df_sample.columns, df_sample.dtypes)]
    if not parts:
        parts = ['"_dummy" TEXT']  # evita DDL inválida se DF vier vazio
    cols_def = ", ".join(parts)

    try:
        with engine.begin() as conn:  # commit/rollback automático
            # 1) cria a tabela se não existir
            conn.execute(text(f'CREATE TABLE IF NOT EXISTS "{table_name}" ({cols_def});'))

            # 2) adiciona colunas que porventura faltem
            for c, dt in zip(df_sample.columns, df_sample.dtypes):
                conn.execute(text(
                    f'ALTER TABLE "{table_name}" ADD COLUMN IF NOT EXISTS "{c}" {_pg_type(dt)};'
                ))

            # 3) metadados padrão
            conn.execute(text(
                f'ALTER TABLE "{table_name}" '
                f'ADD COLUMN IF NOT EXISTS data_hora_carga TIMESTAMPTZ DEFAULT NOW();'
            ))
            conn.execute(text(
                f'ALTER TABLE "{table_name}" '
                f'ADD COLUMN IF NOT EXISTS usuario_carga VARCHAR(255) DEFAULT CURRENT_USER;'
            ))

        print(f"✅ Esquema garantido (sem DROP) para '{table_name}'.")
    except Exception as e:
        print("Erro:", e)
        try:
            engine.dispose()
        except Exception:
            pass
        sys.exit(1)

# -------------------------------
# Carga (TRUNCATE + COPY)
# -------------------------------
def load_gold_to_db(
    engine,
    table_name: str,
    gold_uri: str,
    storage_options: Optional[Dict[str, Any]] = None,
    export_csv: bool = True,
) -> None:
    """
    Lê o parquet da camada Gold (em S3 ou local), faz TRUNCATE e carrega via COPY.
    Mantém a estrutura da tabela (não executa DROP/CREATE).
    """
    if storage_options is None:
        storage_options = {}

    try:
        print(f"Lendo Gold de: {gold_uri}")
        df_gold = pd.read_parquet(gold_uri, storage_options=storage_options)
        print(f"Gold lido: {len(df_gold)} linhas")

        with engine.connect() as connection:
            raw = connection.connection
            cur = raw.cursor()
            try:
                print(f'TRUNCATE "{table_name}"')
                cur.execute(_sql.SQL('TRUNCATE TABLE {}').format(_sql.Identifier(table_name)))

                # Buffer CSV em memória para COPY
                buf = io.StringIO()
                df_gold.to_csv(buf, index=False, header=False, sep="\t")
                buf.seek(0)
                cols = list(df_gold.columns)

                print(f"COPY {len(df_gold)} linhas → {table_name}")
                cur.copy_from(buf, table_name, sep="\t", null="", columns=cols)

                raw.commit()
                cur.close()
                print("✅ Carga concluída")

                if export_csv:
                    # Export opcional para CSV local (pós-carga)
                    print("Exportando tabela para CSV local…")
                    out_csv = f"{table_name}_exportado.csv"
                    df_all = pd.read_sql_query(f'SELECT * FROM "{table_name}";', connection)
                    df_all.to_csv(out_csv, index=False, sep=";", encoding="utf-8-sig")
                    print("✅ Exportado:", os.path.join(os.getcwd(), out_csv))

            except Exception as e:
                print("❌ Erro durante a carga:", e)
                try:
                    raw.rollback()
                    print("Rollback efetuado.")
                except Exception:
                    pass
                # Propaga para o handler externo (dispose + exit)
                raise

    except Exception as e:
        print("Erro:", e)
        try:
            engine.dispose()
        except Exception:
            pass
        sys.exit(1)

create_schema = ensure_schema_no_drop
