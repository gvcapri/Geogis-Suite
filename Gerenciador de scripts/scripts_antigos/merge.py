import pandas as pd

# Arquivos
arquivo_vj = "Relatorio Ambiental_Contrato VJ.xlsx"
arquivo_vrc = "Relatório_Ambiental_Contrato_VRC.xlsx"

# Ler planilhas
df_vj = pd.read_excel(arquivo_vj)
df_vrc = pd.read_excel(arquivo_vrc)

# Criar coluna de contrato
df_vj["Contrato"] = "VJ"
df_vrc["Contrato"] = "VRC"

# Padronizar coluna de localização
df_vj["Localidade"] = df_vj["Bairro"]
df_vrc["Localidade"] = df_vrc["Núcleos"]

# (opcional) remover colunas antigas para não duplicar
df_vj = df_vj.drop(columns=["Bairro"])
df_vrc = df_vrc.drop(columns=["Núcleos"])

# Garantir que as colunas estejam na mesma ordem
colunas_padrao = [
    "Contrato",
    "Localidade",
    "Ambiental",
    "Relatório Ambiental",
    "Fotos",
    "Mapa Sitação Ambiental"
]

df_vj = df_vj[colunas_padrao]
df_vrc = df_vrc[colunas_padrao]

# Juntar as planilhas
df_final = pd.concat([df_vj, df_vrc], ignore_index=True)

# Salvar resultado final
df_final.to_excel("Relatorio_Ambiental_Todos_Contratos.xlsx", index=False)

print("Planilhas unidas e padronizadas com sucesso!")
