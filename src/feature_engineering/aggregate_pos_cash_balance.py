import pandas as pd

from src.config import FINAL_DATA_DIR
from src.database import read_table, write_table
from src.feature_configs.pos_cash_balance_config import (
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
def load_data() -> pd.DataFrame:
    """
    Load POS_CASH_balance dataset.
    """

    log("Loading raw.pos_cash_balance...")

    pos_cash_balance = read_table(
        "raw",
        "pos_cash_balance"
    )

    validate_columns(
        pos_cash_balance,
        [
            "SK_ID_CURR",
            "MONTHS_BALANCE",
            "CNT_INSTALMENT",
            "CNT_INSTALMENT_FUTURE",
            "SK_DPD",
            "SK_DPD_DEF",
            "NAME_CONTRACT_STATUS",
        ]
    )

    dataframe_summary(pos_cash_balance)

    return pos_cash_balance

# ==========================
# 
# ==========================
def create_numeric_features(
    pos_cash_balance: pd.DataFrame
) -> pd.DataFrame:
    """
    Create customer-level numeric features.
    """

    log("Creating numeric features...")

    numeric_features = (
        pos_cash_balance
        .groupby("SK_ID_CURR")
        .agg(NUMERIC_AGGREGATIONS)
    )

    numeric_features.columns = [
        f"pos_{col.lower()}_{agg}"
        for col, agg in numeric_features.columns
    ]

    numeric_features = numeric_features.reset_index()

    dataframe_summary(numeric_features)

    return numeric_features

# ==========================
# Create Categorical Features
# ==========================
def create_categorical_features(
    pos_cash_balance: pd.DataFrame
) -> pd.DataFrame:
    """
    Create customer-level categorical features.
    """

    log("Creating categorical features...")

    categorical_features = pd.crosstab(
        pos_cash_balance["SK_ID_CURR"],
        pos_cash_balance["NAME_CONTRACT_STATUS"]
    )

    categorical_features.columns = [
        f"pos_status_{str(col).lower().replace(' ', '_')}"
        for col in categorical_features.columns
    ]

    categorical_features = categorical_features.reset_index()

    dataframe_summary(categorical_features)

    return categorical_features

# ==========================
# Merge Features
# ==========================
def merge_features(
    numeric_features: pd.DataFrame,
    categorical_features: pd.DataFrame
) -> pd.DataFrame:
    """
    Merge numeric and categorical features.
    """

    log("Merging customer features...")

    pos_cash_features = numeric_features.merge(
        categorical_features,
        on="SK_ID_CURR",
        how="left"
    )

    dataframe_summary(pos_cash_features)

    return pos_cash_features

# ==========================
# Create Ratio Features
# ==========================
def create_ratio_features(
    pos_cash_features: pd.DataFrame
) -> pd.DataFrame:
    """
    Create business features.
    """

    log("Creating business features...")

    pos_cash_features["pos_completion_ratio"] = (
        pos_cash_features["pos_cnt_instalment_future_mean"] /
        pos_cash_features["pos_cnt_instalment_mean"]
    )

    pos_cash_features["pos_dpd_ratio"] = (
        pos_cash_features["pos_sk_dpd_mean"] /
        (pos_cash_features["pos_sk_dpd_def_mean"] + 1)
    )

    dataframe_summary(pos_cash_features)

    return pos_cash_features

# ==========================
# Optimize Features
# ==========================
def optimize_features(
    pos_cash_features: pd.DataFrame
) -> pd.DataFrame:
    """
    Optimize memory usage.
    """

    log("Optimizing dataframe memory...")

    pos_cash_features = optimize_memory(
        pos_cash_features
    )

    return pos_cash_features

# ==========================
# Save Features
# ==========================
def save_features(
    pos_cash_features: pd.DataFrame
) -> None:
    """
    Save POS CASH features.
    """

    log("Saving POS CASH features...")

    write_table(
        pos_cash_features,
        schema="feature",
        table_name="pos_cash_balance_features"
    )

    save_csv(
        pos_cash_features,
        FINAL_DATA_DIR / OUTPUT_FILE
    )

    log("POS CASH features saved successfully.")

# ==========================
# Main
# ==========================
def main():

    start = start_timer(
        "Feature Engineering Pipeline : POS CASH Balance"
    )

    pos_cash_balance = load_data()

    numeric_features = create_numeric_features(
        pos_cash_balance
    )

    categorical_features = create_categorical_features(
        pos_cash_balance
    )

    pos_cash_features = merge_features(
        numeric_features,
        categorical_features
    )

    pos_cash_features = create_ratio_features(
        pos_cash_features
    )

    pos_cash_features = optimize_features(
        pos_cash_features
    )

    save_features(
        pos_cash_features
    )

    end_timer(start)

    log("Pipeline completed successfully.")

if __name__ == "__main__":
    main()