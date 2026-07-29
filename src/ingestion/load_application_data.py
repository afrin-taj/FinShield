import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

FILE_PATH = Path("Data/raw/application_train.csv")
CHUNK_SIZE = 50000

print("Starting data ingestion...")

for chunk_number, chunk in enumerate(
    pd.read_csv(FILE_PATH, chunksize=CHUNK_SIZE),
    start=1
):
    if_exists_action = "replace" if chunk_number == 1 else "append"

    chunk.to_sql(
        name="application_train",
        con=engine,
        schema="raw",
        if_exists=if_exists_action,
        index=False,
        method="multi",
        chunksize=1000
    )

    print(
        f"Chunk {chunk_number} loaded successfully "
        f"({len(chunk):,} rows)"
    )

print("\nData ingestion completed!")

with engine.connect() as connection:
    row_count = connection.execute(
        text("SELECT COUNT(*) FROM raw.application_train")
    ).scalar()

print(f"Total rows in PostgreSQL: {row_count:,}")