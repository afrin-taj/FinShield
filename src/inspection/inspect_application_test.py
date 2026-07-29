import pandas as pd

# Load dataset
df = pd.read_csv("Data/raw/application_test.csv")

print("=" * 60)
print("APPLICATION TEST DATASET")
print("=" * 60)

# Shape
print("\nShape:")
print(df.shape)

# Columns
print("\nColumns:")
print(df.columns.tolist())

# Data Types
print("\nData Types:")
print(df.dtypes.value_counts())

# Missing Values
print("\nTop 20 Missing Values (%):")
print(
    (df.isnull().sum() / len(df) * 100)
    .sort_values(ascending=False)
    .head(20)
)

# Duplicate Applicants
print("\nDuplicate SK_ID_CURR:")
print(df["SK_ID_CURR"].duplicated().sum())

# First 5 Rows
print("\nFirst 5 Rows:")
print(df.head())