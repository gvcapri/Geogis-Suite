import os
import docx
from docx.shared import Pt
import re

def count_page_breaks(paragraph):
    """
    Conta as quebras de página contidas em um parágrafo do DOCX.
    Detecta quebras manuais e automáticas do Word.
    """
    breaks = 0
    br_elements = paragraph._element.xpath('.//*[local-name()="br" and @*[local-name()="type"]="page"]')
    breaks += len(br_elements)
    lrpb_elements = paragraph._element.xpath('.//*[local-name()="lastRenderedPageBreak"]')
    breaks += len(lrpb_elements)
    return breaks

# Caminho exato do seu arquivo com base no seu log de erro
docx_path = r"C:\onedrive2\OneDrive - Geogis Geotecnologia LTDA\Documentos\Automações\Códigos\MD_LOTES_INTEGRAL_att.docx"

# Validação de segurança para evitar o erro PackageNotFoundError
if not os.path.exists(docx_path):
    print(f"ERRO: O arquivo não foi encontrado no caminho especificado:\n{docx_path}")
    print("\nPROVÁVEL SOLUÇÃO:")
    print("Como o arquivo está no OneDrive, clique sobre ele com o botão direito no seu")
    print("Explorador de Arquivos e selecione: 'Manter sempre neste dispositivo'.")
else:
    # Abre o documento Word original
    doc = docx.Document(docx_path)
    
    memoriais = []
    corrente_memorial = None
    pagina_atual = 1

    # 1. Agrupar os parágrafos por Memorial Descritivo e mapear suas páginas virtuais
    for idx, p in enumerate(doc.paragraphs):
        texto = p.text.strip()
        
        if "MEMORIAL DESCRITIVO" in texto.upper():
            if corrente_memorial is not None:
                memoriais.append(corrente_memorial)
                
            corrente_memorial = {
                "pagina_inicio": pagina_atual,
                "paragrafos": [],
                "lote": "?",
                "quadra": "?"
            }
            
        if corrente_memorial is not None:
            corrente_memorial["paragrafos"].append((pagina_atual, p))
            
        pagina_atual += count_page_breaks(p)

    if corrente_memorial is not None:
        memoriais.append(corrente_memorial)

    print("Analisando páginas e aplicando correções nos memoriais longos...\n")
    
    contador_corrigidos = 0

    # 2. Analisar o tamanho de cada memorial e aplicar formatação corretiva se necessário
    for m in memoriais:
        pagina_inicio = m["pagina_inicio"]
        
        # Identificar LOTE e QUADRA para o relatório do terminal
        texto_completo = "\n".join([p.text for pag, p in m["paragrafos"]])
        match = re.search(r"LOTE[:\s]*([0-9A-Z]+)[\s\-–]*QUADRA[:\s]*([0-9A-Z]+)", texto_completo, re.IGNORECASE)
        if match:
            m["lote"] = match.group(1)
            m["quadra"] = match.group(2)

        # Agrupar o texto limpo por página (sua lógica original de corte)
        texto_por_pagina = {}
        for pag, p in m["paragrafos"]:
            t = p.text.strip()
            texto_limpo = re.sub(r"(Página\s*\d+|MEMORIAL DESCRITIVO.*|LOTEAMENTO.*)", "", t, flags=re.IGNORECASE).strip()
            if pag not in texto_por_pagina:
                texto_por_pagina[pag] = ""
            texto_por_pagina[pag] += texto_limpo

        # Contar páginas reais ocupadas com conteúdo significativo (> 100 caracteres)
        paginas_ocupadas = 1
        paginas_adicionais = [pag for pag in texto_por_pagina if pag > pagina_inicio]
        
        for pag in paginas_adicionais:
            if len(texto_por_pagina[pag]) > 100:
                paginas_ocupadas += 1

        # SE O MEMORIAL OCUPA 2 OU MAIS PÁGINAS, ENTRA A REPROGRAFIA CORRETIVA:
        if paginas_ocupadas > 1:
            print(f"[!] Lote {m['lote']} - Quadra {m['quadra']} ocupava {paginas_ocupadas} páginas. Corrigindo...")
            
            # Ação A: Força o título do memorial a começar sempre no topo de uma página nova
            m["paragrafos"][0][1].paragraph_format.page_break_before = True
            
            # Ação B: Compactar e agrupar as linhas do bloco
            for i, (pag, p) in enumerate(m["paragrafos"]):
                # Impede que parágrafos quebrem linhas de forma órfã
                p.paragraph_format.keep_together = True
                
                # Junta este parágrafo ao próximo, impedindo o Word de cindir o memorial ao meio
                if i < len(m["paragrafos"]) - 1:
                    p.paragraph_format.keep_with_next = True
                
                # Reduz o espaçamento vertical antes e depois do parágrafo para economizar espaço
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                
                # Ajusta para espaçamento entre linhas Simples (1.0)
                p.paragraph_format.line_spacing = 1.0
                
                # Altera o tamanho da fonte de todos os textos (runs) do parágrafo para 10pt
                for run in p.runs:
                    run.font.size = Pt(10)
            
            contador_corrigidos += 1

    # 3. Salvar as alterações em um novo arquivo para não destruir o original
    if contador_corrigidos > 0:
        docx_saida_path = docx_path.replace(".docx", "_Corrigido.docx")
        doc.save(docx_saida_path)
        print(f"\n[SUCESSO] Correção concluída! {contador_corrigidos} memoriais foram ajustados.")
        print(f"O novo arquivo corrigido foi salvo em:\n{docx_saida_path}")
    else:
        print("\n[OK] Nenhum memorial ocupando mais de uma página foi detectado. Nenhuma alteração foi necessária.")