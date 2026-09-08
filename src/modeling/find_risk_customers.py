import pandas as pd
import joblib

from src.config import MODELS_DIR
from src.modeling.predict import prepare_features, predict

df = pd.read_csv("data/final/clean_master_dataset.csv")

model = joblib.load(MODELS_DIR / "xgboost_model.pkl")
feature_names = joblib.load(MODELS_DIR / "xgboost_features.pkl")

results = []

for start in range(0, len(df), 1000):
    batch = df.iloc[start:start + 1000].copy()

    features = prepare_features(batch, feature_names)
    probabilities, predictions = predict(model, features)

    for customer_id, probability in zip(
        batch["SK_ID_CURR"], probabilities
    ):
        results.append({
            "SK_ID_CURR": customer_id,
            "default_probability": probability
        })

    medium_count = sum(
        0.10 <= x["default_probability"] < 0.20
        for x in results
    )

    if medium_count >= 10:
        break

results_df = pd.DataFrame(results)

medium = results_df[
    (results_df["default_probability"] >= 0.10) &
    (results_df["default_probability"] < 0.20)
]

print("\nMEDIUM RISK CUSTOMERS")
print("=====================")
print(
    medium.sort_values(
        "default_probability",
        ascending=False
    ).head(10).to_string(index=False)
)