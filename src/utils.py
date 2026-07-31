"""
Utility Functions
-----------------
Reusable helper functions for the FinShield project.
"""

from pathlib import Path
from datetime import datetime
import pandas as pd

from src.config import FINAL_DATA_DIR
from src.database import write_table
from src.feature_configs.bureau_balance_config import OUTPUT_FILE


# ============================================================
# Logger
# ============================================================

def log(message: str) -> None:
    """
    Print formatted log messages.
    """
    print(f"[INFO] {message}")


# ============================================================
# Save CSV
# ============================================================

def save_csv(df: pd.DataFrame, file_path) -> None:
    """
    Save DataFrame as CSV.
    Creates parent folders if they do not exist.
    """
    file_path = Path(file_path)

    file_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(file_path, index=False)

    log(f"CSV saved -> {file_path}")


# ============================================================
# Validate Required Columns
# ============================================================

def validate_columns(df: pd.DataFrame, required_columns: list) -> None:
    """
    Ensure all required columns exist.
    """
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")


# ============================================================
# DataFrame Summary
# ============================================================

def dataframe_summary(df: pd.DataFrame) -> None:
    """
    Display basic dataframe information.
    """
    memory = df.memory_usage(deep=True).sum() / (1024 ** 2)

    log(f"Rows      : {len(df):,}")
    log(f"Columns   : {df.shape[1]}")
    log(f"Memory    : {memory:.2f} MB")


# ============================================================
# Memory Optimization
# ============================================================

def optimize_memory(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reduce dataframe memory usage by downcasting numeric columns.
    """

    for column in df.select_dtypes(include=["int"]).columns:
        df[column] = pd.to_numeric(df[column], downcast="integer")

    for column in df.select_dtypes(include=["float"]).columns:
        df[column] = pd.to_numeric(df[column], downcast="float")

    return df


# ============================================================
# Timer
# ============================================================

def start_timer(title: str):
    """
    Start execution timer.
    """

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    start = datetime.now()

    print(f"Start Time : {start.strftime('%Y-%m-%d %H:%M:%S')}\n")

    return start


def end_timer(start):
    """
    End execution timer.
    """

    end = datetime.now()

    print(f"\nEnd Time : {end.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Execution Time : {end - start}")
    print("\nPipeline completed successfully.")
    print("=" * 60)


# ============================================================
# Separator
# ============================================================

def separator():
    """
    Print a separator line.
    """

    log("-" * 60)