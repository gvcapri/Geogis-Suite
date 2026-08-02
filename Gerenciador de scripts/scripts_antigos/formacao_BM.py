import pandas as pd
import re

arquivo_shp = 'ARQUIVO BASE\SHP_Zona Central_Juruena.xlsx'
arquivo_ecoleta = 'ARQUIVO BASE\Ecoleta_Zona Central_Juruena.xlsx'
nomeCombinada = 'Combinada Zona Central_Juruena.xlsx'

# Função para quadra e lote: remove zeros à esquerda + maiúsculo
def padronizar_quadra_lote(texto):
    if pd.isnull(texto):
        return texto
    texto = str(texto).strip()
    texto = texto.lstrip('0')  # remove zeros à esquerda
    if texto == '':
        texto = '0'  # se ficou vazio, coloca 0
    return texto.upper()

# Função para chave de ordenação (parte numérica + parte alfabética)
def chave_ordenacao(valor):
    if pd.isnull(valor):
        return (float('inf'), '')  # valores nulos vão para o fim
    valor = str(valor).strip().lower()
    m = re.match(r'(\d+)(.*)', valor)
    if m:
        num_part = int(m.group(1))
        str_part = m.group(2)
        return (num_part, str_part)
    else:
        # Se não começar com número, joga no fim, ordenando lexicograficamente
        return (float('inf'), valor)

# Leitura das planilhas
df_shp = pd.read_excel(arquivo_shp, dtype=str)
df_ecoleta = pd.read_excel(arquivo_ecoleta, dtype=str)

# Renomear colunas 'Quadra' e 'Lote' da ECOLETA para minúsculas
df_ecoleta = df_ecoleta.rename(columns={'Quadra': 'quadra', 'Lote': 'lote'})

# Seleção automática: pega todas as colunas do SHP
colunas_shp = df_shp.columns.tolist()

# ECOLETA: mantém apenas quadra, lote e as colunas necessárias
colunas_ecoleta = ['Status Processo', 'Nome do Beneficiário', 'CPF do Beneficiário', 'Número do ofício']
df_ecoleta = df_ecoleta[['quadra', 'lote'] + colunas_ecoleta]

# Padronização de quadra e lote
for col in ['quadra', 'lote']:
    df_shp[col] = df_shp[col].apply(padronizar_quadra_lote)
    df_ecoleta[col] = df_ecoleta[col].apply(padronizar_quadra_lote)

df_ecoleta = df_ecoleta.drop_duplicates(subset=['quadra', 'lote'])

# Junção: LEFT JOIN → todos os SHP, completa com ECOLETA se tiver
df_merged = pd.merge(df_shp, df_ecoleta, on=['quadra', 'lote'], how='left')

# Ordena por quadra e lote com chave personalizada para números + letras
df_merged = df_merged.sort_values(by=['quadra', 'lote'], key=lambda col: col.map(chave_ordenacao))

# Exportação
df_merged.to_excel(nomeCombinada, index=False)

print(f"✅ Planilha combinada criada com sucesso: {nomeCombinada}")
