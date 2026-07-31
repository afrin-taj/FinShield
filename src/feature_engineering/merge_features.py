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
# Load Data
# ==========================
def load_data():
    """
    Load application and all engineered feature tables.
    """

    log("Loading feature tables...")

    application = read_table(
        "raw",
        "application_train"
    )

    bureau = read_table(
        "feature",
        "bureau_features"
    )

    bureau_balance = read_table(
        "feature",
        "bureau_balance_features"
    )

    previous_application = read_table(
        "feature",
        "previous_application_features"
    )

    pos_cash = read_table(
        "feature",
        "pos_cash_balance_features"
    )

    installments = read_table(
        "feature",
        "installments_payments_features"
    )

    credit_card = read_table(
        "feature",
        "credit_card_balance_features"
    )

    return (
        application,
        bureau,
        bureau_balance,
        previous_application,
        pos_cash,
        installments,
        credit_card,
    )

# ==========================
# Merge Features
# ==========================
def merge_features(
    application,
    bureau,
    bureau_balance,
    previous_application,
    pos_cash,
    installments,
    credit_card,
):
    """
    Merge all feature tables.
    """

    log("Merging feature tables...")

    master = application.copy()

    tables = [
        bureau,
        bureau_balance,
        previous_application,
        pos_cash,
        installments,
        credit_card,
    ]

    for table in tables:

        master = master.merge(
            table,
            on="SK_ID_CURR",
            how="left"
        )

        log(f"Merged -> {table.shape}")

    dataframe_summary(master)

    return master

# ==========================
# optimize Features
# ==========================
def optimize_features(master):

    log("Optimizing dataframe...")

    return optimize_memory(master)

# ==========================
# Save Features
# ==========================
def save_master_dataset(master):

    log("Saving master dataset...")

    write_table(
        master,
        schema="feature",
        table_name="master_dataset"
    )

    save_csv(
        master,
        FINAL_DATA_DIR / "master_dataset.csv"
    )

    log("Master dataset saved successfully.")

# ==========================
# Main
# ==========================
def main():

    start = start_timer(
        "Feature Engineering Pipeline : Merge Features"
    )

    (
        application,
        bureau,
        bureau_balance,
        previous_application,
        pos_cash,
        installments,
        credit_card,
    ) = load_data()

    master = merge_features(
        application,
        bureau,
        bureau_balance,
        previous_application,
        pos_cash,
        installments,
        credit_card,
    )

    master = optimize_features(master)

    save_master_dataset(master)

    end_timer(start)

    log("Pipeline completed successfully.")

if __name__ == "__main__":
    main()