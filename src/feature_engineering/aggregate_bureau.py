"""
Feature Engineering - Bureau Table
----------------------------------
Creates customer-level features from the raw.bureau table.
"""

# ==========================
# Imports
# ==========================

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add the src folder to Python's path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.config import (
    RAW_SCHEMA,
    FEATURE_SCHEMA,
    FINAL_DATA_DIR
)

from src.database import (
    read_table,
    write_table
)

from src.utils import (
    log,
    validate_columns,
    dataframe_summary,
    save_csv,
    start_timer,
    end_timer,
    separator
)

from src.feature_configs.bureau_config import (
    NUMERIC_AGGREGATIONS,
    CATEGORICAL_COLUMNS,
    OUTPUT_FILE,
    OUTPUT_TABLE,
    RATIO_FEATURES
)
# ==========================
# Required Columns
# ==========================

REQUIRED_COLUMNS = [
    "SK_ID_CURR",
    "SK_ID_BUREAU",
    "CREDIT_ACTIVE",
    "CREDIT_TYPE",
    "CREDIT_CURRENCY",
    "AMT_CREDIT_SUM",
    "AMT_CREDIT_SUM_DEBT",
    "AMT_CREDIT_SUM_OVERDUE",
    "AMT_CREDIT_SUM_LIMIT",
    "AMT_ANNUITY",
    "DAYS_CREDIT",
    "DAYS_CREDIT_ENDDATE",
    "DAYS_ENDDATE_FACT",
    "DAYS_CREDIT_UPDATE",
    "CREDIT_DAY_OVERDUE",
    "CNT_CREDIT_PROLONG"
]
# ==========================
# Load Data
# ==========================

def load_data() -> pd.DataFrame:
    """
    Load bureau table from PostgreSQL and validate it.
    """

    log("Loading raw.bureau table...")

    bureau = read_table(RAW_SCHEMA, "bureau")

    validate_columns(bureau, REQUIRED_COLUMNS)

    dataframe_summary(bureau)

    log("Bureau table loaded successfully.")

    return bureau

# ==========================
# Numeric Features
# ==========================
def create_numeric_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates customer-level numeric features.
    """

    log("Creating numeric features...")

    numeric_features = (
        df
        .groupby("SK_ID_CURR")
        .agg(NUMERIC_AGGREGATIONS)
    )

    # Flatten MultiIndex column names
    numeric_features.columns = [
        f"bureau_{column.lower()}_{aggregation.lower()}"
        for column, aggregation in numeric_features.columns
    ]

    # Rename count column
    numeric_features.rename(
        columns={
            "bureau_sk_id_bureau_count": "bureau_total_loans"
        },
        inplace=True
    )

    numeric_features.reset_index(inplace=True)

    dataframe_summary(numeric_features)

    return numeric_features

# ==========================
# Categorical Features
# ==========================
def aggregate_categorical_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates customer-level categorical features.
    """

    log("Creating categorical features...")

    categorical_features = []

    for column in CATEGORICAL_COLUMNS:

        temp = pd.crosstab(
            df["SK_ID_CURR"],
            df[column]
        )

        temp.columns = [
            f"bureau_{column.lower()}_{str(value).lower().replace(' ', '_').replace('/', '_')}"
            for value in temp.columns
        ]

        categorical_features.append(temp)

    categorical_features = pd.concat(
        categorical_features,
        axis=1
    ).reset_index()

    dataframe_summary(categorical_features)

    return categorical_features

# ==========================
# Merge Features
# ==========================
def merge_bureau_features(numeric_features: pd.DataFrame, categorical_features: pd.DataFrame) -> pd.DataFrame:
    """
    Merge all bureau features into a single dataframe.
    """

    log("Merging bureau features...")

    bureau_features = numeric_features.merge(
        categorical_features,
        on="SK_ID_CURR",
        how="left"
    )

    dataframe_summary(bureau_features)

    return bureau_features

# ==========================
# Ratio Features
# ==========================

def create_ratio_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create ratio-based bureau features.
    """

    log("Creating ratio features...")

    for feature_name, (numerator, denominator) in RATIO_FEATURES.items():

        denominator_values = (
            df[denominator]
            .replace(0, np.nan)
        )

        df[feature_name] = (
            df[numerator] / denominator_values
        )

        df[feature_name] = (
            df[feature_name]
            .fillna(0)
            .astype("float64")
        )

    dataframe_summary(df)

    return df

# ==========================
# Optimize Memory
# ==========================

def optimize_memory(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reduce dataframe memory usage by downcasting numeric columns.
    """

    log("Optimizing dataframe memory...")

    for column in df.select_dtypes(include=["int64"]).columns:
        df[column] = pd.to_numeric(df[column], downcast="integer")

    for column in df.select_dtypes(include=["float64"]).columns:
        df[column] = pd.to_numeric(df[column], downcast="float")

    dataframe_summary(df)

    return df

# ==========================
# Save Features
# ==========================
def save_features(df: pd.DataFrame)-> None:
    """
    Save bureau features to PostgreSQL and CSV.
    """

    log("Saving bureau features...")

    write_table(
        df=df,
        schema=FEATURE_SCHEMA,
        table_name=OUTPUT_TABLE
    )

    save_csv(
        df,
        FINAL_DATA_DIR / OUTPUT_FILE
    )

    log("Bureau features saved successfully.")

print("\nRatio Feature Data Types:\n")

# ==========================
# Main
# ==========================

def main() -> None:
    """
    Run the Bureau feature engineering pipeline.
    """

    start = start_timer(
        "Feature Engineering Pipeline : Bureau"
    )

    try:

        bureau = load_data()

        numeric_features = create_numeric_features(
            bureau
        )

        categorical_features = aggregate_categorical_features(
            bureau
        )

        bureau_features = merge_bureau_features(
            numeric_features,
            categorical_features
        )

        bureau_features = create_ratio_features(
            bureau_features
        )

        bureau_features = optimize_memory(
            bureau_features
        )

        save_features(
            bureau_features
        )

        print("\nFinal Bureau Features\n")
        print(bureau_features.head())

    except Exception as e:

        separator()

        log("Pipeline Failed")
        log(f"ERROR : {e}")

        separator()

    finally:

        end_timer(start)

        log("Pipeline completed successfully.")

bureau = read_table(
    "feature",
    "bureau_features"
)

if __name__ == "__main__":
    main()