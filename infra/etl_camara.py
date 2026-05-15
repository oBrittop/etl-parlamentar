import requests
import os
import zipfile

def baixar_extrair_dados_tse():
    url = "https://cdn.tse.jus.br/estatistica/sead/odsele/prestacao_contas/prestacao_de_contas_eleitorais_candidatos_2022.zip"
    pasta_destino = "dados_brutos"
    caminho_zip = os.path.join(pasta_destino, "tse_2022.zip")
    os.makedirs(pasta_destino, exist_ok=True)
    print("Fazendo o download,(Isso pode demorar alguns minutos)")
    resposta = requests.get(url, stream=True)
    
    if resposta.status_code == 200:
        with open(caminho_zip, "wb") as arquivo:
            for bloco in resposta.iter_content(chunk_size=8192):
                arquivo.write(bloco)
        print("Download concluido!")
        with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
            zip_ref.extractall(pasta_destino)
        print(f"Arquvivos . csv descompactados na pasta'{pasta_destino}'.")
        os.remove(caminho_zip)
    else:
        print(f"Erro ao acessar o TSE. Codigo de erro : {resposta.status_code}")
        
        
if __name__ == "__main__":
    baixar_extrair_dados_tse()