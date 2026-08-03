from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.database import read_table
from src.utils import (
    log,
    dataframe_summary,
    start_timer,
    end_timer,
)
#===========================
#Create Reports Directory for Figures
#===========================
REPORTS_DIR = Path("reports/figures")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

#===========================
# Load Data

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

FEATURES = [
    "TARGET",
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "AMT_GOODS_PRICE",
    "DAYS_BIRTH",
    "DAYS_EMPLOYED",
]

#===========================
# Correlation Analysis
#===========================
def correlation_analysis(
    master: pd.DataFrame
):
    """
    Compute correlation matrix.
    """

    log("Calculating correlation matrix...")

    correlation = (
        master[FEATURES]
        .corr()
    )

    print("\nCorrelation Matrix\n")

    print(
        correlation.round(2)
    )

    return correlation

#===========================
# Plotting Heatmap
#===========================
def plot_heatmap(
    correlation: pd.DataFrame
):
    """
    Plot correlation heatmap.
    """

    log("Creating correlation heatmap...")

    plt.figure(figsize=(8,6))

    plt.imshow(
        correlation,
        cmap="coolwarm",
        interpolation="nearest"
    )

    plt.colorbar()

    plt.xticks(
        range(len(correlation.columns)),
        correlation.columns,
        rotation=90
    )

    plt.yticks(
        range(len(correlation.columns)),
        correlation.columns
    )

    plt.tight_layout()

    plt.savefig(
        REPORTS_DIR / "correlation_heatmap.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

#===========================
# Display Strong Correlations
#===========================
def strong_correlations(
    correlation: pd.DataFrame
):
    """
    Display strong correlations.
    """

    log("Finding strong correlations...")

    print()

    for column in correlation.columns:

        for index in correlation.index:

            value = correlation.loc[index, column]

            if (
                abs(value) >= 0.7
                and index != column
            ):

                print(
                    f"{index} <-> {column} : {value:.2f}"
                )

#=================
#Main Function
#=================
def main():

    start = start_timer(
        "EDA : Correlation Analysis"
    )

    master = load_data()

    correlation = correlation_analysis(
        master
    )

    plot_heatmap(
        correlation
    )

    strong_correlations(
        correlation
    )

    end_timer(start)

    log("Pipeline completed successfully.")


if __name__ == "__main__":
    main()

