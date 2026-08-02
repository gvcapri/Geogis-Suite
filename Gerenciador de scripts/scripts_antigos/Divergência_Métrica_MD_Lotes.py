import re
import pandas as pd
from docx import Document

# =====================
# CONFIGURAÇÕES
# =====================
ARQUIVO_WORD = "MD_integral.docx"
ARQUIVO_EXCEL = "Planilha1.xlsx"

SAIDA_COMPARACAO = "comparacao_completa_word_x_excel_Distrito_São_Jorge2.xlsx"
SAIDA_CORRIGIDO = "excel_corrigido_pelo_word_Vila_Distrito_São_Jorge2.xlsx"

TOL = 0.02

ESTADO_PADRAO = ""
MUNICIPIO_PADRAO = ""
BAIRRO_PADRAO = ""

# =====================
# NORMALIZAÇÕES
# =====================
def normalizar_numero(v):
    if pd.isna(v):
        return None
    v = str(v).replace("m²", "").replace("m", "")
    v = v.replace(".", "").replace(",", ".")
    try:
        return float(v)
    except:
        return None


def formatar_area(v):
    if v is None:
        return None
    return f"{v:.2f}".replace(".", ",") + " m²"


def formatar_perimetro(v):
    if v is None:
        return None
    return f"{v:.2f}".replace(".", ",") + " m"


def normalizar_lote(l):
    return str(l).upper().replace(".", "").replace(" ", "")


def normalizar_quadra(q):
    nums = re.findall(r"\d+", str(q))
    return nums[0].zfill(2) if nums else None

# =====================
# WORD
# =====================
def extrair_word(caminho):
    doc = Document(caminho)
    texto = "\n".join(p.text for p in doc.paragraphs)

    padrao = re.compile(
        r"LOTE:\s*([A-Z0-9\.\-\s]+)\s*-\s*QUADRA:\s*([0-9\s]+).*?"
        r"ÁREA:\s*([\d\.,]+)\s*m².*?"
        r"PERÍMETRO:\s*([\d\.,]+)\s*m",
        re.DOTALL | re.IGNORECASE
    )

    dados = []
    for m in padrao.finditer(texto):
        dados.append({
            "Quadra": normalizar_quadra(m.group(2)),
            "Lote": normalizar_lote(m.group(1)),
            "Área_Word": normalizar_numero(m.group(3)),
            "Perímetro_Word": normalizar_numero(m.group(4))
        })

    return pd.DataFrame(dados)

# =====================
# EXCEL
# =====================
df_excel = pd.read_excel(ARQUIVO_EXCEL)

df_excel["Quadra"] = df_excel["Quadra"].apply(normalizar_quadra)
df_excel["Lote"] = df_excel["Lote"].apply(normalizar_lote)

df_excel["Área_Excel"] = df_excel["Área do lote"].apply(normalizar_numero)
df_excel["Perímetro_Excel"] = df_excel["Perímetro do lote"].apply(normalizar_numero)

df_word = extrair_word(ARQUIVO_WORD)

# =====================
# COMPARAÇÃO E CORREÇÃO
# =====================
comparacao = []
df_corrigido = df_excel.copy()

# --- Excel x Word ---
for i, e in df_excel.iterrows():
    w = df_word[
        (df_word["Quadra"] == e["Quadra"]) &
        (df_word["Lote"] == e["Lote"])
    ]

    if w.empty:
        comparacao.append({
            "Quadra": e["Quadra"],
            "Lote": e["Lote"],
            "Status": "Somente Excel"
        })
        continue

    w = w.iloc[0]

    dif_area = abs(w["Área_Word"] - e["Área_Excel"])
    dif_per = abs(w["Perímetro_Word"] - e["Perímetro_Excel"])

    if dif_area <= TOL and dif_per <= TOL:
        df_corrigido.at[i, "Área do lote"] = formatar_area(w["Área_Word"])
        df_corrigido.at[i, "Perímetro do lote"] = formatar_perimetro(w["Perímetro_Word"])
    else:
        df_corrigido.at[i, "Área do lote"] = formatar_area(e["Área_Excel"])
        df_corrigido.at[i, "Perímetro do lote"] = formatar_perimetro(e["Perímetro_Excel"])

    comparacao.append({
        "Quadra": e["Quadra"],
        "Lote": e["Lote"],
        "Área_Word": formatar_area(w["Área_Word"]),
        "Área_Excel": formatar_area(e["Área_Excel"]),
        "Diferença_Área": round(dif_area, 4),
        "Perímetro_Word": formatar_perimetro(w["Perímetro_Word"]),
        "Perímetro_Excel": formatar_perimetro(e["Perímetro_Excel"]),
        "Diferença_Perímetro": round(dif_per, 4),
        "Status": "Ambos"
    })

# --- Word sem Excel ---
for _, w in df_word.iterrows():
    existe = df_excel[
        (df_excel["Quadra"] == w["Quadra"]) &
        (df_excel["Lote"] == w["Lote"])
    ]

    if existe.empty:
        comparacao.append({
            "Quadra": w["Quadra"],
            "Lote": w["Lote"],
            "Status": "Somente Word"
        })

# =====================
# AJUSTE DE COLUNAS
# =====================
for col, val in {
    "Estado": ESTADO_PADRAO,
    "Município": MUNICIPIO_PADRAO,
    "Bairro": BAIRRO_PADRAO
}.items():
    if col not in df_corrigido.columns:
        df_corrigido[col] = val

ordem = [
    "Estado", "Município", "Bairro",
    "Quadra", "Lote", "Área do lote", "Perímetro do lote"
]

outras = [c for c in df_corrigido.columns if c not in ordem]
df_corrigido = df_corrigido[ordem + outras]

# =====================
# SAÍDA
# =====================
pd.DataFrame(comparacao).to_excel(SAIDA_COMPARACAO, index=False)
df_corrigido.to_excel(SAIDA_CORRIGIDO, index=False)

print("Arquivos gerados com sucesso.")
