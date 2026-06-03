from pathlib import Path
import pandas as pd
from zipfile import ZipFile
import requests

def download_file(url: str, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    output_path.write_bytes(response.content)
    return output_path

def extract_zip(zip_path: str | Path, output_dir: str | Path) -> list[Path]:
    zip_path = Path(zip_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with ZipFile(zip_path, "r") as zip_file:
        zip_file.extractall(output_dir)
        extracted_files = [output_dir / name for name in zip_file.namelist()]
        
    return extracted_files


def read_csv_file(file_path: str | Path, sep: str = ",", encoding: str = "utf-8") -> pd.DataFrame:
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    return pd.read_csv(file_path, sep=sep, encoding=encoding, low_memory=False)

    