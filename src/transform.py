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
    df =df.copy()
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")
        df[column] = df[column].fillna(0)
    return df

def transform_receitas(df: pd.DataFrame) -> pd.DataFrame:
    df = remove_duplicates(df)
    df = fill_missing_values(df)
    df = convert_numeric_column(df, "VR_RECEITA")

    return df

#script terminal
# python -c "from src.extract import read_csv_file; from src.transform import transform_receitas; df = read_csv_file('dados_limpos/receitas_deputados_federais.csv'); print('Antes:', df.shape, 'duplicadas:', df.duplicated().sum()); df2 = transform_receitas(df); print('Depois:', df2.shape, 'duplicadas:', df2.duplicated().sum()); print(df2.isna().sum())"