import os
import glob
import fitz  # PyMuPDF

def processar_lote_pdf():
    print("Iniciando automação com Posicionamento Inteligente (Ajuste Fino)...")

    # =========================================================================
    # 1. CONFIGURAÇÕES DOS ARQUIVOS
    # =========================================================================
    pasta_pdfs = r"C:\Users\Rafael Honorato\Downloads\Nova pasta 5"
    caminho_assinatura = r"C:\onedrive2\OneDrive - Geogis Geotecnologia LTDA\Área de Trabalho\Assinatura Thiago.jpeg"
    caminho_logo = r"C:\onedrive2\OneDrive - Geogis Geotecnologia LTDA\Área de Trabalho\Prancheta 1.jpg"
    # =========================================================================

    if not os.path.exists(pasta_pdfs):
        print(f"ERRO: A pasta '{pasta_pdfs}' não existe.")
        return
    if not os.path.exists(caminho_assinatura):
        print(f"ERRO: Assinatura não encontrada em '{caminho_assinatura}'.")
        return
    if not os.path.exists(caminho_logo):
        print(f"ERRO: Logo não encontrada em '{caminho_logo}'.")
        return

    arquivos_pdf = glob.glob(os.path.join(pasta_pdfs, "*.pdf"))
    if not arquivos_pdf:
        print("Nenhum arquivo PDF encontrado na pasta.")
        return

    print(f"Foram encontrados {len(arquivos_pdf)} arquivos. Processando...\n")

    sucesso = 0
    erros = 0

    for arquivo in arquivos_pdf:
        nome_arquivo = os.path.basename(arquivo)
        
        try:
            doc = fitz.open(arquivo)
            pagine = doc[0]
            
            rect_assinatura = None
            rect_logo = None

            # --- POSICIONAMENTO DINÂMICO (BUSCA POR TEXTO) ---
            
            # 1. Procura o nome do responsável para ancorar a ASSINATURA
            textos_nome = pagine.search_for("Thiago Costa Marques Ninomiya")
            if textos_nome:
                r_nome = textos_nome[0] 
                
                # AJUSTE FINO AQUI:
                # r_nome.x0 e x1 limitam a largura exatamente à largura do texto.
                # r_nome.y0 - 40 define o topo (para não invadir a linha de cima).
                # r_nome.y0 - 5 define a base (logo acima da linha preta do nome).
                # Caixa ajustada exatamente para o retângulo preto do carimbo
                rect_assinatura = fitz.Rect(r_nome.x0 + 15, r_nome.y0 - 35, r_nome.x1 - 15, r_nome.y0 - 8)
            else:
                print(f" [{nome_arquivo}] AVISO: Nome 'Thiago' não encontrado. Assinatura será pulada.")

            # 2. Procura a palavra DATUM para ancorar a LOGO
            textos_datum = pagine.search_for("DATUM/FUSO/MC")
            if textos_datum:
                r_datum = textos_datum[0]
                rect_logo = fitz.Rect(r_datum.x1 + 60, r_datum.y0 - 80, r_datum.x1 + 240, r_datum.y1 + 10)
            else:
                rect_logo = fitz.Rect(640, 450, 810, 550)

            # --- VERIFICAÇÃO E INSERÇÃO ---
            tem_assinatura = False
            tem_logo = False

            imagens_na_pagina = pagine.get_image_info()
            
            for img in imagens_na_pagina:
                if "bbox" in img:
                    bbox_imagem = fitz.Rect(img["bbox"])
                    if rect_assinatura and bbox_imagem.intersects(rect_assinatura):
                        tem_assinatura = True
                    if rect_logo and bbox_imagem.intersects(rect_logo):
                        tem_logo = True

            modificado = False

            if rect_assinatura and not tem_assinatura:
                pagine.insert_image(rect_assinatura, filename=caminho_assinatura)
                print(f" [{nome_arquivo}] -> Assinatura inserida perfeitamente sobre o nome.")
                modificado = True
            elif tem_assinatura:
                print(f" [{nome_arquivo}] -> Assinatura já detectada (ignorada).")

            if rect_logo and not tem_logo:
                pagine.insert_image(rect_logo, filename=caminho_logo)
                print(f" [{nome_arquivo}] -> Logo inserida.")
                modificado = True
            elif tem_logo:
                print(f" [{nome_arquivo}] -> Logo já detectada (ignorada).")

            if modificado:
                doc.saveIncr()
                sucesso += 1
            
            doc.close()

        except Exception as e:
            print(f" ❌ ERRO ao processar {nome_arquivo}: {e}")
            erros += 1

    print("\n" + "="*45)
    print("RESUMO DO PROCESSAMENTO")
    print(f"PDFs modificados com sucesso: {sucesso}")
    print(f"Arquivos com erro: {erros}")
    print("="*45)

if __name__ == "__main__":
    processar_lote_pdf()