import pandas as pd

# Carrega os arquivos
df1 = pd.read_excel(r"att.xlsx")  #<- Aqui vai ECOLETA
df2 = pd.read_excel(r"serradourada_shp.xlsx")     #<- Aqui vai SHP
nome = "serra dourada att - SHP_ECOLETA - Comparativo.xlsx"

# Função para padronizar quadra e lote
def padronizar(df):
    df["quadra"] = df["quadra"].astype(str).str.strip().str.upper().str.lstrip("0")
    df["lote"] = df["lote"].astype(str).str.strip().str.upper().str.lstrip("0")
    return df

# Padroniza os dados
df1_limpo = padronizar(df1.rename(columns={"Quadra": "quadra", "Lote": "lote", "Status Processo": "Status"}))[["quadra", "lote", "Status"]]
df2_temp = df2.rename(columns={"Quadra": "quadra", "Lote": "lote"})
df2_temp["Status"] = "--"
df2_limpo = padronizar(df2_temp)[["quadra", "lote", "Status"]]

# Verifica duplicatas
duplicatas_ecoleta = df1_limpo[df1_limpo.duplicated(subset=["quadra", "lote"], keep=False)]
duplicatas_shp = df2_limpo[df2_limpo.duplicated(subset=["quadra", "lote"], keep=False)]

# Cria conjuntos únicos
set_ecoleta = set(zip(df1_limpo["quadra"], df1_limpo["lote"]))
set_shp = set(zip(df2_limpo["quadra"], df2_limpo["lote"]))

# Agrupa para pegar um único status 
status_dict = df1_limpo.drop_duplicates(subset=["quadra", "lote"]).set_index(["quadra", "lote"])["Status"].to_dict()

# Identifica os casos
resultado = []

for quadra_lote in sorted(set_ecoleta - set_shp):
    status = status_dict.get((quadra_lote[0], quadra_lote[1]), "")
    resultado.append({"Quadra": quadra_lote[0], "Lote": quadra_lote[1], "Status": status, "Origem": "ECOLETA"})

for quadra_lote in sorted(set_shp - set_ecoleta):
    resultado.append({"Quadra": quadra_lote[0], "Lote": quadra_lote[1], "Status": "--", "Origem": "SHP"})

for quadra_lote in sorted(set_ecoleta & set_shp):
    status = status_dict.get((quadra_lote[0], quadra_lote[1]), "")
    resultado.append({"Quadra": quadra_lote[0], "Lote": quadra_lote[1], "Status": status, "Origem": "Ambos"})

# Cria DataFrame do resultado
df_resultado = pd.DataFrame(resultado)

# Salva em novo arquivo Excel com múltiplas abas
with pd.ExcelWriter(nome) as writer:
    df_resultado.to_excel(writer, sheet_name="Comparativo", index=False)
    duplicatas_ecoleta.to_excel(writer, sheet_name="Duplicatas_ECOLETA", index=False)
    duplicatas_shp.to_excel(writer, sheet_name="Duplicatas_SHP", index=False)

print(f"Planilha gerada: {nome}")
