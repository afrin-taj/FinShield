import pandas as pd

from src.config import FINAL_DATA_DIR
from src.database import read_table, write_table
from src.utils import (
    log,
    dataframe_summary,
    save_csv,
    optimize_memory,
    start_timer,
    end_timer,
)
# ==========================
# load_data
# ==========================

def load_data() -> pd.DataFrame:
    """
    Load merged master dataset.
    """

    log("Loading feature.master_dataset...")

    master = read_table(
        "feature",
        "master_dataset"
    )

    dataframe_summary(master)

    return master

# ==========================
# Analyszing Missing Values
# ==========================
def analyze_missing_values(
    master: pd.DataFrame
) -> pd.DataFrame:
    """
    Analyze missing values in the dataset.
    """

    log("Analyzing missing values...")

    missing = (
        master.isnull()
        .sum()
        .reset_index()
    )

    missing.columns = [
        "Column",
        "Missing_Values"
    ]

    missing["Missing_Percentage"] = (
        missing["Missing_Values"] /
        len(master)
    ) * 100

    missing = missing.sort_values(
        "Missing_Percentage",
        ascending=False
    )

    print("\nTop 20 Columns with Missing Values\n")

    print(
        missing.head(20)
    )

    return missing

# ==========================
# Dropping Empty Columns
# ==========================
def drop_empty_columns(
    master: pd.DataFrame
) -> pd.DataFrame:
    """
    Drop columns that contain only missing values.
    """

    log("Dropping completely empty columns...")

    empty_columns = master.columns[
        master.isnull().all()
    ]

    if len(empty_columns) > 0:

        print("\nDropped Columns\n")

        for column in empty_columns:
            print(column)

        master = master.drop(
            columns=empty_columns
        )

    else:

        log("No completely empty columns found.")

    dataframe_summary(master)

    return master

# ==========================
# Filling Missing Values
# ==========================
def fill_missing_values(
    master: pd.DataFrame
) -> pd.DataFrame:
    """
    Fill missing values.
    """

    log("Filling missing values...")

    numeric_columns = master.select_dtypes(
        include=["number"]
    ).columns

    categorical_columns = master.select_dtypes(
        exclude=["number"]
    ).columns

    # Fill numeric columns with median
    for column in numeric_columns:
        master[column] = master[column].fillna(
            master[column].median()
        )

    # Fill categorical columns with mode
    for column in categorical_columns:
        if master[column].isnull().any():
            master[column] = master[column].fillna(
                master[column].mode()[0]
            )

    dataframe_summary(master)

    return master
# ==========================
# Verify Missing Values
# ==========================
def verify_missing_values(
    master: pd.DataFrame
):
    """
    Verify remaining missing values.
    """

    log("Verifying missing values...")

    missing = master.isnull().sum().sum()

    print()

    print(f"Remaining Missing Values : {missing:,}")


#=========================
# Load Feature Tables
#=========================
def optimize_features(
    master: pd.DataFrame
) -> pd.DataFrame:
    """
    Optimize memory usage.
    """

    log("Optimizing dataframe memory...")

    master = optimize_memory(master)

    dataframe_summary(master)

    return master

#=========================
# Save Clean Dataset
#=========================
def save_clean_dataset(
    master: pd.DataFrame
):
    """
    Save cleaned master dataset.
    """

    log("Saving cleaned dataset...")

    write_table(
        master,
        schema="feature",
        table_name="clean_master_dataset"
    )

    save_csv(
        master,
        FINAL_DATA_DIR / "clean_master_dataset.csv"
    )

    log("Clean master dataset saved successfully.")

# ==========================
# Main
# ==========================
def main():

    start = start_timer(
        "Data Cleaning Pipeline"
    )

    master = load_data()
    missing = analyze_missing_values(master)
    master = drop_empty_columns(master)
    master = fill_missing_values(master)
    verify_missing_values(master)
    master = optimize_features(master)
    save_clean_dataset(master)

    end_timer(start)

    log("Pipeline completed successfully.")



if __name__ == "__main__":
    main()