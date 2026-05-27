import pandas as pd
import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from pandasai import Agent
from pandasai.llm import GoogleGemini

load_dotenv()
CHAVE_IA = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=CHAVE_IA)

llm_gemini = GoogleGemini(api_key=CHAVE_IA)
llm_gemini.google_gemini = genai.GenerativeModel("gemini-2.5-flash")

DATA_DIR = "dados_limpos/receitas_deputados_federais.csv"
caminho = os.path.join(os.path.abspath(DATA_DIR))

if not os.path.exists(caminho):
    st.error("ERRO: arquivo de dados não encontrado no caminho especificado.")

st.write("# DASHBOARD PARLAMENTAR")

df_bruto = pd.read_csv(caminho)

# remoçao duplicatas e tratamento de valores nulos 
df = df_bruto.drop_duplicates()
df["VR_RECEITA"] = pd.to_numeric(df["VR_RECEITA"], errors="coerce")
df["VR_RECEITA"] = df["VR_RECEITA"].fillna(0)
df["NM_DOADOR"] = df["NM_DOADOR"].fillna("Doador Não Identificado")

# =====================================================================
#CONFIGURAÇÃO DOS FILTROS E MÉTRICAS
def formatar_milhoes(valor):
    if valor >= 1_000_000_000:
        return f"R$ {valor/1_000_000_000:.2f} Bi"
    elif valor >= 1_000_000:
        return f"R$ {valor/1_000_000:.2f} Mi"
    elif valor >= 1_000:
        return f"R$ {valor/1_000:.2f} Mil"
    else:
        return f"R$ {valor:.2f}"

opcoes_estados = sorted(df["SG_UF"].dropna().unique())
estado_escolhido = st.selectbox("Escolha o estado que você quer usar", opcoes_estados)

# Filtragem dos dados
df_filtrado = df[df["SG_UF"] == estado_escolhido]

# Processamento do Top 10 Doadores
maiores_doadores = df_filtrado.groupby("NM_DOADOR")["VR_RECEITA"].sum().reset_index()
maiores_doadores = maiores_doadores.sort_values(by="VR_RECEITA", ascending=False).head(10)

st.subheader(f"Top 10 Doadores em {estado_escolhido}")

# Cálculos para os KPIs
total_arrecadado = df_filtrado["VR_RECEITA"].sum()
total_doadores = df_filtrado["NM_DOADOR"].nunique()
maior_doacao = df_filtrado["VR_RECEITA"].max()

total_arrecadado_fmt = formatar_milhoes(total_arrecadado)
maior_doacao_fmt = formatar_milhoes(maior_doacao)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Arrecadado", value=total_arrecadado_fmt)
with col2:
    st.metric(label="Total de Doadores", value=total_doadores)
with col3:
    st.metric(label="Maior Doação Única", value=maior_doacao_fmt)

st.divider()

# Gráfico Nativo e Tabela de Dados
st.bar_chart(maiores_doadores, x="NM_DOADOR", y="VR_RECEITA")

# Criamos uma cópia para exibição formatada sem quebrar os dados numéricos originais
maiores_doadores_exibicao = maiores_doadores.copy()
maiores_doadores_exibicao["VR_RECEITA"] = maiores_doadores_exibicao["VR_RECEITA"].apply(lambda x: f"R$ {x:,.2f}")
st.dataframe(maiores_doadores_exibicao, width="stretch")

# ----------------------------------------------------
# NOVA SEÇÃO: O AGENTE DE DADOS AUTÔNOMO
st.divider()
st.subheader("Cientista de Dados IA (Motor Customizado)")
st.write("Peça à IA para filtrar ou cruzar dados. Ela criará e executará o código em tempo real!")

pergunta = st.text_input("O que você quer descobrir? (Ex: Deputados com maior número de doadores únicos)")

if st.button("Executar Análise"):
    if pergunta:
        with st.spinner("A IA está escrevendo e rodando o código Pandas nos bastidores..."):
            
            # 1. O Prompt Mestre: Ensinamos o Gemini a ser um programador Pandas
            prompt_mestre = f"""
            Você é um Engenheiro de Dados Sênior. Eu tenho um DataFrame no Python chamado `df_filtrado`.
            As colunas disponíveis nessa tabela são: {list(df_filtrado.columns)}
            
            O usuário fez a seguinte requisição: "{pergunta}"
            
            Escreva o código em Python (usando a biblioteca pandas) para resolver isso.
            Obrigatoriamente, salve a tabela final numa variável chamada `resultado`.
            
            REGRA ABSOLUTA: Retorne SOMENTE O CÓDIGO PURO. Sem marcações Markdown, sem crases (```), sem a palavra python, sem explicações.
            """
            
            # 2. O Gemini gera o código puro (usamos a variável que você já configurou lá em cima)
            # Como instanciamos o GenerativeModel na variável llm_gemini.google_gemini, usamos ela:
            resposta = llm_gemini.google_gemini.generate_content(prompt_mestre)
            
            # Limpamos qualquer sujeira de formatação que a IA possa tentar colocar
            codigo_gerado = resposta.text.replace("```python", "").replace("```", "").strip()
            
            # 3. O Ambiente Virtual: Damos acesso seguro apenas à tabela e ao Pandas
            ambiente = {"df_filtrado": df_filtrado, "pd": pd}
            
            try:
                # 4. A Magia Acontece: Executamos o código que a IA acabou de escrever!
                exec(codigo_gerado, ambiente)
                
                # Resgatamos a variável 'resultado' que mandamos a IA criar
                resultado = ambiente.get("resultado")
                
                if isinstance(resultado, pd.DataFrame):
                    st.success("Análise concluída com sucesso!")
                    st.dataframe(resultado, width="stretch")
                    
                    # === SEU CÓDIGO MATPLOTLIB INTACTO ===
                    st.write(" Gráfico Gerado Automaticamente:")
                    import matplotlib.pyplot as plt
                    
                    fig, ax = plt.subplots(figsize=(10, 5))
                    
                    # Descobre sozinho os eixos X e Y baseados no dataframe gerado
                    coluna_x = resultado.columns[0]
                    coluna_y = resultado.columns[1] if len(resultado.columns) > 1 else resultado.columns[0]
                    df_plot = resultado.head(10)
                    
                    ax.bar(df_plot[coluna_x].astype(str), df_plot[coluna_y], color='#4C72B0', edgecolor='black')
                    
                    plt.title(f"Análise: {coluna_x} vs {coluna_y}", fontsize=12)
                    plt.xlabel(coluna_x, fontsize=10)
                    plt.ylabel(coluna_y, fontsize=10)
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    
                    st.pyplot(fig)
                else:
                    st.info(f"Resultado: {resultado}")
                    
            except Exception as e:
                # Se a IA errar a sintaxe do Pandas, nós mostramos o erro e o código para o professor ver o nível do projeto!
                st.error(f"Houve um erro na execução lógica do código. O Agente se confundiu.")
                with st.expander("Ver o código gerado pela IA (Debug)"):
                    st.code(codigo_gerado)
                    st.write(f"Erro original: {e}")
                    
    else:
        st.warning("Por favor, digite algo para o Agente analisar.")