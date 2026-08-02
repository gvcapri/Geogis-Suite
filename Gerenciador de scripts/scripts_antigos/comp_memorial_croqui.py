import re
import pandas as pd
import pypdf
import os

def normalize_value(val):
    if val is None: return ""
    s = str(val).strip().upper()
    # Remove zeros à esquerda (ex: "01" -> "1", "05" -> "5")
    match = re.match(r'0+([1-9A-Z].*)', s)
    return match.group(1) if match else s

def extract_area(text_val):
    if not text_val: return 0.0
    # Limpa formatação brasileira (8.432,10 -> 8432.10)
    clean = re.sub(r'[^\d,.]', '', str(text_val))
    if ',' in clean:
        clean = clean.replace('.', '').replace(',', '.')
    try:
        return float(clean)
    except:
        return 0.0

def processar_paginas_pdf(caminho_pdf, caminho_excel_base):
    # 1. Preparar a base de dados do Excel
    df_base = pd.read_excel(caminho_excel_base)
    df_base['Q_Key'] = df_base['Quadra'].apply(normalize_value)
    df_base['L_Key'] = df_base['Lote'].apply(normalize_value)
    df_base['A_Key'] = df_base['Área do lote'].apply(extract_area)

    resultados = []

    # 2. Abrir o PDF e iterar por cada página
    print(f"Lendo arquivo: {caminho_pdf}...")
    with open(caminho_pdf, 'rb') as f:
        reader = pypdf.PdfReader(f)
        total_paginas = len(reader.pages)
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if not text: continue
            
            # Extração via Regex (Baseada no seu modelo de memorial)
            quadra_match = re.search(r'Quadra\s*(\d+)', text, re.I)
            lote_match = re.search(r'Lote\s*([0-9A-Z]+)', text, re.I)
            area_match = re.search(r'Área:\s*([\d.,\s]+m²)', text, re.I)
            
            q_doc = normalize_value(quadra_match.group(1)) if quadra_match else "N/D"
            l_doc = normalize_value(lote_match.group(1)) if lote_match else "N/D"
            a_doc = extract_area(area_match.group(1)) if area_match else 0.0
            
            # 3. Comparação com o Excel
            match = df_base[(df_base['Q_Key'] == q_doc) & (df_base['L_Key'] == l_doc)]
            
            status = ""
            area_excel = "N/A"
            
            if not match.empty:
                area_excel = match.iloc[0]['A_Key']
                # Diferença menor que 0.01 para evitar erros de arredondamento
                if abs(area_excel - a_doc) < 0.01:
                    status = "✅ CONFERE"
                else:
                    status = f"❌ DIVERGÊNCIA (Excel: {area_excel})"
            else:
                status = "⚠️ LOTE NÃO ENCONTRADO NO EXCEL"
            
            # Adiciona ao relatório
            resultados.append({
                'Página': i + 1,
                'Quadra_PDF': q_doc,
                'Lote_PDF': l_doc,
                'Area_PDF': a_doc,
                'Area_Excel': area_excel,
                'Status': status
            })
            print(f"Pág {i+1}/{total_paginas}: Quadra {q_doc} Lote {l_doc} -> {status}")

    # 4. Gerar Excel de saída
    df_relatorio = pd.DataFrame(resultados)
    nome_saida = "relatorio_conferencia_paginas_FAKE.xlsx"
    df_relatorio.to_excel(nome_saida, index=False)
    print(f"\n--- Concluído! Relatório salvo como: {nome_saida} ---")

# --- EXECUÇÃO ---
# Certifique-se de que os nomes dos arquivos abaixo estão corretos na sua pasta
processar_paginas_pdf('md_lotes_croqui.pdf', 'met_saojorge.xlsx')