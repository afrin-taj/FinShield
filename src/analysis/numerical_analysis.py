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

NUMERICAL_FEATURES = [
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "AMT_GOODS_PRICE",
    "DAYS_BIRTH",
    "DAYS_EMPLOYED",
]

#===========================
# Load Data
#===========================
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

#===========================
#Numerical Summary
#===========================
def numerical_summary(
    master: pd.DataFrame
):
    """
    Display summary statistics.
    """

    log("Generating numerical summary...")

    print()

    print(
        master[NUMERICAL_FEATURES]
        .describe()
        .T
    )

#===========================
#Plotting Histograms
#===========================
def plot_histograms(
    master: pd.DataFrame
):
    """
    Plot histograms.
    """

    log("Creating histograms...")

    for column in NUMERICAL_FEATURES:

        plt.figure(figsize=(8,4))

        master[column].hist(
            bins=40
        )

        plt.title(column)

        plt.tight_layout()

        plt.savefig(
            REPORTS_DIR / f"{column}_histogram.png",
            dpi=300,
            bbox_inches="tight"
        )

        plt.show()

#===========================
#Plotting boxplots
#===========================
def plot_boxplots(
    master: pd.DataFrame
):
    """
    Plot boxplots.
    """

    log("Creating boxplots...")

    for column in NUMERICAL_FEATURES:

        plt.figure(figsize=(8,2))

        plt.boxplot(
            master[column],
            orientation="horizontal"
        )

        plt.title(column)

        plt.tight_layout()

        plt.savefig(
            REPORTS_DIR / f"{column}_boxplot.png",
            dpi=300,
            bbox_inches="tight"
        )

        plt.show()

#===========================
#Outlier Detection
#===========================
def outlier_summary(
    master: pd.DataFrame
):
    """
    Detect outliers using IQR.
    """

    log("Detecting outliers...")

    results = []

    for column in NUMERICAL_FEATURES:

        q1 = master[column].quantile(0.25)
        q3 = master[column].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = (
            (master[column] < lower)
            |
            (master[column] > upper)
        ).sum()

        results.append(
            {
                "Feature": column,
                "Outliers": outliers
            }
        )

    print()

    print(
        pd.DataFrame(results)
    )

#===========================
#Main Function
#===========================
def main():

    start = start_timer(
        "EDA : Numerical Analysis"
    )

    master = load_data()

    numerical_summary(master)

    plot_histograms(master)

    plot_boxplots(master)

    outlier_summary(master)

    end_timer(start)

    log("Pipeline completed successfully.")


if __name__ == "__main__":
    main()   