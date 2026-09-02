from doctest import master
from pathlib import Path

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split

from src.database import read_table
from src.utils import (
    log,
    dataframe_summary,
    start_timer,
    end_timer,
)

MODEL_DIR = Path("models")

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

#========================
#Load data
#========================
def load_data() -> pd.DataFrame:
    """
    Load cleaned dataset.
    """

    log("Loading feature.clean_master_dataset...")

    master = read_table(
        "feature",
        "clean_master_dataset"
    )

    master["bureau_debt_to_credit_ratio"] = pd.to_numeric(
    master["bureau_debt_to_credit_ratio"],
    errors="coerce"
)

    master["bureau_overdue_to_credit_ratio"] = pd.to_numeric(
    master["bureau_overdue_to_credit_ratio"],
    errors="coerce"
)

    dataframe_summary(master)

    return master

#=======================
#Split Features
#=======================
def prepare_data(master: pd.DataFrame):

    log("Preparing features and target...")

    X = master.drop(
        columns=["TARGET"]
    )

    y = master["TARGET"]

    print("\nData Types:\n")

    print(
        master.dtypes[
            [
                "bureau_debt_to_credit_ratio",
                "bureau_overdue_to_credit_ratio"
            ]
        ].head(10)
    )

    print("\nCategorical Columns:\n")

    categorical = X.select_dtypes(
        include=["object", "string"]
    )

    print(categorical.columns.tolist())

    return X, y


#=======================
#Train Test Split
#=======================
def split_dataset(
    X,
    y
):
    """
    Split dataset.
    """

    log("Splitting dataset...")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print()

    print(f"Train : {X_train.shape}")

    print(f"Test  : {X_test.shape}")

    return (
        X_train,
        X_test,
        y_train,
        y_test
    )

#=======================
#Saving Split Data
#=======================
def save_split(
    X_train,
    X_test,
    y_train,
    y_test
):
    """
    Save train and test datasets.
    """

    log("Saving train/test split...")

    joblib.dump(
        X_train,
        MODEL_DIR / "X_train.pkl"
    )

    joblib.dump(
        X_test,
        MODEL_DIR / "X_test.pkl"
    )

    joblib.dump(
        y_train,
        MODEL_DIR / "y_train.pkl"
    )

    joblib.dump(
        y_test,
        MODEL_DIR / "y_test.pkl"
    )
    
    log("Train/Test split saved successfully.")

#=======================
#Main Function
#=======================
def main():

    start = start_timer(
        "Machine Learning : Train/Test Split"
    )

    master = load_data()

    X, y = prepare_data(
        master
    )

    X_train, X_test, y_train, y_test = split_dataset(
        X,
        y
    )

    save_split(
        X_train,
        X_test,
        y_train,
        y_test
    )

    end_timer(start)

    log("Pipeline completed successfully.")


if __name__ == "__main__":
    main()

