import pandas as pd

from src.database import read_table
from src.utils import (
    log,
    dataframe_summary,
    start_timer,
    end_timer,
)
#===========================
#Load Data
#===========================
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

#===========================
#Feature Selection
#===========================
def split_features(
    master: pd.DataFrame
):
    """
    Separate features and target.
    """

    log("Separating features and target...")

    X = master.drop(
        columns=["TARGET"]
    )

    y = master["TARGET"]

    print()

    print(f"Features : {X.shape[1]}")
    print(f"Target   : {y.name}")

    return X, y

#===========================
#Constant Features
#===========================
def constant_features(
    X: pd.DataFrame
):
    """
    Find constant features.
    """

    log("Checking constant features...")

    constant = []

    for column in X.columns:

        if X[column].nunique() == 1:

            constant.append(column)

    print()

    print(f"Constant Features : {len(constant)}")

    if constant:

        print()

        for column in constant:

            print(column)

    return constant

#===========================
#Missing Features
#===========================
def missing_features(
    X: pd.DataFrame
):
    """
    Check remaining missing values.
    """

    log("Checking missing values...")

    missing = X.isnull().sum()

    missing = missing[
        missing > 0
    ]

    print()

    print(f"Columns with Missing Values : {len(missing)}")

#============================
#Low Variance Features
#============================
def low_variance_features(
    X: pd.DataFrame
):
    """
    Detect low variance features.
    """

    log("Checking low variance features...")

    variance = X.var(
        numeric_only=True
    )

    low = variance[
        variance < 0.01
    ]

    print()

    print(f"Low Variance Features : {len(low)}")

    return low

#===========================
#Main Function
#===========================S
def main():

    start = start_timer(
        "EDA : Feature Selection"
    )

    master = load_data()

    X, y = split_features(master)

    constant_features(X)

    missing_features(X)

    low_variance_features(X)

    end_timer(start)

    log("Pipeline completed successfully.")


if __name__ == "__main__":
    main()

