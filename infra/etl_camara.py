import requests
import pandas as pd
import os
import zipfile

def baixar_extrair_dados_tse():
    url = "https://cdn.tse.jus.br/estatistica/sead/odsele/prestacao_contas/prestacao_de_contas_eleitorais_candidatos_2022.zip"
    pasta_destino = "dados_brutos"
    caminho_zip = os.path.join(pasta_destino, "tse_2022.zip")
    os.makedirs(pasta_destino, exist_ok=True)
    print("Fazendo o download,(Isso pode demorar alguns minutos)")
    resposta = requests.get(url, stream=True)