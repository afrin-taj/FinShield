from pathlib import Path
import pandas as pd

DATA_PATH = Path("Data/raw")

csv_files = list(DATA_PATH.glob("*.csv"))

print(f"Total CSV files found: {len(csv_files)}\n")

for file in csv_files:
    file_size_mb = file.stat().st_size / (1024 * 1024)

    sample = pd.read_csv(file, nrows=5)

    print("=" * 70)
    print(f"File: {file.name}")
    print(f"Size: {file_size_mb:.2f} MB")
    print(f"Number of columns: {len(sample.columns)}")
    print(f"Columns: {sample.columns.tolist()}")