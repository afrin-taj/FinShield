from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

FILE_PATH = Path("Data/raw/previous_application.csv")

chunksize = 50000

for i, chunk in enumerate(pd.read_csv(FILE_PATH, chunksize=chunksize)):
    chunk.to_sql(
        name="previous_application",
        con=engine,
        schema="raw",
        if_exists="replace" if i == 0 else "append",
        index=False
    )

    print(f"Loaded chunk {i + 1}")

print("\nPrevious application data loaded successfully!")