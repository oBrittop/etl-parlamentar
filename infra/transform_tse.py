import pandas as pd
import os

def limpar_dados_receitas():
    pasta_origem = "dados_brutos"
    pasta_destino = "dados_limpos"
    
    os.makedirs(pasta_destino, exist_ok=True)
    lista_df = []
    print("Aguarde um instante...\nEstamos trabalhando nisso....")
    
    for nome_arqivo in os.listdir(pasta_origem):
        if nome_arqivo.startswith("receitas_candidatos_2022") and nome_arqivo.endswith(".csv"):
            caminho = os.path.join(pasta_origem, nome_arqivo)
            df_estado = pd.read_csv(caminho, sep=";", encoding="latin-1")
            df_federais = df_estado[df_estado["DS_CARGO"].str.contains("DEPUTADO FEDERAL", case=False, na=False)]
            
            if not df_federais.empty:
                colunas_importantes = [
                "SG_UF", "NM_CANDIDATO", "NR_CPF_CANDIDATO", "NM_DOADOR", "VR_RECEITA", "DS_ORIGEM_RECEITA"
                ]
                df_limpo = df_federais[colunas_importantes]
                lista_df.append(df_limpo)
            
    if lista_df:
        df_brasil = pd.concat(lista_df, ignore_index=True)
        df_brasil["VR_RECEITA"] = df_brasil["VR_RECEITA"].str.replace(",",".").astype(float)
        caminho_final = os.path.join(pasta_destino, "receitas_deputados_federais.csv")
        df_brasil.to_csv(caminho_final, index=False, sep=",")
        return df_brasil
    else:
        print("Nenhum dado de deputado federal fpo encontrado") 
        print(lista_df)
        






if __name__=="__main__":
    limpar_dados_receitas()