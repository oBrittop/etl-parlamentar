import pandas as pd
import os

def limpar_dados_receitas():
    pasta_origem = "dados_brutos"
    pasta_destino = "dados_limpos"
    
    os.makedirs(pasta_destino, exist_ok=True)
    lista_df = []
    print("Aguarde um instante...\nEstamos trabalhando nisso....")
    
    for nome_arqivo in os.listdir(pasta_origem):
        if nome_arqivo.startswith("receitas_canditados_2022") and nome_arqivo.endswith(".csv"):
            caminho = os.path.join(pasta_origem, nome_arqivo)
            df_estado = pd.read_csv(caminho, sep=";", encoding="latin-1")
            df_federais = df_estado[df_estado["DS_CARGO"] == "DEPUTADO FEDERAL"]
            
        if not df_federais.empty:
            colunas_importantes = [
                "SG_UF", "MN_CANDITADO", "NR_CPF_CANDITADO", "NM_DOADOR", "VR_RECEITA", "DS_ORIGEM_RECEITA"
            ]
            df_limpo = df_federais[colunas_importantes]
            lista_df.append(df_limpo)
            
