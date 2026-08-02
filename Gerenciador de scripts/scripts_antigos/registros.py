import pandas as pd
import re

def normalizar_valor(valor):
    """
    Padroniza Quadras e Lotes: remove zeros à esquerda, 
    espaços e caracteres especiais (hífens/pontos).
    """
    if pd.isna(valor):
        return ""
    # Converte para string, remove espaços e coloca em maiúsculo
    s = str(valor).strip().upper()
    # Remove zeros à esquerda (ex: 05 -> 5 ou 05B -> 5B)
    s = re.sub(r'\b0+', '', s)
    # Remove hífens ou pontos (ex: 05-B vira 5B)
    s = s.replace("-", "").replace(".", "")
    return s

# 1. Carregar os arquivos Excel
# Certifique-se de que os nomes dos arquivos estão corretos
df_registrados = pd.read_excel('REGISTRADOS_SERRA DOURADA.xlsx')
df_ecoleta = pd.read_excel('ECOLETA_SERRA DOURADA.xlsx')

# 2. Criar colunas temporárias para comparação (sem alterar as originais)
df_registrados['lote_norm'] = df_registrados['lote'].apply(normalizar_valor)
df_registrados['quadra_norm'] = df_registrados['quadra'].apply(normalizar_valor)

df_ecoleta['lote_norm'] = df_ecoleta['Lote'].apply(normalizar_valor)
df_ecoleta['quadra_norm'] = df_ecoleta['Quadra'].apply(normalizar_valor)

# 3. Selecionar as colunas que queremos trazer da Ecoleta
# Adicionamos o CPF aqui
ecoleta_dados = df_ecoleta[['quadra_norm', 'lote_norm', 'Nome do Beneficiário', 'CPF do Beneficiário']]

# 4. Cruzamento dos dados (Merge)
df_final = pd.merge(
    df_registrados, 
    ecoleta_dados, 
    on=['quadra_norm', 'lote_norm'], 
    how='left'
)

# 5. Regra de Negócio: Se registro NÃO for 'Sim', limpa o Nome e o CPF
mask_nao_registrado = df_final['registro'].astype(str).str.strip().str.lower() != 'sim'
df_final.loc[mask_nao_registrado, ['Nome do Beneficiário', 'CPF do Beneficiário']] = ""

# 6. Remover as colunas de suporte (normalização) antes de salvar
df_final = df_final.drop(columns=['lote_norm', 'quadra_norm'])

# 7. Salvar o resultado final
df_final.to_excel('RESULTADO_COM_CPF.xlsx', index=False)

print("Sucesso! O arquivo 'RESULTADO_COM_CPF.xlsx' foi gerado com Nomes e CPFs normalizados.")