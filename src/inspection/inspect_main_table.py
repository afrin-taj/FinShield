from pathlib import Path
import pandas as pd

file_path = Path("Data/raw/application_train.csv")

df = pd.read_csv(file_path)

print("Dataset Shape:")
print(df.shape)

print("\nFirst 5 Rows:")
print(df.head())

print("\nData Types:")
print(df.dtypes.value_counts())

print("\nTarget Distribution:")
print(df["TARGET"].value_counts())

print("\nTarget Percentage:")
print((df["TARGET"].value_counts(normalize=True) * 100).round(2))

print("\nDuplicate Applicant IDs:")
print(df["SK_ID_CURR"].duplicated().sum())

print("\nMissing Values:")
missing = df.isnull().mean().mul(100).sort_values(ascending=False)
print(missing.head(20))