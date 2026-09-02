"""
Machine Learning - Random Forest
--------------------------------------
Train and evaluate a Random Forest model.
"""

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from src.config import (
    PROCESSED_DATA_DIR,
    MODELS_DIR
)

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

from src.utils import (
    log,
    dataframe_summary,
    start_timer,
    end_timer
)

# ==========================
# Load Data
# ==========================
def load_data():
    """
    Load train and test datasets.
    """

    log("Loading train and test datasets...")

    X_train = joblib.load(
        MODELS_DIR / "X_train.pkl"
    )

    X_test = joblib.load(
        MODELS_DIR / "X_test.pkl"
    )

    y_train = joblib.load(
        MODELS_DIR / "y_train.pkl"
    )

    y_test = joblib.load(
        MODELS_DIR / "y_test.pkl"
    )

    print()

    print(f"X Train : {X_train.shape}")
    print(f"X Test  : {X_test.shape}")
    print(f"y Train : {y_train.shape}")
    print(f"y Test  : {y_test.shape}")

    return (
        X_train,
        X_test,
        y_train,
        y_test
    )

# ==========================
# Encode Features
# ==========================
def encode_features(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame
):
    """
    One-Hot Encode categorical columns.
    """

    log("Encoding categorical features...")

    categorical_columns = X_train.select_dtypes(
        include=["object", "string"]
    ).columns.tolist()

    print("\nCategorical Columns\n")
    print(categorical_columns)

    X_train = pd.get_dummies(
        X_train,
        columns=categorical_columns,
        drop_first=True,
        dtype="uint8"
    )

    X_test = pd.get_dummies(
        X_test,
        columns=categorical_columns,
        drop_first=True,
        dtype="uint8"
    )

    # Make both datasets have identical columns
    X_train, X_test = X_train.align(
        X_test,
        join="left",
        axis=1,
        fill_value=0
    )

    print()
    print(f"Encoded X Train : {X_train.shape}")
    print(f"Encoded X Test  : {X_test.shape}")

    return (
        X_train,
        X_test
    )

# ==========================
# Train Model
# ==========================
def train_model(
    X_train,
    y_train
):
    """
    Train Random Forest model.
    """

    log("Training Random Forest model...")

    model = RandomForestClassifier(
    n_estimators=300,
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=5,
    max_features="sqrt",
    class_weight="balanced_subsample",
    random_state=42,
    n_jobs=-1
)
    model.fit(
        X_train,
        y_train
    )

    log("Model training completed.")

    return model

# ==========================
# Predict
# ==========================
def predict(
    model,
    X_test
):
    """
    Make predictions.
    """

    log("Making predictions...")

    y_prob = model.predict_proba(X_test)[:, 1]

    threshold = 0.40

    y_pred = (y_prob >= threshold).astype(int)

    y_prob = model.predict_proba(X_test)[:, 1]

    log("Predictions completed.")

    return (
        y_pred,
        y_prob
    )

# ==========================
# Evaluate Model
# ==========================
def evaluate_model(
    y_test,
    y_pred,
    y_prob
):
    """
    Evaluate Random Forest model.
    """

    log("Evaluating model...")

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    precision = precision_score(
        y_test,
        y_pred
    )

    recall = recall_score(
        y_test,
        y_pred
    )

    f1 = f1_score(
        y_test,
        y_pred
    )

    roc_auc = roc_auc_score(
        y_test,
        y_prob
    )

    print("\nModel Performance\n")

    print(f"Accuracy  : {accuracy:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1 Score  : {f1:.4f}")
    print(f"ROC-AUC   : {roc_auc:.4f}")

    print("\nConfusion Matrix\n")
    print(
        confusion_matrix(
            y_test,
            y_pred
        )
    )

    print("\nClassification Report\n")
    print(
        classification_report(
            y_test,
            y_pred
        )
    )

# ==========================
# Save Model
# ==========================
def save_model(
    model
):
    """
    Save trained model and scaler.
    """

    log("Saving model...")

    joblib.dump(
        model,
        MODELS_DIR / "random_forest_model.pkl"
    )

    log("Model saved successfully.")

#=========================
#Main Function
#=========================
def main():

    start = start_timer(
        "Machine Learning : Random Forest"
    )

    X_train, X_test, y_train, y_test = load_data()
    X_train, X_test = encode_features(
    X_train,
    X_test
    )

    model = train_model(
    X_train,
    y_train
    )

    y_pred, y_prob = predict(
    model,
    X_test
    )

    evaluate_model(
    y_test,
    y_pred,
    y_prob
    )

    save_model(
    model
    )
    
    end_timer(start)

    log("Pipeline completed successfully.")


if __name__ == "__main__":
    main()