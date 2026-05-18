import pandas as pd
import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
CHAVE_IA = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=CHAVE_IA)
modelo_ia = genai.GenerativeModel("gemini-2.5-flash")

DATA_DIR = "dados_limpos/receitas_deputados_federais.csv"
caminho = os.path.join(os.path.abspath(DATA_DIR))
if not os.path.exists(caminho):
    print("ERRO: caminho nao encontrado")
    st.error("ERRO: caminho nao encontrado")

# st.title("DASHBOARDS PARLAMENTAR")
df = pd.read_csv(caminho)
st.write("""
         # DASH BOARD PARLAMENTAR
         
         """)
def formatar_milhoes(valor):
    if valor >= 1_000_000_000:
        return f"R$ {valor/1_000_000_000:.2f} Bi"
    elif valor >= 1_000_000:
        return f"R$ {valor/1_000_000:.2f} Mi"
    elif valor >= 1_000:
        return f"R$ {valor/1_000:.2f} Mil"
    else:
        return f"R$ {valor:.2f}"

opcoes_estados = df["SG_UF"].unique()
opcoes_estados = sorted(opcoes_estados)
estado_escolhido = st.selectbox("Escolha o estado que vc quer usar", opcoes_estados)
df_filtrado = df[df["SG_UF"] == estado_escolhido]


maiores_doadores = df_filtrado.groupby("NM_DOADOR")["VR_RECEITA"].sum().reset_index()
maiores_doadores = maiores_doadores.sort_values(by= "VR_RECEITA", ascending=False).head(10)

st.subheader(f"Top 10 DOadores em {estado_escolhido}")

total_arrecadado = df_filtrado["VR_RECEITA"].sum()
total_doadores = df_filtrado["NM_DOADOR"].nunique()
maior_doacao = df_filtrado["VR_RECEITA"].max()

total_arrecadado_fmt = formatar_milhoes(total_arrecadado)
maior_doacao_fmt = formatar_milhoes(maior_doacao)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Arrecadado", value=total_arrecadado_fmt)
with col2:
    st.metric(label="Total de Doadores",value=total_doadores)
with col3:
    st.metric(label="Maior Doação Única", value=maior_doacao_fmt)
st.divider()
st.bar_chart(maiores_doadores, x="NM_DOADOR", y="VR_RECEITA")


maiores_doadores["VR_RECEITA"] = maiores_doadores["VR_RECEITA"].apply(lambda x: f"R$ {x:,.2f}")
# st.dataframe(maiores_doadores.head(15))

st.dataframe(maiores_doadores, width="stretch")



# -------------CHAT COM GEMINI FLASH AI-------------
st.divider()
st.subheader("Analista de Dados IA")
st.write("Pergunte algo sobre os Top 10 doadores deste estado e a IA vai analisar para você.")
pergunta = st.text_input("O que voce quer saber?")


if st.button("Perguntar a IA"):
    if pergunta:
        with st.spinner("O Gemini esta analisando os dados..."):
            
            tabela_em_texto = maiores_doadores.to_string()
            
            prompt_mestre = f"""
            Você é um assistente de dados focado em analisar doações políticas.
            O usuário está analisando atualmente os dados do estado: {estado_escolhido}.
            
            Aqui estão os dados dos maiores doadores desse estado específico:
            {tabela_em_texto}
            
            Com base EXCLUSIVAMENTE nos dados acima, responda à seguinte pergunta do usuário de forma clara, direta e educada.
            Se a pergunta for sobre o estado atual ({estado_escolhido}), use os dados para responder.
            
            Pergunta do usuário: {pergunta}
            """
            resposta = modelo_ia.generate_content(prompt_mestre)
            st.info(resposta.text)
    else:
        print("Por favor, digite uma pergunta antes de clicar no botão.")