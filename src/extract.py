from pathlib import Path
import pandas as pd

def read_csv_file(file_path: str | Path, sep: str = ",", encoding: str = "utf-8") -> pd.DataFrame:
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    return pd.read_csv(file_path, sep=sep, encoding=encoding, low_memory=False)

    