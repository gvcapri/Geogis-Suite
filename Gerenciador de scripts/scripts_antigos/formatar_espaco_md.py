import os
from docx import Document

def remover_enters_excessivos():
    # 1. Entrada do caminho
    caminho = input("Cole o caminho do arquivo .docx: ").strip().replace('"', '').replace("'", "")
    
    if not os.path.exists(caminho):
        print("Arquivo não encontrado.")
        return

    # 2. Carrega o documento original
    doc = Document(caminho)
    
    # 3. Identifica parágrafos que estão totalmente vazios e os remove
    # Fazemos a varredura de trás para frente para não perder o índice ao deletar
    for p in reversed(doc.paragraphs):
        # Se o parágrafo não tem texto e não tem imagens (inline_shapes)
        if not p.text.strip() and not p.runs:
            # Acessa o elemento XML do parágrafo e o remove do pai
            p._element.getparent().remove(p._element)
        elif not p.text.strip():
            # Verifica se há imagens dentro dos runs antes de apagar
            tem_imagem = False
            for run in p.runs:
                if run.element.xpath('.//w:drawing') or run.element.xpath('.//w:pict'):
                    tem_imagem = True
                    break
            if not tem_imagem:
                p._element.getparent().remove(p._element)

    # 4. Salva as alterações no mesmo arquivo ou em um novo
    nome_saida = caminho.replace(".docx", "_LIMPO.docx")
    doc.save(nome_saida)
    
    print(f"\nPronto! Os 'Enters' vazios foram removidos.")
    print(f"Arquivo salvo como: {nome_saida}")

if __name__ == "__main__":
    remover_enters_excessivos()