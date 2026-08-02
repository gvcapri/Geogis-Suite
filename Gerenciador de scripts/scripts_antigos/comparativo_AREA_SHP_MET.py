import pandas as pd

arquivo_metrica = r"met_saojorge.xlsx"
arquivo_shp = r"shp_saojorge.xlsx"
nome_saida = " Comparativo ATT - sao jorge"       +".xlsx"   #!!!!!!!!!!!!!!!!NÃO PRECISA COLOCAR .XLSX!!!!!!!!!!!!!!!!!!!  

def padronizar(df):
    df["quadra"] = df["quadra"].astype(str).str.strip().str.upper().str.lstrip("0")
    df["lote"] = df["lote"].astype(str).str.strip().str.upper().str.lstrip("0")
    return df

# Carregar os arquivos
df_metrica = pd.read_excel(arquivo_metrica).rename(columns={"Quadra": "quadra", "Lote": "lote", "Área do lote": "área"})
df_shp = pd.read_excel(arquivo_shp).rename(columns={"quadra": "quadra", "lote": "lote", "area": "área"})

# Padronizar quadra e lote
df_metrica = padronizar(df_metrica[["quadra", "lote", "área"]])
df_shp = padronizar(df_shp[["quadra", "lote", "área"]])

# Tratar áreas
df_metrica["área"] = df_metrica["área"].astype(str).str.replace("m²", "", case=False).str.replace(" ", "").str.replace(".", "").str.replace(",", ".").astype(float)
df_shp["área"] = df_shp["área"].astype(str).str.replace(",", ".").astype(float)

# Arredondar
df_metrica["área"] = df_metrica["área"].round(2)
df_shp["área"] = df_shp["área"].round(2)

# Comparação
df_merged = pd.merge(df_metrica, df_shp, on=["quadra", "lote"], how="outer", suffixes=('_metrica', '_shp'))

def definir_status(row):
    if pd.isna(row['área_metrica']):
        return "Somente no SHP"
    elif pd.isna(row['área_shp']):
        return "Somente na MÉTRICA"
    elif row['área_metrica'] == row['área_shp']:
        return "Presente em ambos - Área igual"
    else:
        return "Presente em ambos - Área diferente"

df_merged['status'] = df_merged.apply(definir_status, axis=1)

df_resultado = df_merged[['quadra', 'lote', 'área_metrica', 'área_shp', 'status']]

with pd.ExcelWriter(nome_saida) as writer:
    df_resultado.to_excel(writer, sheet_name="Comparativo", index=False)

print(f"\n\nPlanilha gerada: {nome_saida}")
