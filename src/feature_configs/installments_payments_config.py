NUMERIC_AGGREGATIONS = {
    "AMT_INSTALMENT": ["mean", "max", "sum"],
    "AMT_PAYMENT": ["mean", "max", "sum"],
    "DAYS_INSTALMENT": ["min", "max", "mean"],
    "DAYS_ENTRY_PAYMENT": ["min", "max", "mean"],
}

OUTPUT_TABLE = "feature.installments_payments_features"

OUTPUT_FILE = "installments_payments_features.csv"