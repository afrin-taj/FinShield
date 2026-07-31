NUMERIC_AGGREGATIONS = {
    "MONTHS_BALANCE": ["count", "min", "max"],
    "CNT_INSTALMENT": ["mean", "max"],
    "CNT_INSTALMENT_FUTURE": ["mean", "max"],
    "SK_DPD": ["mean", "max", "sum"],
    "SK_DPD_DEF": ["mean", "max", "sum"],
}

CATEGORICAL_COLUMNS = [
    "NAME_CONTRACT_STATUS"
]

OUTPUT_TABLE = "feature.pos_cash_balance_features"

OUTPUT_FILE = "pos_cash_balance_features.csv"