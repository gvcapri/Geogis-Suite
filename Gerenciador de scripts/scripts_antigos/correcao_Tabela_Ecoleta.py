import pandas as pd
import string 
import re

file_path = r"ARQUIVO BASE\Ecoleta_Zona Central_Juruena.xlsx"  # Caminho da planilha
nome = 'Corrigido Zona Central_Juruena.xlsx'  # Nome da Planilha formatada 

df = pd.read_excel(file_path, dtype=str, engine="openpyxl")

def formatar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, str(cpf)))
    if len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf  

def formatar_expedidor(expedidor):
    if pd.isna(expedidor):
        return ''
    expedidor = str(expedidor).strip().upper().replace(' ', '')
    if expedidor in ['NULL', 'NULO', 'NAN']:
        return ''
    if expedidor == 'DPF':
        return expedidor
    if '/' in expedidor:
        return expedidor
    match = re.match(r'^([A-Z]+)([A-Z]{2})$', expedidor)
    if match:
        return f'{match.group(1)}/{match.group(2)}'
    return expedidor

def remover_rua(texto):
    if pd.isna(texto):
        return ''
    return re.sub(r"\bru[áa]\b", "", str(texto), flags=re.IGNORECASE).strip()

# Aplicações
df["Profissão"] = df["Profissão"].astype(str).apply(string.capwords)
df["Profissão do Cônjuge"] = df["Profissão do Cônjuge"].astype(str).apply(string.capwords)
df["Nome do Beneficiário"] = df["Nome do Beneficiário"].astype(str).apply(string.capwords)
df["Nome do Cônjuge"] = df["Nome do Cônjuge"].astype(str).apply(string.capwords)
df["CPF do Beneficiário"] = df["CPF do Beneficiário"].apply(formatar_cpf).astype(str)
df["CPF do Cônjuge"] = df["CPF do Cônjuge"].apply(formatar_cpf).astype(str)
df["Logradouro"] = df["Logradouro"].apply(remover_rua).astype(str).apply(string.capwords)
df["Órg. Exp. RG Benef."] = df["Órg. Exp. RG Benef."].apply(formatar_expedidor)
df["Órg. Exp. RG Conj."] = df["Órg. Exp. RG Conj."].apply(formatar_expedidor)
df["Regime de Casamento"] = df["Regime de Casamento"].astype(str).apply(string.capwords)


df.replace(to_replace=["nan", "NaN", "NAN", "Nan"], value="", inplace=True)
df.fillna("", inplace=True)

# Exportar
df.to_excel(nome, index=False)
