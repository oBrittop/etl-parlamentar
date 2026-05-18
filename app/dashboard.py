import pandas as pd
import streamlit as st
import os

DATA_DIR = "dados_limpos/receitas_deputados_federais.csv"
caminho = os.path.join(os.path.abspath(DATA_DIR))
if not os.path.exists(caminho):
    print("ERRO: caminho nao encontrado")

# st.title("DASHBOARDS PARLAMENTAR")
df = pd.read_csv(caminho)
st.write("""
         #DASH BOARD PARLAMENTAR
         
         """)

opcoes_estados = df["SG_UF"].unique()
opcoes_estados = sorted(opcoes_estados)
estado_escolido = st.selectbox("Escolha o estado que vc quer usar", opcoes_estados)
df_filtrado = df[df["SG_UF"] == estado_escolido]


maiores_doadores = df_filtrado.groupby("NM_DOADOR")["VR_RECEITA"].sum().reset_index()
maiores_doadores = maiores_doadores.sort_values(by= "VR_RECEITA", ascending=False).head(20)

st.subheader(f"Top 10 DOadores em {estado_escolido}")
st.bar_chart(maiores_doadores, x="NM_DOADOR", y="VR_RECEITA")







maiores_doadores["VR_RECEITA"] = maiores_doadores["VR_RECEITA"].apply(lambda x: f"R$ {x:,.2f}")
# st.dataframe(maiores_doadores.head(15))

st.dataframe(maiores_doadores, use_container_width=True)