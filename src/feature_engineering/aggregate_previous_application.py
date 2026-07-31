import pandas as pd

from src.config import FINAL_DATA_DIR
from src.database import read_table, write_table
from src.feature_configs.previous_application_config import (
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
    Load previous application dataset.
    """

    log("Loading raw.previous_application...")

    previous_application = read_table(
        "raw",
        "previous_application"
    )

    validate_columns(
        previous_application,
        [
            "SK_ID_CURR",
            "AMT_APPLICATION",
            "AMT_CREDIT",
            "AMT_ANNUITY",
            "AMT_GOODS_PRICE",
            "CNT_PAYMENT",
            "DAYS_DECISION",
            "NAME_CONTRACT_STATUS",
            "NAME_CONTRACT_TYPE"
        ]
    )

    dataframe_summary(previous_application)

    return previous_application

# ==========================
# Create Numeric Features
# ==========================
def create_numeric_features(
    previous_application: pd.DataFrame
) -> pd.DataFrame:
    """
    Create customer-level numeric features.
    """

    log("Creating numeric features...")

    numeric_features = (
        previous_application
        .groupby("SK_ID_CURR")
        .agg(NUMERIC_AGGREGATIONS)
    )

    numeric_features.columns = [
        f"prev_{col.lower()}_{agg}"
        for col, agg in numeric_features.columns
    ]

    numeric_features = numeric_features.reset_index()

    dataframe_summary(numeric_features)

    return numeric_features

# ==========================
# Create Categorical Features
# ==========================
def create_categorical_features(
    previous_application: pd.DataFrame
) -> pd.DataFrame:
    """
    Create customer-level categorical features.
    """

    log("Creating categorical features...")

    categorical_features = []

    for column in CATEGORICAL_COLUMNS:

        crosstab = pd.crosstab(
            previous_application["SK_ID_CURR"],
            previous_application[column]
        )

        crosstab.columns = [
            f"prev_{column.lower()}_{str(col).lower().replace(' ', '_')}"
            for col in crosstab.columns
        ]

        categorical_features.append(crosstab)

    categorical_features = pd.concat(
        categorical_features,
        axis=1
    ).reset_index()

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

    previous_application_features = numeric_features.merge(
        categorical_features,
        on="SK_ID_CURR",
        how="left"
    )

    dataframe_summary(previous_application_features)

    return previous_application_features

# ==========================
# Create Ratio Features
# ==========================
def create_ratio_features(
    previous_application_features: pd.DataFrame
) -> pd.DataFrame:
    """
    Create business ratio features.
    """

    log("Creating ratio features...")

    previous_application_features["prev_credit_application_ratio"] = (
    previous_application_features["prev_amt_credit_mean"] /
    previous_application_features["prev_amt_application_mean"].replace(0, pd.NA)
)

    previous_application_features["prev_annuity_credit_ratio"] = (
    previous_application_features["prev_amt_annuity_mean"] /
    previous_application_features["prev_amt_credit_mean"].replace(0, pd.NA)
)

    dataframe_summary(previous_application_features)

    return previous_application_features

# ==========================
# Optimize Features
# ==========================
def optimize_features(
    previous_application_features: pd.DataFrame
) -> pd.DataFrame:
    """
    Optimize memory usage of previous application features.
    """

    log("Optimizing dataframe memory...")

    previous_application_features = optimize_memory(
        previous_application_features
    )

    return previous_application_features

# ==========================
# Save Features
# ==========================
def save_features(
    previous_application_features: pd.DataFrame
) -> None:
    """
    Save previous application features.
    """

    log("Saving previous application features...")

    write_table(
        previous_application_features,
        schema="feature",
        table_name="previous_application_features"
    )

    save_csv(
        previous_application_features,
        FINAL_DATA_DIR / OUTPUT_FILE
    )

    log("Previous application features saved successfully.")

# ==========================
# Main
# ==========================
def main():

    start = start_timer(
        "Feature Engineering Pipeline : Previous Application"
    )

    previous_application = load_data()

    numeric_features = create_numeric_features(
        previous_application
    )

    categorical_features = create_categorical_features(
        previous_application
    )

    previous_application_features = merge_features(
        numeric_features,
        categorical_features
    )

    previous_application_features = create_ratio_features(
        previous_application_features
    )

    previous_application_features = optimize_features(
        previous_application_features
    )

    save_features(
        previous_application_features
    )

    end_timer(start)

    log("Pipeline completed successfully.")

if __name__ == "__main__":
    main()