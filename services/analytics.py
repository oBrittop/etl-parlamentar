import pandas as pd
import os
DATA_DIR = "dados_limpos/receitas_deputados_federais.csv"
print(os.path.abspath(DATA_DIR))

caminho = os.path.join(os.path.abspath(DATA_DIR))
if not os.path.exists(caminho):
    print("Rode primeiro o ETL")
print(caminho)
df = pd.read_csv(caminho)
df.info()
print(df.head())
filtro_df = df["SG_UF"] == "DF"
print("-"*120)
print(df[filtro_df])
maiores_doadores = df.groupby("NM_DOADOR")["VR_RECEITA"].sum()
print("-"*120)
print("15 Maiores doadores:")
print(maiores_doadores.sort_values(ascending=False).apply(lambda x: f"R$ {x:,.2f}").head(15))
estado_maior_arecado = df.groupby("SG_UF")["VR_RECEITA"].sum()
print("-"*120)
print("Estado que mais arrecadou: ")
print(estado_maior_arecado.sort_values(ascending=False).apply(lambda x: f"R$ {x:,.2f}").head(1)) 