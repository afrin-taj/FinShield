from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

FILE_PATH = Path("Data/raw/bureau.csv")

chunksize = 50000

for i, chunk in enumerate(pd.read_csv(FILE_PATH, chunksize=chunksize)):
    chunk.to_sql(
        name="bureau",
        con=engine,
        schema="raw",
        if_exists="replace" if i == 0 else "append",
        index=False
    )

    print(f"Loaded chunk {i + 1}")

print("\nBureau data loaded successfully!")