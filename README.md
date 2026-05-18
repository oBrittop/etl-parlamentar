# etl-parlamentar
ETL feito em arquitetura 3 camadas - Python-MySQL-gemini-1.5-flash
## Arquitetura do Sistema
O projeto foi estruturado utilizando uma Arquitetura em 3 Camadas para garantir escalabilidade e separação de responsabilidades (Clean Code):

1. **Camada de Dados (Infraestrutura/ETL):** - Scripts automatizados em **Python** (`requests`, `pandas`) que consomem a API de Dados Abertos da Câmara dos Deputados, limpam os JSONs e realizam a carga (Load) em um banco de dados relacional **MySQL**.
2. **Camada de Serviço (Inteligência Artificial):**
   - Implementação de um Agente IA utilizando a **API do Google Gemini**. O agente atua com a técnica de *Text-to-SQL*, traduzindo perguntas em linguagem natural feitas pelo usuário em consultas SQL otimizadas para interagir com o banco de dados de forma segura.
3. **Camada de Apresentação (Frontend):**
   - Interface web interativa desenvolvida com **Streamlit** e visualização de dados suportada pela biblioteca **Plotly**, permitindo filtros dinâmicos e chat em tempo real com o Agente de IA.

libs++ etl-parlamentar> pip install pandas requests sqlalchemy mysql-connector-python streamlit plotly python-dotenv

```bash
# 1. Instalação das bibliotecas base e da IA do Google
pip install pandas requests sqlalchemy mysql-connector-python streamlit plotly python-dotenv google-generativeai pyyaml

# 2. Instalação isolada do PandasAI (para não quebrar o Pandas moderno)
pip install pandasai --no-deps

# 3. Instalação das dependências secundárias exigidas pelo PandasAI para desenhar os gráficos
pip install "matplotlib>=3.7.1,<4.0.0" "sqlglot[rs]>=25.0.3,<26.0.0" "faker>=19.12.0,<20.0.0" "openai<2" "pillow>=10.1.0,<11.0.0"