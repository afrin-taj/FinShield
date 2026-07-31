import pandas as pd

from src.config import FINAL_DATA_DIR
from src.database import read_table, write_table
from src.feature_configs.credit_card_balance_config import (
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
    Load credit card balance dataset.
    """

    log("Loading raw.credit_card_balance...")

    credit_card = read_table(
        "raw",
        "credit_card_balance"
    )

    validate_columns(
        credit_card,
        [
            "SK_ID_CURR",
            "AMT_BALANCE",
            "AMT_CREDIT_LIMIT_ACTUAL",
            "AMT_PAYMENT_CURRENT",
            "AMT_PAYMENT_TOTAL_CURRENT",
            "AMT_RECEIVABLE_PRINCIPAL",
            "AMT_TOTAL_RECEIVABLE",
            "SK_DPD",
            "SK_DPD_DEF",
            "NAME_CONTRACT_STATUS",
        ]
    )

    dataframe_summary(credit_card)

    return credit_card
# ==========================
# Create Behavior Features
# ==========================
def create_behavior_features(
    credit_card: pd.DataFrame
) -> pd.DataFrame:
    """
    Create credit card behavior features.
    """

    log("Creating credit card behavior features...")

    # Credit utilization ratio
    credit_card["credit_utilization_ratio"] = (
        credit_card["AMT_BALANCE"] /
        credit_card["AMT_CREDIT_LIMIT_ACTUAL"].replace(0, pd.NA)
    )

    # Payment ratio
    credit_card["payment_ratio"] = (
        credit_card["AMT_PAYMENT_CURRENT"] /
        credit_card["AMT_BALANCE"].replace(0, pd.NA)
    )

    # Receivable ratio
    credit_card["receivable_ratio"] = (
        credit_card["AMT_TOTAL_RECEIVABLE"] /
        credit_card["AMT_CREDIT_LIMIT_ACTUAL"].replace(0, pd.NA)
    )

    dataframe_summary(credit_card)

    return credit_card

# ==========================
# Create Numeric Features
# ==========================
def create_numeric_features(
    credit_card: pd.DataFrame
) -> pd.DataFrame:
    """
    Create customer-level numeric features.
    """

    log("Creating numeric features...")

    numeric_features = (
        credit_card
        .groupby("SK_ID_CURR")
        .agg({
            **NUMERIC_AGGREGATIONS,
            "credit_utilization_ratio": ["mean", "max"],
            "payment_ratio": ["mean", "max"],
            "receivable_ratio": ["mean", "max"],
        })
    )

    numeric_features.columns = [
        f"cc_{col.lower()}_{agg}"
        for col, agg in numeric_features.columns
    ]

    numeric_features = numeric_features.reset_index()

    dataframe_summary(numeric_features)

    return numeric_features

# ==========================
# create Categorical Features
# ==========================
def create_categorical_features(
    credit_card: pd.DataFrame
) -> pd.DataFrame:
    """
    Create customer-level categorical features.
    """

    log("Creating categorical features...")

    categorical_features = pd.crosstab(
        credit_card["SK_ID_CURR"],
        credit_card["NAME_CONTRACT_STATUS"]
    )

    categorical_features.columns = [
        f"cc_status_{str(col).lower().replace(' ', '_')}"
        for col in categorical_features.columns
    ]

    categorical_features = categorical_features.reset_index()

    dataframe_summary(categorical_features)

    return categorical_features

# ==========================
# Load All Features
# ==========================
def merge_features(
    numeric_features: pd.DataFrame,
    categorical_features: pd.DataFrame
) -> pd.DataFrame:
    """
    Merge customer-level features.
    """

    log("Merging customer features...")

    credit_card_features = numeric_features.merge(
        categorical_features,
        on="SK_ID_CURR",
        how="left"
    )

    dataframe_summary(credit_card_features)

    return credit_card_features

# ==========================
# Optimize Features
# ==========================
def optimize_features(
    credit_card_features: pd.DataFrame
) -> pd.DataFrame:
    """
    Optimize dataframe memory.
    """

    log("Optimizing dataframe memory...")

    credit_card_features = optimize_memory(
        credit_card_features
    )

    return credit_card_features

# ==========================
# Save Features
# ==========================
def save_features(
    credit_card_features: pd.DataFrame
) -> None:
    """
    Save credit card features.
    """

    log("Saving credit card features...")

    write_table(
        credit_card_features,
        schema="feature",
        table_name="credit_card_balance_features"
    )

    save_csv(
        credit_card_features,
        FINAL_DATA_DIR / OUTPUT_FILE
    )

    log("Credit card features saved successfully.")

# ==========================
# Main
# ==========================
def main():

    start = start_timer(
        "Feature Engineering Pipeline : Credit Card Balance"
    )

    credit_card = load_data()

    credit_card = create_behavior_features(
        credit_card
    )

    numeric_features = create_numeric_features(
        credit_card
    )

    categorical_features = create_categorical_features(
        credit_card
    )

    credit_card_features = merge_features(
        numeric_features,
        categorical_features
    )

    credit_card_features = optimize_features(
        credit_card_features
    )

    save_features(
        credit_card_features
    )

    end_timer(start)

    log("Pipeline completed successfully.")

if __name__ == "__main__":
    main()