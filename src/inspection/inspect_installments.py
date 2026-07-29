from pathlib import Path
import pandas as pd

FILE_PATH = Path("Data/raw/installments_payments.csv")

df = pd.read_csv(FILE_PATH)

print("=" * 60)
print("INSTALLMENTS PAYMENTS DATASET")
print("=" * 60)

print("\nShape:")
print(df.shape)

print("\nFirst 5 Rows:")
print(df.head())

print("\nData Types:")
print(df.dtypes.value_counts())

print("\nDuplicate Previous Loan IDs:")
print(df["SK_ID_PREV"].duplicated().sum())

print("\nDuplicate Applicant IDs:")
print(df["SK_ID_CURR"].duplicated().sum())

print("\nTop Missing Values:")
missing = (
    df.isnull()
      .mean()
      .mul(100)
      .sort_values(ascending=False)
)

print(missing.head(20))