from src.extract import read_csv_file
from src.load import save_csv_file
from src.transform import transform_receitas


RAW_FILE = "dados_limpos/receitas_deputados_federais.csv"
OUTPUT_FILE = "dados_limpos/receitas_deputados_federais_tratadas.csv"


def main() -> None:
    df_raw = read_csv_file(RAW_FILE)

    print("Dados carregados:")
    print(f"Linhas: {df_raw.shape[0]}")
    print(f"Colunas: {df_raw.shape[1]}")
    print(f"Duplicatas: {df_raw.duplicated().sum()}")

    df_clean = transform_receitas(df_raw)

    print("\nDados tratados:")
    print(f"Linhas: {df_clean.shape[0]}")
    print(f"Colunas: {df_clean.shape[1]}")
    print(f"Duplicatas: {df_clean.duplicated().sum()}")

    save_csv_file(df_clean, OUTPUT_FILE)

    print(f"\nArquivo salvo em: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()