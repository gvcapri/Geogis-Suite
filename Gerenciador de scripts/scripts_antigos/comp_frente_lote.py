import pandas as pd
import re
import unicodedata
from docx import Document

def normalizar_texto(texto):
    """Remove acentos, espaços extras e deixa tudo em maiúsculo para comparação exata."""
    if pd.isna(texto):
        return ""
    texto = str(texto).upper().strip()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return texto

def limpar_lote(lote):
    """Padroniza o formato do lote (ex: '01- B' ou '02A' viram '01B' ou '02A')."""
    return normalizar_texto(lote).replace(" ", "").replace("-", "")

def extrair_dados_docx(caminho_docx):
    doc = Document(caminho_docx)
    texto_completo = "\n".join([p.text for p in doc.paragraphs])
    
    memoriais = re.split(r'MEMORIAL DESCRITIVO', texto_completo, flags=re.IGNORECASE)
    
    dados_extraidos = []
    
    for memorial in memoriais:
        if not memorial.strip():
            continue
            
        # Captura Lote e Quadra
        padrao_lote_quadra = r'LOTE:\s*(.*?)\s*(?:-|–)\s*QUADRA:\s*(\w+)'
        match_lote = re.search(padrao_lote_quadra, memorial, re.IGNORECASE)
        
        # Captura a rua de frente
        padrao_frente = r'de frente.*?confrontando com\s+([^,\n]+)'
        match_frente = re.search(padrao_frente, memorial, re.IGNORECASE)
        
        if match_lote and match_frente:
            lote = match_lote.group(1).strip()
            quadra = match_lote.group(2).strip()
            rua_frente = match_frente.group(1).strip()
            
            dados_extraidos.append({
                'Quadra': str(int(quadra)) if quadra.isdigit() else quadra,
                'Lote': limpar_lote(lote),
                'Frente_Word': rua_frente
            })
            
    return pd.DataFrame(dados_extraidos)

def comparar_frentes(caminho_docx, caminho_excel):
    print("Extraindo dados do Word...")
    df_word = extrair_dados_docx(caminho_docx)
    
    print("Lendo dados do Excel...")
    # Lê o arquivo .xlsx diretamente
    df_excel = pd.read_excel(caminho_excel)
    
    # Padroniza as colunas do Excel para o cruzamento
    df_excel['Quadra_Norm'] = df_excel['quadra'].apply(lambda x: str(int(x)) if str(x).isdigit() else str(x))
    df_excel['Lote_Norm'] = df_excel['lote'].apply(limpar_lote)
    
    # Realiza o cruzamento (Merge) usando Quadra e Lote
    df_comparativo = pd.merge(
        df_word, 
        df_excel[['Quadra_Norm', 'Lote_Norm', 'rua']], 
        left_on=['Quadra', 'Lote'], 
        right_on=['Quadra_Norm', 'Lote_Norm'], 
        how='left'
    ).rename(columns={'rua': 'Frente_Excel'})
    
    # Regra de Validação
    def verificar_frente(row):
        if pd.isna(row['Frente_Excel']):
            return "Lote não encontrado no Excel"
            
        word_norm = normalizar_texto(row['Frente_Word'])
        excel_norm = normalizar_texto(row['Frente_Excel'])
        
        # Verifica se o logradouro do Word está contido no logradouro do Excel ou vice-versa
        if word_norm in excel_norm or excel_norm in word_norm:
            return "Correto"
        else:
            return "Divergente"
            
    df_comparativo['Status_Frente'] = df_comparativo.apply(verificar_frente, axis=1)
    
    # Organiza e exporta o resultado
    colunas_finais = ['Quadra', 'Lote', 'Frente_Word', 'Frente_Excel', 'Status_Frente']
    df_final = df_comparativo[colunas_finais]
    
    print("\n--- Resumo da Comparação ---")
    print(df_final['Status_Frente'].value_counts())
    
    # Salva o relatório em formato Excel (.xlsx)
    df_final.to_excel('Relatorio_Divergencias_Frentes.xlsx', index=False)
    print("\nRelatório completo salvo como 'Relatorio_Divergencias_Frentes.xlsx'.")
    
    return df_final

# Mude o final do arquivo de Excel para corresponder ao nome exato do seu arquivo (.xlsx)
caminho_docx = r"MD_Lotes_Ouro_Verde_att.docx"
caminho_excel = r"shp_ouroverde.xlsx"

df_resultado = comparar_frentes(caminho_docx, caminho_excel)