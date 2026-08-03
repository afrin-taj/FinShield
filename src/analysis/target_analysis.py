import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

from src.database import read_table
from src.utils import (
    log,
    dataframe_summary,
    start_timer,
    end_timer,
)

REPORTS_DIR = Path("reports/figures")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
#================
# Load Data
#================

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

#==========================
# Analyzing Target Variable
#=========================
def analyze_target(
    master: pd.DataFrame
):
    """
    Analyze target distribution.
    """

    log("Analyzing target variable...")

    target = master["TARGET"].value_counts()

    percentage = (
        master["TARGET"]
        .value_counts(normalize=True)
        * 100
    )

    summary = pd.DataFrame({
        "Count": target,
        "Percentage": percentage.round(2)
    })

    print("\nTarget Distribution\n")
    print(summary)

    return summary

#============================
# Plotting Target Distribution
#============================
def plot_target_distribution(
    master: pd.DataFrame
):
    """
    Plot target distribution.
    """

    log("Creating target distribution plot...")

    target = (
        master["TARGET"]
        .value_counts()
        .sort_index()
    )

    plt.figure(figsize=(6, 4))

    plt.bar(
        ["No Default", "Default"],
        target.values
    )

    plt.title("Target Distribution")
    plt.xlabel("Class")
    plt.ylabel("Number of Customers")

    plt.tight_layout()

    # Save the figure
    plt.savefig(
        REPORTS_DIR / "target_distribution.png",
        dpi=300,
        bbox_inches="tight"
    )

    # Display the figure
    plt.show()

#=================================
# Calculating Class Imbalance Ratio
#=================================
def imbalance_ratio(
    master: pd.DataFrame
):
    """
    Calculate class imbalance ratio.
    """

    majority = (
        master["TARGET"] == 0
    ).sum()

    minority = (
        master["TARGET"] == 1
    ).sum()

    ratio = majority / minority

    print()

    print(f"Class Imbalance Ratio : {ratio:.2f} : 1")

#================
# Main Function
#================
def main():

    start = start_timer(
        "EDA : Target Analysis"
    )

    master = load_data()

    analyze_target(master)

    imbalance_ratio(master)

    plot_target_distribution(master)

    end_timer(start)

    log("Pipeline completed successfully.")


if __name__ == "__main__":
    main()