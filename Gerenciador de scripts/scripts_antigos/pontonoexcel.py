import pandas as pd

# ===== CONFIGURAÇÕES =====
arquivo_entrada = 'excel_corrigido_pelo_word_Guariba.xlsx'
arquivo_saida = 'Guaribacomponto.xlsx'

colunas_formatar = [
    'Área do lote',
    'Perímetro do lote'
]
# =========================


def adicionar_ponto_milhar(valor):
    if pd.isna(valor):
        return valor

    valor_str = str(valor).strip()

    # Se não tiver vírgula, considera inteiro
    if ',' in valor_str:
        parte_inteira, parte_decimal = valor_str.split(',', 1)
        parte_decimal = ',' + parte_decimal
    else:
        parte_inteira = valor_str
        parte_decimal = ''

    # Remove pontos antigos (caso existam)
    parte_inteira = parte_inteira.replace('.', '')

    # Só formata se for número >= 1000
    try:
        if int(parte_inteira) >= 1000:
            parte_inteira = f"{int(parte_inteira):,}".replace(',', '.')
    except:
        return valor_str

    return parte_inteira + parte_decimal


# Lê o Excel
df = pd.read_excel(arquivo_entrada, dtype=str)

# Aplica somente nas colunas desejadas
for coluna in colunas_formatar:
    if coluna in df.columns:
        df[coluna] = df[coluna].apply(adicionar_ponto_milhar)

# Salva o arquivo final
df.to_excel(arquivo_saida, index=False)

print('Arquivo gerado com sucesso:', arquivo_saida)
