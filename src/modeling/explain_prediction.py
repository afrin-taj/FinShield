"""
FinShield Model Explainability
------------------------------
Generates SHAP explanations for
individual customer credit-risk predictions.
"""

import joblib
import pandas as pd
import shap

from src.config import MODELS_DIR
from src.modeling.predict import prepare_features


# ============================================================
# Load Model
# ============================================================

def load_model():

    return joblib.load(
        MODELS_DIR / "xgboost_model.pkl"
    )


# ============================================================
# Load Training Feature Names
# ============================================================

def load_feature_names():

    return joblib.load(
        MODELS_DIR / "xgboost_features.pkl"
    )


# ============================================================
# Prepare Customer
# ============================================================

def prepare_customer(customer):

    feature_names = load_feature_names()

    features = prepare_features(
        customer,
        feature_names
    )

    return features


# ============================================================
# Generate SHAP Values
# ============================================================

def explain_customer(
    model,
    features
):
    """
    Generate SHAP values for a customer.

    Positive SHAP values push the prediction
    toward default.

    Negative SHAP values push the prediction
    toward non-default.
    """

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(
        features
    )

    # SHAP versions may return either
    # an array or a list for binary classification.

    if isinstance(shap_values, list):

        shap_values = shap_values[1]

    shap_values = shap_values[0]

    explanation = pd.DataFrame(
        {
            "feature": features.columns,
            "value": features.iloc[0].values,
            "shap_value": shap_values
        }
    )

    # Absolute SHAP value shows
    # how strongly the feature influenced
    # the prediction.

    explanation["importance"] = (
        explanation["shap_value"].abs()
    )

    explanation = explanation.sort_values(
        "importance",
        ascending=False
    )

    return explanation


# ============================================================
# Main Test
# ============================================================

if __name__ == "__main__":

    model = load_model()

    customer_data = pd.read_csv(
        "data/prediction_input.csv"
    )

    customer = customer_data.iloc[
        [0]
    ].copy()

    features = prepare_customer(
        customer
    )

    explanation = explain_customer(
        model,
        features
    )

    print()
    print("=" * 70)
    print("FinShield : SHAP Explanation")
    print("=" * 70)

    print(
        explanation[
            [
                "feature",
                "value",
                "shap_value"
            ]
        ].head(10).to_string(
            index=False
        )
    )

    print("=" * 70)