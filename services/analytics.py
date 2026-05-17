import pandas as pd
import os
DATA_DIR = "dados_limpos/receitas_deputados_federais.csv"
print(os.path.abspath(DATA_DIR))

caminho = os.path.join(os.path.abspath(DATA_DIR))
print(caminho)


df = pd.read_csv(caminho)
df.info()
print(df.head())
filtro_df = df["SG_UF"] == "DF"
print("-"*120)
print(df[filtro_df])