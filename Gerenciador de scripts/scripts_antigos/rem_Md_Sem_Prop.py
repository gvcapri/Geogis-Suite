import fitz  # PyMuPDF
from pypdf import PdfReader, PdfWriter

pdf_gerado = r"Final QD_10.pdf"
nome_saida = f"Final QD_10.pdf"

pdf_document = fitz.open(pdf_gerado)

# Palavras ou expressões típicas que indicam a presença de corpo de texto
indicadores_corpo_texto = [
    "PROPRIETÁRIO"
]

# Armazenar as páginas sem corpo de texto (base 0 para facilitar uso depois)
paginas_sem_corpo = []

# Analisar todas as páginas
for num_pagina in range(len(pdf_document)):
    pagina = pdf_document[num_pagina]
    texto = pagina.get_text()
    
    # Verifica se algum indicador está presente
    if not any(indicador in texto for indicador in indicadores_corpo_texto):
        paginas_sem_corpo.append(num_pagina)  # base 0 aqui

print(paginas_sem_corpo)

pdf_document.close()

# Agora abrir o PDF pelo pypdf usando o caminho do arquivo
reader = PdfReader(pdf_gerado)
writer = PdfWriter()

# Adicionar somente as páginas que NÃO estão sem corpo de texto
for i in range(len(reader.pages)):
    if i not in paginas_sem_corpo:
        writer.add_page(reader.pages[i])

# Salvar o novo PDF
with open(nome_saida, "wb") as f:
    writer.write(f)

print(f"Páginas removidas com sucesso! Arquivo salvo como '{nome_saida}'")
