import re
import pandas as pd
from docx import Document

# =========================
# LEITURA MD (DOCX)
# =========================

def ler_docx(caminho):
    doc = Document(caminho)
    return "\n".join(p.text for p in doc.paragraphs).upper()


# =========================
# NORMALIZAÇÃO
# =========================

def normalizar(valor):
    return str(valor).replace(" ", "").upper()


def str_para_float(v):
    if v is None or pd.isna(v):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    return float(str(v).replace(".", "").replace(",", "."))


def chave(quadra, lote):
    return f"QD{quadra}_LT{lote}"


# =========================
# EXTRAÇÃO MD (POR LOTE)
# =========================

def extrair_md(texto):
    dados = []

    blocos = re.split(
        r"(PROPRIEDADE:\s*LOTE:\s*[0-9A-Z\-]+\s*-\s*QUADRA:\s*[0-9A-Z]+)",
        texto
    )

    for i in range(1, len(blocos), 2):
        cabecalho = blocos[i]
        corpo = blocos[i + 1] if i + 1 < len(blocos) else ""

        m = re.search(
            r"LOTE:\s*([0-9A-Z\-]+)\s*-\s*QUADRA:\s*([0-9A-Z]+)",
            cabecalho
        )
        if not m:
            continue

        lote = normalizar(m.group(1))
        quadra = normalizar(m.group(2))

        # Regex flexível: mesma linha ou linhas separadas
        m_area = re.search(r"ÁREA\s*:\s*([\d.,]+)", corpo)
        m_per = re.search(r"PERÍMETRO\s*:\s*([\d.,]+)", corpo)

        dados.append({
            "quadra": quadra,
            "lote": lote,
            "area_md": str_para_float(m_area.group(1)) if m_area else None,
            "perimetro_md": str_para_float(m_per.group(1)) if m_per else None,
            "chave": chave(quadra, lote)
        })

    return pd.DataFrame(dados)


# =========================
# LEITURA PLANILHA MÉTRICA
# =========================

def ler_metrica(caminho):
    df = pd.read_excel(caminho)

    # normaliza nomes das colunas
    colunas = {c: c.upper().strip() for c in df.columns}
    df = df.rename(columns=colunas)

    # mapeamento flexível
    mapa = {
        "QUADRA": "quadra",
        "LOTE": "lote",
        "ÁREA DO LOTE": "area_metrica",
        "AREA DO LOTE": "area_metrica",
        "ÁREA": "area_metrica",
        "AREA": "area_metrica",
        "PERÍMETRO DO LOTE": "perimetro_metrica",
        "PERIMETRO DO LOTE": "perimetro_metrica",
        "PERÍMETRO": "perimetro_metrica",
        "PERIMETRO": "perimetro_metrica",
    }

    df = df.rename(columns={k: v for k, v in mapa.items() if k in df.columns})

    # validação
    colunas_necessarias = ["quadra", "lote", "area_metrica", "perimetro_metrica"]
    for c in colunas_necessarias:
        if c not in df.columns:
            raise ValueError(f"❌ Coluna obrigatória não encontrada na planilha: {c}")

    df["quadra"] = df["quadra"].apply(normalizar)
    df["lote"] = df["lote"].apply(normalizar)

    df["area_metrica"] = df["area_metrica"].apply(str_para_float)
    df["perimetro_metrica"] = df["perimetro_metrica"].apply(str_para_float)

    df["chave"] = df.apply(lambda r: chave(r["quadra"], r["lote"]), axis=1)

    return df
    df = pd.read_excel(caminho)

    df = df.rename(columns={
        "Quadra": "quadra",
        "Lote": "lote",
        "Área do lote": "area_metrica",
        "Perímetro do lote": "perimetro_metrica"
    })

    df["quadra"] = df["quadra"].apply(normalizar)
    df["lote"] = df["lote"].apply(normalizar)

    df["area_metrica"] = df["area_metrica"].apply(str_para_float)
    df["perimetro_metrica"] = df["perimetro_metrica"].apply(str_para_float)

    df["chave"] = df.apply(lambda r: chave(r["quadra"], r["lote"]), axis=1)

    return df


# =========================
# EXECUÇÃO
# =========================

ARQUIVO_MD = "MD_Guariba 1.docx"
ARQUIVO_METRICA = "Pasta1 1.xlsx"

texto_md = ler_docx(ARQUIVO_MD)

df_md = extrair_md(texto_md)
df_metrica = ler_metrica(ARQUIVO_METRICA)

df = pd.merge(df_md, df_metrica, on=["chave", "quadra", "lote"], how="outer")

df["dif_area"] = df["area_md"] - df["area_metrica"]
df["dif_perimetro"] = df["perimetro_md"] - df["perimetro_metrica"]

df = df[[
    "quadra",
    "lote",
    "area_md",
    "area_metrica",
    "dif_area",
    "perimetro_md",
    "perimetro_metrica",
    "dif_perimetro"
]]

df.to_excel("comparacao_md_metrica.xlsx", index=False)

print("✅ Arquivo gerado: comparacao_md_metrica.xlsx")
