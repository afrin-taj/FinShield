"""
FinShield Model Comparison
--------------------------
Compare the performance of all trained models.
"""

import pandas as pd
from pathlib import Path


def main():

    results = [

        {
            "Model": "Logistic Regression",
            "Accuracy": 0.9190,
            "Precision": 0.4679,
            "Recall": 0.0264,
            "F1 Score": 0.0500,
            "ROC-AUC": 0.7733
        },

        {
            "Model": "Random Forest",
            "Accuracy": 0.7598,
            "Precision": 0.1851,
            "Recall": 0.5805,
            "F1 Score": 0.2807,
            "ROC-AUC": 0.7507
        },

        {
            "Model": "XGBoost",
            "Accuracy": 0.8540,
            "Precision": 0.2645,
            "Recall": 0.4538,
            "F1 Score": 0.3342,
            "ROC-AUC": 0.7845
        },

        {
            "Model": "LightGBM",
            "Accuracy": 0.8545,
            "Precision": 0.2636,
            "Recall": 0.4475,
            "F1 Score": 0.3318,
            "ROC-AUC": 0.7831
        }

    ]

    comparison = pd.DataFrame(results)

    # Create results directory
    results_dir = Path("results")
    results_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save comparison
    output_file = (
        results_dir / "model_comparison.csv"
    )

    comparison.to_csv(
        output_file,
        index=False
    )

    print()
    print("=" * 70)
    print("FinShield : Model Comparison")
    print("=" * 70)

    print()

    print(
        comparison.to_string(
            index=False
        )
    )

    print()
    print(
        f"Comparison saved to : {output_file}"
    )


if __name__ == "__main__":
    main()