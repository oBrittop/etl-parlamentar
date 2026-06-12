import pandas as pd 

def total_expenses(df: pd.DataFrame) -> float:
    expenses_total = df["vlrLiquido"].sum()
    return expenses_total

#A análise considera parlamentares com despesas registradas na CEAP em 2025, podendo incluir titulares e suplentes que exerceram mandato ao longo do período.
def deputados_unique(df: pd.DataFrame) -> int:
    df = df.copy()
    number_deputados = df["ideCadastro"].nunique()
    
    return number_deputados

def values_category(df: pd.DataFrame) -> pd.DataFrame:
    return(
        df.groupby("txtDescricao", as_index=False)["vlrLiquido"]
        .sum()
        .sort_values("vlrLiquido", ascending=False)
    )
def ranking_expense_deputado(df: pd.DataFrame, limit=10) -> pd.DataFrame:
    return(
        df.groupby(["txNomeParlamentar", "sgPartido", "sgUF"], as_index=False)["vlrLiquido"]
        .sum()
        .sort_values("vlrLiquido", ascending=False)
        .head(limit)
    )
    
def expense_partido(df: pd.DataFrame) -> pd.DataFrame:
    return(
        df.groupby("sgPartido", as_index=False)["vlrLiquido"].sum().sort_values("vlrLiquido",ascending=False)
    )

def expense_uf(df: pd.DataFrame) -> pd.DataFrame:
    return(
        df.groupby("sgUF", as_index=False)["vlrLiquido"].sum().sort_values("vlrLiquido",ascending=False)
    )
    
def ranking_fornecedores(df: pd.DataFrame, limit: int=10) -> pd.DataFrame:
    return(
        df.groupby(["txtFornecedor", "txtCNPJCPF"], as_index=False)["vlrLiquido"]
        .sum()
        .sort_values("vlrLiquido",ascending=False)
        .head(limit)
    )
def values_data(df: pd.DataFrame) -> pd.DataFrame:
    return(
        df.groupby(["numAno", "numMes"], as_index=False,)["vlrLiquido"]
        .sum()
        .sort_values(["numAno","numMes"])
    )









#script
#python -c "import pandas as pd; from src.metrics import total_expenses, deputados_unique, values_category, ranking_expense_deputado, expense_partido, expense_uf, ranking_fornecedores, values_data; pd.set_option('display.float_format', 'R$ {:,.2f}'.format); df = pd.read_csv('data/processed/despesas_ceap_2025.csv'); print('Gasto total:'); print(total_expenses(df)); print('\nDeputados unicos:'); print(deputados_unique(df)); print('\nGastos por categoria:'); print(values_category(df).head(10)); print('\nRanking de deputados:'); print(ranking_expense_deputado(df)); print('\nGastos por partido:'); print(expense_partido(df).head(10)); print('\nGastos por UF:'); print(expense_uf(df).head(10)); print('\nRanking de fornecedores:'); print(ranking_fornecedores(df)); print('\nEvolucao mensal:'); print(values_data(df))"