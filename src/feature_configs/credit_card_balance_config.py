NUMERIC_AGGREGATIONS = {
    "AMT_BALANCE": ["mean", "max", "sum"],
    "AMT_CREDIT_LIMIT_ACTUAL": ["mean", "max"],
    "AMT_PAYMENT_CURRENT": ["mean", "max", "sum"],
    "AMT_PAYMENT_TOTAL_CURRENT": ["mean", "max", "sum"],
    "AMT_RECEIVABLE_PRINCIPAL": ["mean", "max"],
    "AMT_TOTAL_RECEIVABLE": ["mean", "max"],
    "SK_DPD": ["mean", "max", "sum"],
    "SK_DPD_DEF": ["mean", "max", "sum"],
}

CATEGORICAL_COLUMNS = [
    "NAME_CONTRACT_STATUS"
]

OUTPUT_TABLE = "feature.credit_card_balance_features"

OUTPUT_FILE = "credit_card_balance_features.csv"