import pandas as pd
import re
import os
from docx import Document
import unicodedata

# =========================
# CONFIGURAÇÕES
# =========================
ARQUIVO_EXCEL = r"C:\onedrive2\OneDrive - Geogis Geotecnologia LTDA\Documentos\Automações\Códigos\CONFERENCIA_FINAL_REVISADA.xlsx" 
ARQUIVO_CRF_ENTRADA = "CRF - JARDIM DE ALÁ_ATT.docx"
ARQUIVO_SAIDA = "CRF_FINAL_CORRIGIDO.docx"

# =========================
# 1. NORMALIZAÇÃO (Híbrida e Segura)
# =========================
def normalizacao_blindada(val):
    if pd.isna(val) or str(val).strip() == "":
        return ""

    s = str(val).upper().strip()

    # Remove acentos
    s = ''.join(c for c in unicodedata.normalize('NFD', s)
                if unicodedata.category(c) != 'Mn')

    # Remove palavras fixas
    for termo in ["QUADRA", "LOTE", "INDICACAO", "NUMERICA"]:
        s = s.replace(termo, "")

    s = s.strip()

    # ==============================
    # 🔹 ÁREA VERDE / REMANESCENTE
    # ==============================
    if "AREA VERDE" in s:
        numero = re.findall(r'\d+', s)
        if numero:
            return f"AREAVERDE{int(numero[0])}"
        return "AREAVERDE"

    if "AREA REMANESCENTE" in s:
        numero = re.findall(r'\d+', s)
        if numero:
            return f"AREAREMANESCENTE{int(numero[0])}"
        return "AREAREMANESCENTE"

    # ==============================
    # 🔹 LOTE ALFANUMÉRICO (1B, 01B, 1 B, 01 B)
    # ==============================
    s_sem_espaco = re.sub(r'\s+', '', s)

    match_alfanum = re.fullmatch(r'0*(\d+)([A-Z])', s_sem_espaco)
    if match_alfanum:
        numero = int(match_alfanum.group(1))
        letra = match_alfanum.group(2)
        return f"{numero}{letra}"


    # ==============================
    # 🔹 LOTE FRACIONADO (02-03)
    # ==============================
    partes = re.split(r'[ \/\-\\&]+', s)
    resultado = []

    for p in partes:
        p_num = re.sub(r'[^0-9]', '', p)
        if p_num:
            resultado.append(str(int(p_num)))

    if resultado:
        return "_".join(resultado)

    # ==============================
    # 🔹 TEXTO GERAL
    # ==============================
    return re.sub(r'\W+', '', s)


def float_para_str_br(valor):
    """ Converte 1177.58 para '1.177,58' """
    try:
        # 1. Formata no padrão americano primeiro (ex: 1,177.58)
        formatado = f"{float(valor):,.2f}"
        
        # 2. Inverte os sinais para o padrão BR (ex: 1.177,58)
        # Substitui a vírgula por X temporariamente, troca o ponto por vírgula, e o X por ponto.
        return formatado.replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return str(valor)

# =========================
# 2. CARREGAR EXCEL (GABARITO CORRIGIDO)
# =========================
def carregar_mapa_excel(caminho):
    print(f"📊 Lendo Excel: {caminho}...")
    try:
        df = pd.read_excel(caminho) 
    except Exception as e:
        print(f"❌ Erro ao abrir Excel: {e}")
        return {}

    # --- CORREÇÃO AQUI: Normalização dos nomes das colunas para busca ---
    # Criamos um dicionário que mapeia o nome "limpo" ao nome real da coluna
    colunas_reais = {str(col).strip().upper(): col for col in df.columns}
    
    # Busca dinâmica que ignora espaços e maiúsculas
    col_q = next((orig for limpo, orig in colunas_reais.items() if "QUADRA" in limpo), None)
    col_l = next((orig for limpo, orig in colunas_reais.items() if "LOTE" in limpo), None)
    
    # Procura colunas de VALOR CORRETO (Área e Perímetro)
    col_area_alvo = next((orig for limpo, orig in colunas_reais.items() if "AREA" in limpo and ("EXCE" in limpo or "MD" in limpo)), None)
    col_peri_alvo = next((orig for limpo, orig in colunas_reais.items() if "PERI" in limpo and ("EXCE" in limpo or "MD" in limpo)), None)

    if not (col_q and col_l):
        print("❌ Erro: Colunas Quadra/Lote não encontradas.")
        print(f"🔎 Colunas lidas no arquivo: {list(df.columns)}")
        return {}
    
    print(f"   Colunas identificadas: Q='{col_q}', L='{col_l}', Área='{col_area_alvo}', Peri='{col_peri_alvo}'")

    mapa = {}
    for _, row in df.iterrows():
        q_limpa = normalizacao_blindada(row[col_q])
        l_limpo = normalizacao_blindada(row[col_l])
        
        dados = {}
        if col_area_alvo and pd.notna(row[col_area_alvo]):
            try: dados['area'] = float(str(row[col_area_alvo]).replace(",", "."))
            except: pass
            
        if col_peri_alvo and pd.notna(row[col_peri_alvo]):
            try: dados['peri'] = float(str(row[col_peri_alvo]).replace(",", "."))
            except: pass
            
        if dados:
            mapa[(q_limpa, l_limpo)] = dados

    print(f"✅ Mapa de correções carregado: {len(mapa)} lotes.")
    return mapa

# =========================
# 3. CORREÇÃO NO WORD (LÓGICA MANTIDA)
# =========================
def corrigir_word(caminho_entrada, caminho_saida, mapa_correcoes):
    print(f"🔧 Processando Word...")
    try:
        doc = Document(caminho_entrada)
    except Exception as e:
        print(f"❌ Erro ao abrir Word: {e}")
        return

    regex_quadra = re.compile(r"QUADRA\s*([0-9A-Z]+)", re.IGNORECASE)
    regex_lote = re.compile(r"LOTE\s*:?\s*([^\n\r]+)", re.IGNORECASE)
    regex_area = re.compile(r"(ÁREA(?: TOTAL)?\s*:?\s*)([\d\.,]+)(\s*m²?)", re.IGNORECASE)
    regex_peri = re.compile(r"(PERÍMETRO\s*:?\s*)([\d\.,]+)(\s*m?)", re.IGNORECASE)

    quadra_atual = None
    lote_atual = None
    count_area = 0
    count_peri = 0

    for p in doc.paragraphs:
        texto = p.text.strip()
        if not texto: continue

        m_q = regex_quadra.search(texto)
        if m_q:
            quadra_atual = normalizacao_blindada(m_q.group(1))
        
        m_l = regex_lote.search(texto)
        if m_l:
            lote_atual = normalizacao_blindada(m_l.group(1))

        if quadra_atual and lote_atual:
            chave = (quadra_atual, lote_atual)
            if chave in mapa_correcoes:
                alvos = mapa_correcoes[chave]
                
                # Correção de Área
                if "ÁREA" in texto.upper() and 'area' in alvos:
                    m_val = regex_area.search(texto)
                    if m_val:
                        v_antigo, v_novo = m_val.group(2), float_para_str_br(alvos['area'])
                        if v_antigo != v_novo:
                            p.text = texto.replace(v_antigo, v_novo)
                            print(f"✅ ÁREA Q:{quadra_atual} L:{lote_atual} | {v_antigo} -> {v_novo}")
                            count_area += 1
                            texto = p.text # Atualiza texto para o perímetro na mesma linha

                # Correção de Perímetro
                if "PERÍMETRO" in texto.upper() and 'peri' in alvos:
                    m_val = regex_peri.search(texto)
                    if m_val:
                        v_antigo, v_novo = m_val.group(2), float_para_str_br(alvos['peri'])
                        if v_antigo != v_novo:
                            p.text = texto.replace(v_antigo, v_novo)
                            print(f"✅ PERÍMETRO Q:{quadra_atual} L:{lote_atual} | {v_antigo} -> {v_novo}")
                            count_peri += 1

    doc.save(caminho_saida)
    print(f"\n🏆 CONCLUÍDO! Área: {count_area} | Peri: {count_peri}")

# =========================
# EXECUÇÃO
# =========================
if __name__ == "__main__":
    if os.path.exists(ARQUIVO_EXCEL) and os.path.exists(ARQUIVO_CRF_ENTRADA):
        mapa = carregar_mapa_excel(ARQUIVO_EXCEL)
        if mapa:
            corrigir_word(ARQUIVO_CRF_ENTRADA, ARQUIVO_SAIDA, mapa)
    else:
        print("❌ Arquivos não encontrados. Verifique os caminhos.")