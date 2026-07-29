import pandas as pd

# Load dataset
df = pd.read_csv("Data/raw/credit_card_balance.csv")

print("=" * 60)
print("CREDIT CARD BALANCE DATASET")
print("=" * 60)

# Shape
print("\nShape:")
print(df.shape)

# Columns
print("\nColumns:")
print(df.columns.tolist())

# Data Types
print("\nData Types:")
print(df.dtypes)

# Missing Values
print("\nMissing Values (%):")
print((df.isnull().sum() / len(df) * 100).round(2).sort_values(ascending=False))

# Duplicate Previous Loan IDs
print("\nDuplicate SK_ID_PREV:")
print(df["SK_ID_PREV"].duplicated().sum())

# Duplicate Customer IDs
print("\nDuplicate SK_ID_CURR:")
print(df["SK_ID_CURR"].duplicated().sum())

# First five rows
print("\nFirst 5 Rows:")
print(df.head())