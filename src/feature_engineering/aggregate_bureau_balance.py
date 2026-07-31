import pandas as pd
from src.config import FINAL_DATA_DIR
from src.database import read_table, write_table
from src.feature_configs.bureau_balance_config import (
    NUMERIC_AGGREGATIONS,
    CATEGORICAL_COLUMNS,
    OUTPUT_TABLE,
    OUTPUT_FILE,
)

from src.utils import (
    log,
    validate_columns,
    dataframe_summary,
    save_csv,
    optimize_memory,
    start_timer,
    end_timer,
)
# ==========================
# Load Data
# ==========================
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load bureau and bureau_balance tables.
    """

    log("Loading raw.bureau_balance...")

    bureau_balance = read_table("raw", "bureau_balance")

    validate_columns(
        bureau_balance,
        ["SK_ID_BUREAU", "MONTHS_BALANCE", "STATUS"]
    )

    dataframe_summary(bureau_balance)

    log("Loading raw.bureau...")
    bureau = read_table("raw", "bureau")

    validate_columns(
        bureau,
        ["SK_ID_BUREAU", "SK_ID_CURR"]
    )

    dataframe_summary(bureau)

    return bureau_balance, bureau
# ==========================
# Create Numeric Features
# ==========================
def create_numeric_features(
    bureau_balance: pd.DataFrame
) -> pd.DataFrame:
    """
    Create numeric features for each bureau loan.
    """

    log("Creating numeric features...")

    numeric_features = (
        bureau_balance
        .groupby("SK_ID_BUREAU")
        .agg(NUMERIC_AGGREGATIONS)
    )

    numeric_features.columns = [
        f"bb_{col}_{agg}"
        for col, agg in numeric_features.columns
    ]

    numeric_features = numeric_features.reset_index()

    dataframe_summary(numeric_features)

    return numeric_features
# ==========================
# create Categorical Features
# ==========================
def create_categorical_features(
    bureau_balance: pd.DataFrame
) -> pd.DataFrame:
    """
    Create categorical features from loan status.
    """

    log("Creating categorical features...")

    categorical_features = pd.crosstab(
        bureau_balance["SK_ID_BUREAU"],
        bureau_balance["STATUS"]
    )

    categorical_features.columns = [
        f"bb_status_{col.lower()}"
        for col in categorical_features.columns
    ]

    categorical_features = categorical_features.reset_index()

    dataframe_summary(categorical_features)

    return categorical_features
# ==========================
# Merge Numeric and Categorical Features
# ==========================
def merge_features(
    numeric_features: pd.DataFrame,
    categorical_features: pd.DataFrame
) -> pd.DataFrame:
    """
    Merge numeric and categorical features.
    """

    log("Merging loan-level features...")

    bureau_balance_features = numeric_features.merge(
        categorical_features,
        on="SK_ID_BUREAU",
        how="left"
    )

    dataframe_summary(bureau_balance_features)

    return bureau_balance_features
# ==========================
# Map Bureau Loans to Customers
# ==========================
def map_customer_id(
    bureau_balance_features: pd.DataFrame,
    bureau: pd.DataFrame
) -> pd.DataFrame:
    """
    Map each bureau loan to its customer.
    """

    log("Mapping bureau loans to customers...")

    bureau_balance_features = bureau_balance_features.merge(
        bureau[["SK_ID_BUREAU", "SK_ID_CURR"]],
        on="SK_ID_BUREAU",
        how="left"
    )

    dataframe_summary(bureau_balance_features)

    return bureau_balance_features
# ==========================
# Aggregate Customer-Level Features
# ==========================
def aggregate_customer_features(
    bureau_balance_features: pd.DataFrame
) -> pd.DataFrame:
    """
    Aggregate bureau balance features to customer level.
    """

    log("Aggregating customer-level features...")

    customer_features = (
        bureau_balance_features
        .drop(columns=["SK_ID_BUREAU"])
        .groupby("SK_ID_CURR")
        .agg(["mean", "max", "sum"])
    )

    customer_features.columns = [
        f"{col}_{agg}"
        for col, agg in customer_features.columns
    ]

    customer_features = customer_features.reset_index()

    dataframe_summary(customer_features)

    return customer_features
# ==========================
# Optimize Features
# ==========================
def optimize_features(
    customer_features: pd.DataFrame
) -> pd.DataFrame:
    """
    Optimize customer feature dataframe memory.
    """

    log("Optimizing dataframe memory...")

    customer_features = optimize_memory(customer_features)

    dataframe_summary(customer_features)

    return customer_features
# ==========================
# Logging and Saving Features
# ==========================
def save_features(
    customer_features: pd.DataFrame
) -> None:
    """
    Save customer features to PostgreSQL and CSV.
    """

    log("Saving bureau balance features...")

    write_table(
        customer_features,
        schema="feature",
        table_name="bureau_balance_features"
    )

    save_csv(
        customer_features,
        FINAL_DATA_DIR / OUTPUT_FILE
    )

    log("Bureau balance features saved successfully.")
# ==========================
# Main
# ==========================
def main():

    start = start_timer("Feature Engineering Pipeline : Bureau Balance")

    try:

        bureau_balance, bureau = load_data()
        numeric_features = create_numeric_features(
             bureau_balance
        )
        categorical_features = create_categorical_features(
            bureau_balance
        )
        bureau_balance_features = merge_features(
            numeric_features,
            categorical_features
        )
        bureau_balance_features = map_customer_id(
            bureau_balance_features,
            bureau
        )
        bureau_balance_customer_features = aggregate_customer_features(
            bureau_balance_features
        )
        customer_features = optimize_features(
            bureau_balance_customer_features
        )
        save_features(
        customer_features
    )

    except Exception as e:
        log(f"ERROR : {e}")

    finally:
        end_timer(start)

if __name__ == "__main__":
    main()