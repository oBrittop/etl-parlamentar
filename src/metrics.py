import pandas as pd 

def total_expenses(df: pd.DataFrame) -> float:
    df = df.copy()
    expenses_total = df["vlrLiquido"].sum()
    return expenses_total

#A análise considera parlamentares com despesas registradas na CEAP em 2025, podendo incluir titulares e suplentes que exerceram mandato ao longo do período.
def deputados_unique(df: pd.DataFrame) -> int:
    df = df.copy()
    number_deputados = df["cpf"].nunique()
    
    return number_deputados

def values_category(df: pd.DataFrame) -> pd.DataFrame:
    valor_categoria = df.groupby("txtDescricao")["vlrLiquido"].sum()
    return valor_categoria

def ranking_expense_deputado(df: pd.DataFrame, limit=10) -> pd.DataFrame:
    return(
        df.groupby(["txNomeParlamentar", "sgPartido", "sgUF"], as_index=False)["vlrLiquido"]
        .sum()
        .sort_values("vlrLiquido", ascending=False)
        .head(limit)
    )
    
def expense_partido(df: pd.DataFrame) -> pd.DataFrame:
    return(
        df.groupby("sgPartido")["vlrLiquido"].sum().sort_values(ascending=False)
    )

def expense_uf(df: pd.DataFrame) -> pd.DataFrame:
    return(
        df.groupby("sgUF")["vlrLiquido"].sum().sort_values(ascending=False)
    )









#script
#python -c "import pandas as pd; from src.metrics import SUA_FUNCAO; df = pd.read_csv('data/processed/despesas_ceap_2025.csv'); print(SUA_FUNCAO(df))"