import pandas as pd
import re

caminho_ficheiro = '26.xlsx'

# Usamos read_excel para ler o ficheiro .xlsx
df = pd.read_excel(caminho_ficheiro, skiprows=2)

def processar_medida(texto):
    if pd.isna(texto):
        return texto
    
    # Separa pelo '|' e pega apenas a primeira parte (antes dos nomes dos confrontantes)
    medidas_texto = str(texto).split('|')[0]
    
    # Extrai todos os números que estão no formato "00,00" ou "00"
    numeros_str = re.findall(r'(\d+,\d+|\d+)', medidas_texto)
    
    if not numeros_str:
        return texto
        
    # Converte para decimais (substituindo vírgula por ponto) e soma
    soma_total = 0.0
    for num_str in numeros_str:
        num = float(num_str.replace(',', '.'))
        soma_total += num
        
    # Retorna o valor somado reformatado com vírgula, AGORA SEM O " m"
    return f"{soma_total:.2f}".replace('.', ',')

# Colunas que precisam de ser tratadas
colunas_para_processar = ['Frente', 'Direita', 'Esquerda', 'Fundo']

# Aplica a função nas colunas especificadas
for col in colunas_para_processar:
    if col in df.columns:
        df[col] = df[col].apply(processar_medida)

# Guarda o resultado num novo ficheiro Excel (.xlsx)
caminho_saida = caminho_ficheiro + '_processado.xlsx'
df.to_excel(caminho_saida, index=False)

print("Processamento concluído! As medidas foram somadas e a letra 'm' foi removida.")