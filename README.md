# etl-parlamentar
ETL feito em arquitetura 3 camadas - Python-MySQL-gemini-1.5-flash
## Arquitetura do Sistema
O projeto foi estruturado utilizando uma Arquitetura em 3 Camadas para garantir escalabilidade e separação de responsabilidades (Clean Code):

1. **Camada de Dados (Infraestrutura/ETL):** - Scripts automatizados em **Python** (`requests`, `pandas`) que consomem a API de Dados Abertos da Câmara dos Deputados, limpam os JSONs e realizam a carga (Load) em um banco de dados relacional **MySQL**.
2. **Camada de Serviço (Inteligência Artificial):**
   - Implementação de um Agente IA utilizando a **API do Google Gemini**. O agente atua com a técnica de *Text-to-SQL*, traduzindo perguntas em linguagem natural feitas pelo usuário em consultas SQL otimizadas para interagir com o banco de dados de forma segura.
3. **Camada de Apresentação (Frontend):**
   - Interface web interativa desenvolvida com **Streamlit** e visualização de dados suportada pela biblioteca **Plotly**, permitindo filtros dinâmicos e chat em tempo real com o Agente de IA.
