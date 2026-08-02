from docx import Document

def remover_paragrafo_seguro(p):
    """Remove o parágrafo da estrutura do Word sem deixar rastros ou corromper o arquivo."""
    p_element = p._element
    p_element.getparent().remove(p_element)
    p._p = p._element = None

def corrigir_paginacao_memorial(caminho_arquivo):
    try:
        doc = Document(caminho_arquivo)
        
        paragrafos_para_remover = []
        verificando_espacos = False
        
        for p in doc.paragraphs:
            # Pegamos o texto e removemos espaços das pontas para análise
            texto = p.text.strip()
            texto_upper = texto.upper()
            
            # 1. Ativa a verificação ao encontrar "PERÍMETRO"
            if "PERÍMETRO:" in texto_upper or "PERÍMETRO" in texto_upper:
                verificando_espacos = True
                continue
                
            # 2. Desativa a verificação ao encontrar o texto principal
            if "INICIA-SE A DESCRIÇÃO" in texto_upper:
                verificando_espacos = False
                continue
                
            # 3. Se estivermos no trecho crítico (entre o perímetro e o início do texto)
            if verificando_espacos:
                # Se for a palavra "DESCRIÇÃO", nós preservamos
                if "DESCRIÇÃO" in texto_upper:
                    continue
                
                # Se o parágrafo estiver vazio ou tiver apenas espaços/quebras
                if texto == "":
                    paragrafos_para_remover.append(p)

        # Removemos todos os parágrafos vazios encontrados de uma vez
        for p in paragrafos_para_remover:
            remover_paragrafo_seguro(p)
            
        # Salva o arquivo com um novo nome
        novo_nome = caminho_arquivo.replace(".docx", "_PAGINACAO_CORRIGIDA.docx")
        doc.save(novo_nome)
        print(f"Sucesso! Foram removidos {len(paragrafos_para_remover)} parágrafos vazios.")
        print(f"Arquivo salvo como: {novo_nome}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Executar
corrigir_paginacao_memorial("MD_LOTES_INTEGRAL_att.docx")