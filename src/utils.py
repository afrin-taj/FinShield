"""
Utility Functions
-----------------
Reusable helper functions for the FinShield project.
"""

from pathlib import Path
from time import perf_counter
import time
from datetime import datetime
import pandas as pd


# ==========================
# Logger
# ==========================
def log(message):
    """
    Prints formatted log messages.
    """

    print(f"[INFO] {message}")


# ==========================
# Save CSV
# ==========================
def save_csv(df, file_path):
    """
    Saves a DataFrame as CSV.
    Creates parent folders if they don't exist.
    """

    file_path = Path(file_path)

    file_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(file_path, index=False)

    log(f"CSV saved -> {file_path}")


# ==========================
# Validate Required Columns
# ==========================
def validate_columns(df, required_columns):
    """
    Ensures all required columns exist.
    """

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )


# ==========================
# Display DataFrame Info
# ==========================
def dataframe_summary(df: pd.DataFrame) -> None:
    """
    Display basic dataframe information.
    """

    memory = df.memory_usage(deep=True).sum() / (1024 ** 2)

    log(f"Rows      : {len(df):,}")
    log(f"Columns   : {df.shape[1]}")
    log(f"Memory    : {memory:.2f} MB")

# ==========================
# Timer
# ==========================
def start_timer():
    """
    Starts execution timer.
    """

    return perf_counter()


def end_timer(start_time):
    """
    Displays execution time.
    """

    elapsed = perf_counter() - start_time

    log(f"Completed in {elapsed:.2f} seconds.")

# ==========================
# Timer Utilities
# ==========================

def start_timer():
    """
    Start execution timer.
    """
    start_time = time.time()

    log("=" * 60)
    log("Feature Engineering Pipeline : Bureau")
    log("=" * 60)
    log(f"Start Time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return start_time


def end_timer(start_time):
    """
    End execution timer.
    """
    elapsed = time.time() - start_time

    log("=" * 60)
    log(f"Execution Time : {elapsed:.2f} seconds")
    log("Pipeline completed successfully.")
    log("=" * 60)


def separator():
    log("-" * 60)