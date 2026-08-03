import pandas as pd

from src.database import read_table
from src.utils import (
    log,
    dataframe_summary,
    start_timer,
    end_timer,
)

def load_data() -> pd.DataFrame:
    """
    Load cleaned master dataset.
    """

    log("Loading feature.clean_master_dataset...")

    master = read_table(
        "feature",
        "clean_master_dataset"
    )

    dataframe_summary(master)

    return master

def dataset_overview(
    master: pd.DataFrame
):
    """
    Display dataset overview.
    """

    log("Generating dataset overview...")

    print("\nDataset Shape")
    print(master.shape)

    print("\nData Types\n")
    print(master.dtypes.value_counts())

    print("\nMemory Usage")

    memory = (
        master.memory_usage(deep=True).sum()
        / (1024 ** 2)
    )

    print(f"{memory:.2f} MB")

    print("\nSummary Statistics\n")

    print(
        master.describe().T
    )

def main():

    start = start_timer(
        "EDA : Dataset Overview"
    )

    master = load_data()

    dataset_overview(master)

    end_timer(start)

    log("Pipeline completed successfully.")


if __name__ == "__main__":
    main()