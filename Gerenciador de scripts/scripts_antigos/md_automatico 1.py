import os
import re
import unicodedata
from docx2pdf import convert
from PyPDF2 import PdfReader, PdfWriter

# ================= CONFIGURAÇÕES =================
DOCX_PATH = "MD_LOTES_INTEGRAL_ATT.docx" # <----- insira arquivo docx aqui
PDF_TEMP = "temp.pdf"
OUTPUT_DIR = "MD_lotes" 

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ================= FUNÇÕES =================
def pagina_em_branco(texto):
    return not texto or texto.strip() == ""

def normalizar_nome_lote(texto):
    texto = texto.strip()


    if re.fullmatch(r"\d+(?:\s*[\/\-\s]\s*\d+)+", texto):
        numeros = re.findall(r"\d+", texto)
        return "-".join(n.zfill(2) for n in numeros)

    
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ASCII", "ignore").decode("ASCII")
    texto = texto.upper()
    texto = re.sub(r"[^\w\s]", "", texto)
    texto = re.sub(r"\s+", "_", texto)
    return texto.strip("_")

def salvar_pagina(page, nome):
    writer = PdfWriter()
    writer.add_page(page)
    with open(os.path.join(OUTPUT_DIR, nome), "wb") as f:
        writer.write(f)
    print(f"✔ {nome}")


print("Convertendo DOCX para PDF... Isso pode levar alguns segundos.")
convert(DOCX_PATH, PDF_TEMP)

reader = PdfReader(PDF_TEMP)

memorial_atual = None    # (quadra, identificador)
pagina_contador = 0


regex_cabecalho = re.compile(r"PROPRIEDADE:\s*LOTE:\s*(.*?)\s*-\s*QUADRA:\s*([0-9A-Z]+)", re.IGNORECASE)

for i, page in enumerate(reader.pages):
    texto = page.extract_text()
    texto_upper = texto.upper() if texto else ""

    # Ignora páginas em branco
    if pagina_em_branco(texto_upper):
        continue

    # Procura o cabeçalho de um novo lote
    match = regex_cabecalho.search(texto_upper)

    if match:
        # Encontramos um novo lote!
        lote_bruto = match.group(1).strip()
        quadra_bruto = match.group(2).strip()

        quadra = quadra_bruto.zfill(2)
        identificador = normalizar_nome_lote(lote_bruto)

        novo_memorial = (quadra, identificador)

        # Reseta o contador de páginas apenas se mudou o lote
        if novo_memorial != memorial_atual:
            memorial_atual = novo_memorial
            pagina_contador = 0

    # Se temos um memorial na memória (seja ele novo ou a continuação do anterior)
    if memorial_atual:
        pagina_contador += 1
        quadra, identificador = memorial_atual
        
        # Gera o nome do arquivo. Ex: QD01_LT_10_01.pdf
        nome_pdf = f"QD{quadra}_LT_{identificador}_{str(pagina_contador).zfill(2)}.pdf"
        
        salvar_pagina(page, nome_pdf)
    else:
        print(f"Ignorando página {i+1} (Capa, índice ou não pertence a um lote).")

print("\nProcessamento finalizado com sucesso!")