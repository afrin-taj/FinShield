NUMERIC_AGGREGATIONS = {
    "AMT_APPLICATION": ["mean", "max", "sum"],
    "AMT_CREDIT": ["mean", "max", "sum"],
    "AMT_ANNUITY": ["mean", "max", "sum"],
    "AMT_GOODS_PRICE": ["mean", "max", "sum"],
    "CNT_PAYMENT": ["mean", "max"],
    "DAYS_DECISION": ["min", "max", "mean"]
}

CATEGORICAL_COLUMNS = [
    "NAME_CONTRACT_STATUS",
    "NAME_CONTRACT_TYPE"
]

OUTPUT_TABLE = "feature.previous_application_features"

OUTPUT_FILE = "previous_application_features.csv"