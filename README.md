# ETL Parlamentar - Observatório da Cota Parlamentar

Projeto de Análise de Dados com Python voltado à transparência pública.  
A aplicação realiza um processo de ETL sobre dados da **Cota para o Exercício da Atividade Parlamentar (CEAP)** da Câmara dos Deputados, com foco na análise dos gastos parlamentares em 2025.

## Objetivo

O objetivo do projeto é responder à seguinte pergunta:

> Como os deputados federais utilizaram os recursos da Cota Parlamentar em 2025?

A partir dos dados abertos da Câmara dos Deputados, o projeto busca identificar padrões de gasto por parlamentar, partido, unidade federativa, categoria de despesa, fornecedor e mês.

## Fonte dos Dados

Os dados são obtidos a partir dos arquivos públicos da Câmara dos Deputados:

- Base CEAP 2025: `https://www.camara.leg.br/cotas/Ano-2025.csv.zip`
- Documentação dos campos: https://dadosabertos.camara.leg.br/howtouse/2023-12-26-dados-ceap.html

A CEAP é uma verba pública usada para custear despesas relacionadas ao exercício do mandato parlamentar, como passagens aéreas, combustível, manutenção de escritório, divulgação da atividade parlamentar, telefonia, entre outras.

## Tecnologias Utilizadas

- Python
- Pandas
- NumPy
- Requests
- Matplotlib
- Streamlit

## Estrutura do Projeto

```text
etl-parlamentar/
├── app/
│   └── dashboard.py
├── data/
│   ├── raw/
│   └── processed/
├── reports/
├── src/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── metrics.py
├── main.py
├── requirements.txt
└── README.md