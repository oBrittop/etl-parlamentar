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


def calculate_weekend_expenses(df: pd.DataFrame) -> dict:
    if "datEmissao" not in df.columns:
        return {"weekend_val": 0.0, "weekday_val": 0.0, "percentage_weekend": 0.0}
    
    df_date = df.copy()
    df_date["datEmissao"] = pd.to_datetime(df_date["datEmissao"], errors="coerce")
    df_date = df_date.dropna(subset=["datEmissao"])
    
    # 5 = Sábado, 6 = Domingo
    df_date["dia_semana"] = df_date["datEmissao"].dt.dayofweek
    df_date["is_weekend"] = df_date["dia_semana"].isin([5, 6])
    
    summary = df_date.groupby("is_weekend")["vlrLiquido"].sum()
    
    weekend_val = summary.get(True, 0.0)
    weekday_val = summary.get(False, 0.0)
    total = weekend_val + weekday_val
    
    percentage_weekend = (weekend_val / total * 100) if total > 0 else 0.0
    
    return {
        "weekend_val": weekend_val,
        "weekday_val": weekday_val,
        "percentage_weekend": percentage_weekend
    }


def calculate_benford_law(df: pd.DataFrame) -> pd.DataFrame:
    df_benford = df.copy()

    df_benford = df_benford[df_benford["vlrLiquido"] > 0]
    
    df_benford["primeiro_digito"] = (
        df_benford["vlrLiquido"]
        .astype(str)
        .str.replace(r"[^1-9]", "", regex=True) # Remove tudo que não for de 1 a 9 no início
        .str.slice(0, 1)
    )
    
    df_benford = df_benford[df_benford["primeiro_digito"] != ""]
    df_benford["primeiro_digito"] = df_benford["primeiro_digito"].astype(int)
    
    total_registros = len(df_benford)
    if total_registros == 0:
        return pd.DataFrame()
        
    counts = df_benford["primeiro_digito"].value_counts().reindex(range(1, 10), fill_value=0)
    real_percentages = (counts / total_registros) * 100
    
    benford_theoretical = {
        1: 30.1, 2: 17.6, 3: 12.5, 4: 9.7, 
        5: 7.9,  6: 6.7,  7: 5.8,  8: 5.1, 9: 4.6
    }
    
    result_df = pd.DataFrame({
        "Digito": list(range(1, 10)),
        "Frequencia_Real": real_percentages.values,
        "Frequencia_Teorica": [benford_theoretical[d] for d in range(1, 10)]
    })
    
    return result_df



#script
#python -c "import pandas as pd; from src.metrics import total_expenses, deputados_unique, values_category, ranking_expense_deputado, expense_partido, expense_uf, ranking_fornecedores, values_data; pd.set_option('display.float_format', 'R$ {:,.2f}'.format); df = pd.read_csv('data/processed/despesas_ceap_2025.csv'); print('Gasto total:'); print(total_expenses(df)); print('\nDeputados unicos:'); print(deputados_unique(df)); print('\nGastos por categoria:'); print(values_category(df).head(10)); print('\nRanking de deputados:'); print(ranking_expense_deputado(df)); print('\nGastos por partido:'); print(expense_partido(df).head(10)); print('\nGastos por UF:'); print(expense_uf(df).head(10)); print('\nRanking de fornecedores:'); print(ranking_fornecedores(df)); print('\nEvolucao mensal:'); print(values_data(df))" 