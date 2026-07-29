import pandas as pd

# Load dataset
df = pd.read_csv("Data/raw/bureau_balance.csv")

print("=" * 60)
print("BUREAU BALANCE DATASET")
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

# Duplicate Bureau IDs
print("\nDuplicate SK_ID_BUREAU:")
print(df["SK_ID_BUREAU"].duplicated().sum())

# First 5 Rows
print("\nFirst 5 Rows:")
print(df.head())