# ============================================================
# Bureau Balance Feature Configuration
# ============================================================

# Numeric aggregation configuration
NUMERIC_AGGREGATIONS = {
    "MONTHS_BALANCE": ["count", "min", "max"]
}

# Categorical columns
CATEGORICAL_COLUMNS = [
    "STATUS"
]

# Output configuration
OUTPUT_TABLE = "feature.bureau_balance_features"
OUTPUT_FILE = "bureau_balance_features.csv"