import numpy as np
import pandas as pd

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates()


def fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    text_columns = df.select_dtypes(include="object").columns
    numeric_columns = df.select_dtypes(include=np.number).columns
    
    df[text_columns] = df[text_columns].fillna("Não Informado")
    df[numeric_columns] = df[numeric_columns].fillna(0)
    
    return df

def convert_numeric_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    df = df.copy()
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")
        df[column] = df[column].fillna(0)
    return df

def convert_date_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    df = df.copy()
    if column in df.columns:
        df[column] = pd.to_datetime(df[column],errors="coerce")
    return df     


def create_expense_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["valor_liquido_abs"] = df["vlrLiquido"].abs()
    
    df["faixa_valor"] = pd.cut(
        df["valor_liquido_abs"], 
        bins=[-1, 100, 500, 1000, 5000, np.inf],
        labels=["Ate 100", "101 a 500", "501 a 1.000", "1.001 a 5.000", "Acima de 5.000"],
    
    )
    df["tem_documento"] = np.where(df["urlDocumento"]!= "Não informado", "Sim", "Não")
    
    df["mes_nome"] = pd.to_datetime(df["numMes"], format="%m", errors="coerce").dt.month_name(locale="Portuguese_Brazil")
    return df


def filter_parliamentarians(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "ideCadastro" in df.columns:
        df = df[df["ideCadastro"]>0]
    return df

def transform_despesas(df: pd.DataFrame) -> pd.DataFrame:
    df = remove_duplicates(df)
    df = fill_missing_values(df)
    numeric_columns = [
        "vlrDocumento",
        "vlrGlosa",
        "vlrLiquido",
        "numMes",
        "numAno",
    ]
    for column in numeric_columns:
        df = convert_numeric_column(df, column)
    
    df = filter_parliamentarians(df)
    df = convert_date_column(df, "datEmissao")
    df = create_expense_features(df)
    
    return df


#python -c "from src.extract import read_csv_file; from src.transform import transform_despesas; df = read_csv_file('data/raw/Ano-2025.csv'); print('Antes:', df.shape, 'duplicadas:', df.duplicated().sum()); df2 = transform_despesas(df); print('Depois:', df2.shape, 'duplicadas:', df2.duplicated().sum()); print(df2[['txNomeParlamentar','sgUF','sgPartido','txtDescricao','vlrLiquido','valor_liquido_abs','faixa_valor','tem_documento']].head())"

