import pandas as pd

from src.config import FINAL_DATA_DIR
from src.database import read_table, write_table
from src.feature_configs.installments_payments_config import (
    NUMERIC_AGGREGATIONS,
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
    Load installments payments dataset.
    """

    log("Loading raw.installments_payments...")

    installments = read_table(
        "raw",
        "installments_payments"
    )

    validate_columns(
        installments,
        [
            "SK_ID_CURR",
            "AMT_INSTALMENT",
            "AMT_PAYMENT",
            "DAYS_INSTALMENT",
            "DAYS_ENTRY_PAYMENT",
        ]
    )

    dataframe_summary(installments)

    return installments

# ==========================
# Create Behavior Features
# ==========================
def create_behavior_features(
    installments: pd.DataFrame
) -> pd.DataFrame:
    """
    Create payment behavior features.
    """

    log("Creating payment behavior features...")

    # Days payment was late (+) or early (-)
    installments["payment_delay"] = (
        installments["DAYS_ENTRY_PAYMENT"] -
        installments["DAYS_INSTALMENT"]
    )

    # Amount overpaid (+) or underpaid (-)
    installments["payment_difference"] = (
        installments["AMT_PAYMENT"] -
        installments["AMT_INSTALMENT"]
    )

    # Payment ratio
    installments["payment_ratio"] = (
        installments["AMT_PAYMENT"] /
        installments["AMT_INSTALMENT"].replace(0, pd.NA)
    )

    # Late payment flag
    installments["late_payment"] = (
        installments["payment_delay"] > 0
    ).astype(int)

    # Early payment flag
    installments["early_payment"] = (
        installments["payment_delay"] < 0
    ).astype(int)

    dataframe_summary(installments)

    return installments

# ==========================
# Create Numeric Features
# ==========================
def create_numeric_features(
    installments: pd.DataFrame
) -> pd.DataFrame:
    """
    Create customer-level numeric features.
    """

    log("Creating numeric features...")

    numeric_features = (
        installments
        .groupby("SK_ID_CURR")
        .agg({
            **NUMERIC_AGGREGATIONS,
            "payment_delay": ["mean", "max", "min"],
            "payment_difference": ["mean", "sum"],
            "payment_ratio": ["mean", "max"],
            "late_payment": ["sum", "mean"],
            "early_payment": ["sum", "mean"],
        })
    )

    numeric_features.columns = [
        f"inst_{col.lower()}_{agg}"
        for col, agg in numeric_features.columns
    ]

    numeric_features = numeric_features.reset_index()

    dataframe_summary(numeric_features)

    return numeric_features

# ==========================
# Optimize Features
# ==========================
def optimize_features(
    installments_features: pd.DataFrame
) -> pd.DataFrame:
    """
    Optimize memory usage.
    """

    log("Optimizing dataframe memory...")

    installments_features = optimize_memory(
        installments_features
    )

    return installments_features

# ==========================
# Save Features
# ==========================
def save_features(
    installments_features: pd.DataFrame
) -> None:
    """
    Save installments payment features.
    """

    log("Saving installments payment features...")

    write_table(
        installments_features,
        schema="feature",
        table_name="installments_payments_features"
    )

    save_csv(
        installments_features,
        FINAL_DATA_DIR / OUTPUT_FILE
    )

    log("Installments payment features saved successfully.")

# ==========================
# Main
# ==========================
def main():

    start = start_timer(
        "Feature Engineering Pipeline : Installments Payments"
    )

    installments = load_data()

    installments = create_behavior_features(
        installments
    )

    installments_features = create_numeric_features(
        installments
    )

    installments_features = optimize_features(
        installments_features
    )

    save_features(
        installments_features
    )

    end_timer(start)

    log("Pipeline completed successfully.")

if __name__ == "__main__":
    main()