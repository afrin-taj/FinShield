"""
FinShield Prediction Pipeline
-----------------------------
Predicts loan default risk for customers
provided in prediction_input.csv.
"""

import joblib
import pandas as pd

from src.config import MODELS_DIR
from src.utils import log


# ==========================
# Load Model
# ==========================

def load_model():
    """
    Load the final trained XGBoost model.
    """

    log("Loading final XGBoost model...")

    model = joblib.load(
        MODELS_DIR / "xgboost_model.pkl"
    )

    log("Model loaded successfully.")

    return model


# ==========================
# Load Feature Names
# ==========================

def load_feature_names():
    """
    Load the exact feature names used during
    XGBoost training.
    """

    log("Loading training feature names...")

    feature_names = joblib.load(
        MODELS_DIR / "xgboost_features.pkl"
    )

    log(
        f"Features loaded : {len(feature_names)}"
    )

    return feature_names


# ==========================
# Load Customer Data
# ==========================

def load_customer_data():
    """
    Load customer information from CSV.
    """

    log("Loading prediction input...")

    customer = pd.read_csv(
        "data/prediction_input.csv"
    )

    print(
        f"Input rows    : {customer.shape[0]}"
    )

    print(
        f"Input columns : {customer.shape[1]}"
    )

    return customer


# ==========================
# Prepare Features
# ==========================

def prepare_features(
    customer,
    feature_names
):
    """
    Encode categorical features and make sure
    the prediction data has exactly the same
    features as the training data.
    """

    log("Preparing prediction features...")

    # Find categorical columns
    categorical_columns = customer.select_dtypes(
        include=["object", "string"]
    ).columns.tolist()

    # One-hot encode categorical columns
    customer = pd.get_dummies(
        customer,
        columns=categorical_columns,
        drop_first=True,
        dtype="uint8"
    )

    # --------------------------
    # Add Missing Features
    # --------------------------

    missing_columns = [
        column
        for column in feature_names
        if column not in customer.columns
    ]

    if missing_columns:

        missing_data = pd.DataFrame(
            0,
            index=customer.index,
            columns=missing_columns
        )

        customer = pd.concat(
            [
                customer,
                missing_data
            ],
            axis=1
        )

    # --------------------------
    # Remove Extra Features
    # --------------------------

    customer = customer[
        [
            column
            for column in feature_names
            if column in customer.columns
        ]
    ]

    # --------------------------
    # Exact Feature Order
    # --------------------------

    customer = customer.reindex(
        columns=feature_names,
        fill_value=0
    )

    log(
        f"Final features : {customer.shape[1]}"
    )

    return customer


# ==========================
# Make Predictions
# ==========================

def predict(
    model,
    customer
):
    """
    Generate default probabilities
    and classifications.
    """

    log("Generating prediction...")

    # Probability of class 1 (default)
    probabilities = model.predict_proba(
        customer
    )[:, 1]

    # Final XGBoost threshold
    threshold = 0.15

    predictions = (
        probabilities >= threshold
    ).astype(int)

    return (
        probabilities,
        predictions
    )


# ==========================
# Display Results
# ==========================

def display_result(
    probability,
    prediction,
    customer_number
):
    """
    Display the risk assessment.
    """

    probability_percent = (
        probability * 100
    )

    if prediction == 1:

        risk = "HIGH RISK"
        result = "DEFAULT"

    else:

        risk = "LOW RISK"
        result = "NON-DEFAULT"

    print()
    print("=" * 60)

    print(
        f"FinShield : Customer {customer_number}"
    )

    print("=" * 60)

    print()

    print(
        f"Default Probability : "
        f"{probability_percent:.2f}%"
    )

    print(
        f"Risk Level          : "
        f"{risk}"
    )

    print(
        f"Prediction          : "
        f"{result}"
    )

    print()
    print("=" * 60)


# ==========================
# Main
# ==========================

def main():

    log(
        "Starting FinShield prediction pipeline..."
    )

    # Load model
    model = load_model()

    # Load training feature names
    feature_names = load_feature_names()

    # Load customer input
    customer = load_customer_data()

    # Prepare features
    customer = prepare_features(
        customer,
        feature_names
    )

    # Generate predictions
    probabilities, predictions = predict(
        model,
        customer
    )

    # Display results
    for index, (
        probability,
        prediction
    ) in enumerate(
        zip(
            probabilities,
            predictions
        ),
        start=1
    ):

        display_result(
            probability,
            prediction,
            index
        )

    log(
        "Prediction pipeline completed successfully."
    )


# ==========================
# Entry Point
# ==========================

if __name__ == "__main__":
    main()