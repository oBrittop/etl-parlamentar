from src.extract import download_ceap_csv, read_csv_file
from src.load import save_csv_file
from src.transform import transform_despesas


YEAR = 2025
OUTPUT_FILE = "data/processed/despesas_ceap_2025.csv"


def main() -> None:
    raw_file = download_ceap_csv(YEAR)
    df_raw = read_csv_file(raw_file)

    print("Dados carregados:")
    print(f"Arquivo: {raw_file}")
    print(f"Linhas: {df_raw.shape[0]}")
    print(f"Colunas: {df_raw.shape[1]}")
    print(f"Duplicatas: {df_raw.duplicated().sum()}")

    df_clean = transform_despesas(df_raw)

    print("\nDados tratados:")
    print(f"Linhas: {df_clean.shape[0]}")
    print(f"Colunas: {df_clean.shape[1]}")
    print(f"Duplicatas: {df_clean.duplicated().sum()}")

    save_csv_file(df_clean, OUTPUT_FILE)

    print(f"\nArquivo salvo em: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()