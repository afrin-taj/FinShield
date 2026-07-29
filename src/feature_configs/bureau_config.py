"""
Configuration for Bureau Feature Engineering
"""

# Numeric Aggregations
NUMERIC_AGGREGATIONS = {

    "SK_ID_BUREAU": ["count"],

    "AMT_CREDIT_SUM": [
        "sum",
        "mean",
        "max",
        "min",
        "median",
        "std"
    ],

    "AMT_CREDIT_SUM_DEBT": [
        "sum",
        "mean",
        "max",
        "min",
        "std"
    ],

    "AMT_CREDIT_SUM_OVERDUE": [
        "sum",
        "mean",
        "max"
    ],

    "AMT_CREDIT_SUM_LIMIT": [
        "sum",
        "mean",
        "max"
    ],

    "AMT_ANNUITY": [
        "sum",
        "mean",
        "max"
    ],

    "DAYS_CREDIT": [
        "mean",
        "min",
        "max"
    ],

    "DAYS_CREDIT_ENDDATE": [
        "mean",
        "min",
        "max"
    ],

    "DAYS_ENDDATE_FACT": [
        "mean"
    ],

    "DAYS_CREDIT_UPDATE": [
        "mean"
    ],

    "CREDIT_DAY_OVERDUE": [
        "sum",
        "mean",
        "max"
    ],

    "CNT_CREDIT_PROLONG": [
        "sum",
        "mean",
        "max"
    ]
}

# Categorical Columns
CATEGORICAL_COLUMNS = [
    "CREDIT_ACTIVE",
    "CREDIT_TYPE",
    "CREDIT_CURRENCY"
]

# ==========================
# Ratio Features
# ==========================

RATIO_FEATURES = {

    "bureau_debt_to_credit_ratio": (
        "bureau_amt_credit_sum_debt_sum",
        "bureau_amt_credit_sum_sum"
    ),

    "bureau_overdue_to_credit_ratio": (
        "bureau_amt_credit_sum_overdue_sum",
        "bureau_amt_credit_sum_sum"
    ),

    "bureau_avg_credit_per_loan": (
        "bureau_amt_credit_sum_sum",
        "bureau_total_loans"
    ),

    "bureau_avg_debt_per_loan": (
        "bureau_amt_credit_sum_debt_sum",
        "bureau_total_loans"
    )

}

# ==========================
# Output Configuration
# ==========================

OUTPUT_TABLE = "bureau_features"

OUTPUT_FILE = "bureau_features.csv"