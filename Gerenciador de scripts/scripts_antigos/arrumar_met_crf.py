import pandas as pd
import re
from docx import Document

def normalizar(valor):
    if pd.isna(valor): return ""
    s = str(valor).strip().upper()
    # Padroniza números (ex: 01 vira 1)
    s = re.sub(r'\d+', lambda m: str(int(m.group(0))), s)
    return s

def formatar_br(valor, unidade):
    if valor is None: return ""
    # Retorna no formato 1.234,56
    return f"{float(valor):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') + f" {unidade}"

def extrair_float(texto):
    if not texto: return None
    # Remove unidades e converte formato BR para float
    limpo = texto.replace(' m²', '').replace(' m', '').replace('.', '').replace(',', '.')
    try: return float(limpo)
    except: return None

def corrigir_met_via_word(caminho_word, caminho_excel):
    print(f"📖 Lendo documento Word: {caminho_word}")
    doc = Document(caminho_word)
    
    # Dicionário para armazenar os dados extraídos do Word
    # Chave: (Quadra, Lote) -> Valor: {'area': float, 'perimetro': float}
    dados_word = {}
    
    # Regex para capturar os dados no Word
    # Exemplo esperado: LOTE: 03 - QUADRA: 01 ... ÁREA: 253,40 m² PERÍMETRO: 72,17 m
    re_lote_quadra = re.compile(r"LOTE:\s*([^-\n]+)\s*-\s*QUADRA:\s*([^\s\n]+)", re.IGNORECASE)
    re_area = re.compile(r"ÁREA:\s*([\d.,]+)\s*m²?", re.IGNORECASE)
    re_perim = re.compile(r"PERÍMETRO:\s*([\d.,]+)\s*m?", re.IGNORECASE)

    for p in doc.paragraphs:
        texto = p.text
        match_lq = re_lote_quadra.search(texto)
        if match_lq:
            lote_str = normalizar(match_lq.group(1))
            quadra_str = normalizar(match_lq.group(2))
            
            m_area = re_area.search(texto)
            m_perim = re_perim.search(texto)
            
            if m_area and m_perim:
                area_val = extrair_float(m_area.group(1))
                perim_val = extrair_float(m_perim.group(1))
                dados_word[(quadra_str, lote_str)] = {'area': area_val, 'perim': perim_val}

    print(f"✅ {len(dados_word)} memoriais encontrados no Word.")

    # Carregar Excel
    print(f"📊 Lendo Excel: {caminho_excel}")
    df = pd.read_excel(caminho_excel)
    
    alteracoes = 0
    for idx, row in df.iterrows():
        q_excel = normalizar(row['Quadra'])
        l_excel = normalizar(row['Lote'])
        chave = (q_excel, l_excel)
        
        if chave in dados_word:
            valor_word_a = dados_word[chave]['area']
            valor_word_p = dados_word[chave]['perim']
            
            valor_excel_a = extrair_float(str(row['Área do lote']))
            valor_excel_p = extrair_float(str(row['Perímetro do lote']))
            
            # Comparar e corrigir se houver diferença
            if abs(valor_excel_a - valor_word_a) > 0.001 or abs(valor_excel_p - valor_word_p) > 0.001:
                df.at[idx, 'Área do lote'] = formatar_br(valor_word_a, 'm²')
                df.at[idx, 'Perímetro do lote'] = formatar_br(valor_word_p, 'm')
                print(f"⚡ Corrigido: Q {row['Quadra']} L {row['Lote']}")
                alteracoes += 1

    # Salvar
    saida = "MET_Corrigida_pelo_Word.xlsx"
    df.to_excel(saida, index=False)
    print(f"\n✅ Pronto! {alteracoes} correções feitas.")
    print(f"Arquivo salvo como: {saida}")

# Execução
corrigir_met_via_word('MD_Lotes_Integral_JD_de_Alá.docx', 'MET_Jd_Ala_VG.xlsx')