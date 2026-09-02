"""
Create a CSV template for single-customer predictions.
"""

import joblib
import pandas as pd

from src.config import MODELS_DIR
from src.utils import log


def main():

    log("Loading test dataset...")

    X_test = joblib.load(
        MODELS_DIR / "X_test.pkl"
    )

    # Take one customer as a template
    customer = X_test.iloc[[0]].copy()

    output_file = (
        "data/prediction_input.csv"
    )

    customer.to_csv(
        output_file,
        index=False
    )

    print()
    print(
        f"Prediction template created:"
    )

    print(
        output_file
    )

    print()
    print(
        f"Columns : {customer.shape[1]}"
    )


if __name__ == "__main__":
    main()