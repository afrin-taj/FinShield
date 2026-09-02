import pandas as pd
from pathlib import Path


def main():

    results = [
        {
            "Threshold": 0.30,
            "Precision": 0.3810,
            "Recall": 0.1641,
            "F1 Score": 0.2294
        },
        {
            "Threshold": 0.25,
            "Precision": 0.3519,
            "Recall": 0.2302,
            "F1 Score": 0.2783
        },
        {
            "Threshold": 0.20,
            "Precision": 0.3121,
            "Recall": 0.3257,
            "F1 Score": 0.3187
        },
        {
            "Threshold": 0.15,
            "Precision": 0.2645,
            "Recall": 0.4538,
            "F1 Score": 0.3342
        }
    ]

    comparison = pd.DataFrame(results)

    results_dir = Path("results")

    results_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        results_dir /
        "threshold_comparison.csv"
    )

    comparison.to_csv(
        output_file,
        index=False
    )

    print()
    print("=" * 60)
    print("FinShield : Threshold Comparison")
    print("=" * 60)

    print()

    print(
        comparison.to_string(
            index=False
        )
    )

    print()

    print(
        f"Saved to : {output_file}"
    )


if __name__ == "__main__":
    main()