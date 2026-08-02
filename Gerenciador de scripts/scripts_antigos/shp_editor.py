import geopandas as gpd
import pandas as pd
import os

def processar_shapefile_reurb():
    print("--- REURB MANAGER ---")
    
    # 1. Solicita o Shapefile de Entrada
    caminho_shp_entrada = input("Digite o caminho do Shapefile original (.shp): ").strip()
    # Remove aspas se houver (comum ao copiar caminho no Linux/Windows)
    if (caminho_shp_entrada.startswith('"') and caminho_shp_entrada.endswith('"')) or \
       (caminho_shp_entrada.startswith("'") and caminho_shp_entrada.endswith("'")):
        caminho_shp_entrada = caminho_shp_entrada[1:-1]

    if not os.path.exists(caminho_shp_entrada):
        print(f"❌ Erro: Arquivo não encontrado: {caminho_shp_entrada}")
        return

    pasta = os.path.dirname(caminho_shp_entrada)
    nome_arquivo = os.path.basename(caminho_shp_entrada)
    nome_base = os.path.splitext(nome_arquivo)[0]

    # Colunas que formam a IDENTIDADE única do imóvel
    colunas_chave = ['quadra', 'lote'] 

    print(f"\nArquivo selecionado: {nome_arquivo}")
    print(f"Chave de correspondência definida: {colunas_chave}")
    print("1. Gerar Excel para Edição (Exportar)")
    print("2. Importar Excel Editado e Atualizar Shapefile (Importar)")
    modo = input("Escolha o modo (digite 1 ou 2): ")

    # ==============================================================================
    # MODO 1: EXPORTAR PARA EXCEL
    # ==============================================================================
    if modo == '1':
        # Define caminho automático para o Excel (mesma pasta do SHP)
        caminho_excel = os.path.join(pasta, f"{nome_base}_atributos.xlsx")
        
        print(f"\nLendo shapefile...")
        try:
            gdf = gpd.read_file(caminho_shp_entrada, encoding='latin1')
            
            # Verifica se as colunas existem
            for col in colunas_chave:
                if col not in gdf.columns:
                    print(f"❌ Erro: A coluna '{col}' não existe no shapefile.")
                    print(f"Colunas disponíveis: {gdf.columns.tolist()}")
                    return

            # Remove geometria para ir leve para o Excel
            df = gdf.drop(columns='geometry')
            
            # Exporta para Excel
            df.to_excel(caminho_excel, index=False)
            
            print(f"\n✅ Excel gerado: {caminho_excel}")
            print("⚠️  IMPORTANTE: No Excel, NÃO ALTERE os valores das colunas 'quadra' e 'lote'.")
            print("Eles são a chave para devolver os dados para o mapa.")
            
        except Exception as e:
            print(f"Erro ao ler/exportar: {e}")

    # ==============================================================================
    # MODO 2: IMPORTAR E UNIR POR QUADRA + LOTE
    # ==============================================================================
    elif modo == '2':
        # 2. Solicita o Excel de Entrada
        caminho_excel = input("Digite o caminho da planilha Excel para importar (.xlsx): ").strip()
        if (caminho_excel.startswith('"') and caminho_excel.endswith('"')) or \
           (caminho_excel.startswith("'") and caminho_excel.endswith("'")):
            caminho_excel = caminho_excel[1:-1]

        if not os.path.exists(caminho_excel):
            print("❌ Erro: Arquivo Excel não encontrado.")
            return

        # 3. Solicita o Nome do Novo Shapefile
        nome_saida = input("Digite o nome desejado para o novo arquivo Shapefile (ex: final.shp): ").strip()
        if not nome_saida.lower().endswith('.shp'):
            nome_saida += '.shp'
        
        caminho_shp_saida = os.path.join(pasta, nome_saida)

        print("\nProcessando atualização...")
        try:
            # 1. Carrega Shapefile Original (Mantém a geometria)
            gdf_original = gpd.read_file(caminho_shp_entrada, encoding='latin1')
            colunas_para_manter = ['geometry'] + colunas_chave
            gdf_geo = gdf_original[colunas_para_manter].copy()
            
            # 2. Carrega Excel Editado
            df_editado = pd.read_excel(caminho_excel, dtype={col: str for col in colunas_chave})
            
            # 3. Tratamento de Higiene nos Dados
            print("Padronizando chaves (removendo espaços e forçando texto)...")
            for col in colunas_chave:
                gdf_geo[col] = gdf_geo[col].astype(str).str.strip()
                df_editado[col] = df_editado[col].astype(str).str.strip()

            # 4. A Grande União (Merge)
            print(f"Unindo dados usando: {colunas_chave}...")
            gdf_final = gdf_geo.merge(df_editado, on=colunas_chave, how='left')
            
            # 5. Salva o resultado
            gdf_final.to_file(caminho_shp_saida, encoding='latin1')
            
            print(f"\n✅ Shapefile Atualizado salvo em:\n{caminho_shp_saida}")
            
            # Verificação de segurança
            coluna_verificacao = 'rua'
            if coluna_verificacao in gdf_final.columns:
                sem_dados = gdf_final[gdf_final[coluna_verificacao].isna()] 
                if len(sem_dados) > 0:
                    print(f"⚠️  Atenção: {len(sem_dados)} lotes não encontraram correspondência no Excel.")
                    print("Verifique se 'quadra' e 'lote' foram digitados exatamente iguais.")
            else:
                print(f"ℹ️  Verificação pulada: A coluna '{coluna_verificacao}' não existe no arquivo final.")
                print(f"Colunas disponíveis: {gdf_final.columns.tolist()}")
            
        except Exception as e:
            print(f"❌ Erro crítico: {e}")
            
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    processar_shapefile_reurb()