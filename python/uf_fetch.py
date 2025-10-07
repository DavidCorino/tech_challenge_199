import requests
import pandas as pd
from lxml import html

_UF_MAP = {
    '11': {'Sigla': 'RO', 'Região': 'Norte'},
    '12': {'Sigla': 'AC', 'Região': 'Norte'},
    '13': {'Sigla': 'AM', 'Região': 'Norte'},
    '14': {'Sigla': 'RR', 'Região': 'Norte'},
    '15': {'Sigla': 'PA', 'Região': 'Norte'},
    '16': {'Sigla': 'AP', 'Região': 'Norte'},
    '17': {'Sigla': 'TO', 'Região': 'Norte'},
    '21': {'Sigla': 'MA', 'Região': 'Nordeste'},
    '22': {'Sigla': 'PI', 'Região': 'Nordeste'},
    '23': {'Sigla': 'CE', 'Região': 'Nordeste'},
    '24': {'Sigla': 'RN', 'Região': 'Nordeste'},
    '25': {'Sigla': 'PB', 'Região': 'Nordeste'},
    '26': {'Sigla': 'PE', 'Região': 'Nordeste'},
    '27': {'Sigla': 'AL', 'Região': 'Nordeste'},
    '28': {'Sigla': 'SE', 'Região': 'Nordeste'},
    '29': {'Sigla': 'BA', 'Região': 'Nordeste'},
    '31': {'Sigla': 'MG', 'Região': 'Sudeste'},
    '32': {'Sigla': 'ES', 'Região': 'Sudeste'},
    '33': {'Sigla': 'RJ', 'Região': 'Sudeste'},
    '35': {'Sigla': 'SP', 'Região': 'Sudeste'},
    '41': {'Sigla': 'PR', 'Região': 'Sul'},
    '42': {'Sigla': 'SC', 'Região': 'Sul'},
    '43': {'Sigla': 'RS', 'Região': 'Sul'},
    '50': {'Sigla': 'MS', 'Região': 'Centro-Oeste'},
    '51': {'Sigla': 'MT', 'Região': 'Centro-Oeste'},
    '52': {'Sigla': 'GO', 'Região': 'Centro-Oeste'},
    '53': {'Sigla': 'DF', 'Região': 'Centro-Oeste'},
}

def fetch_uf_dataframe(ibge_uf_page_url: str) -> pd.DataFrame:
    """Scrape the IBGE page for UF codes and build a DataFrame with Código, UF, Sigla, Região."""
    resp = requests.get(ibge_uf_page_url, timeout=60)
    resp.encoding = "utf-8"
    tree = html.fromstring(resp.content)

    ufs = tree.xpath('//table[1]/tbody/tr/td[1]/a/text()')
    codigos = tree.xpath('//table[1]/tbody/tr/td[2]/a/text()')

    df = pd.DataFrame({"Código": codigos, "UF": ufs})
    df["Sigla"] = df["Código"].map(lambda x: _UF_MAP.get(x, {}).get("Sigla"))
    df["Região"] = df["Código"].map(lambda x: _UF_MAP.get(x, {}).get("Região"))
    return df

