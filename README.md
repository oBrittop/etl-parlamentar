# ETL Parlamentar - Observatorio da Cota Parlamentar

Projeto de Analise de Dados com Python voltado a transparencia publica.

A aplicacao realiza um processo de ETL sobre dados da **Cota para o Exercicio da Atividade Parlamentar (CEAP)** da Camara dos Deputados, com foco na analise dos gastos parlamentares em 2025.

## Objetivo

O objetivo do projeto e responder a seguinte pergunta:

> Como os deputados federais utilizaram os recursos da Cota Parlamentar em 2025?

A partir dos dados abertos da Camara dos Deputados, o projeto busca identificar padroes de gasto por parlamentar, partido, unidade federativa, categoria de despesa, fornecedor e mes.

## Fonte dos Dados

Os dados sao obtidos a partir dos arquivos publicos da Camara dos Deputados:

- Base CEAP 2025: `https://www.camara.leg.br/cotas/Ano-2025.csv.zip`
- Documentacao dos campos: https://dadosabertos.camara.leg.br/howtouse/2023-12-26-dados-ceap.html

A CEAP e uma verba publica usada para custear despesas relacionadas ao exercicio do mandato parlamentar, como passagens aereas, combustivel, manutencao de escritorio, divulgacao da atividade parlamentar, telefonia, entre outras.

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
|-- app/
|   `-- dashboard.py
|-- data/
|   |-- raw/
|   `-- processed/
|-- reports/
|-- src/
|   |-- __init__.py
|   |-- extract.py
|   |-- transform.py
|   |-- load.py
|   `-- metrics.py
|-- main.py
|-- requirements.txt
`-- README.md
```

## Pipeline ETL

O projeto esta dividido em tres etapas principais.

### 1. Extracao

O arquivo `src/extract.py` baixa automaticamente o arquivo `.zip` da CEAP 2025, extrai o CSV e permite sua leitura com Pandas.

### 2. Transformacao

O arquivo `src/transform.py` realiza o tratamento dos dados:

- remocao de duplicatas;
- tratamento de valores nulos;
- conversao de colunas numericas;
- conversao de datas;
- criacao de novas features;
- classificacao dos gastos por faixa de valor;
- identificacao de registros com documento fiscal disponivel.

### 3. Carga

O arquivo `src/load.py` salva a base tratada em:

```text
data/processed/despesas_ceap_2025.csv
```

## Metricas e Insights

O arquivo `src/metrics.py` sera utilizado para gerar agregacoes analiticas, como:

- gasto total da CEAP;
- quantidade de parlamentares analisados;
- ranking de deputados por gasto;
- gastos por partido;
- gastos por unidade federativa;
- gastos por categoria de despesa;
- principais fornecedores;
- evolucao mensal dos gastos.

## Como Executar o ETL

Crie e ative um ambiente virtual:

```bash
python -m venv venv
```

No Windows:

```bash
venv\Scripts\activate
```

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Execute o pipeline ETL:

```bash
python main.py
```

Apos a execucao, o arquivo tratado sera gerado em:

```text
data/processed/despesas_ceap_2025.csv
```

## Dashboard

O dashboard sera desenvolvido com Streamlit e graficos obrigatoriamente gerados com Matplotlib.

Para executar:

```bash
streamlit run app/dashboard.py
```

## Possiveis Perguntas de Analise

- Quais deputados federais mais utilizaram a Cota Parlamentar em 2025?
- Quais partidos concentraram os maiores gastos?
- Quais estados apresentaram maior volume de despesas?
- Quais categorias de despesa consumiram mais recursos?
- Quais fornecedores receberam os maiores valores?
- Como os gastos evoluiram ao longo dos meses?

## Finalidade Academica

Este projeto foi desenvolvido como trabalho final da disciplina de Analise de Dados com Python.

A implementacao busca atender aos seguintes criterios:

- tratamento de dados com Pandas e NumPy;
- remocao de duplicatas e tratamento de valores ausentes;
- conversao de tipos;
- engenharia de features;
- dashboard funcional em Streamlit;
- visualizacoes com Matplotlib;
- codigo modular e organizado;
- geracao de base para relatorio analitico final.


by Gustavo Brito
trabalho avaliado(nota maxima)