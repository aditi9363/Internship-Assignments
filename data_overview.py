import pandas as pd

df = pd.read_csv("Master_DF.csv")

print("=" * 60)
print("DATASET SHAPE")
print("=" * 60)
print(df.shape)

print("\n" + "=" * 60)
print("DATA TYPES")
print("=" * 60)
print(df.dtypes)

print("\n" + "=" * 60)
print("FIRST 5 ROWS")
print("=" * 60)
print(df.head())

print("\n" + "=" * 60)
print("LAST 5 ROWS")
print("=" * 60)
print(df.tail())

print("\n" + "=" * 60)
print("SUMMARY STATISTICS")
print("=" * 60)
print(df.describe())

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)
print(df.isna().sum())

print("\n" + "=" * 60)
print("DUPLICATE ROWS")
print("=" * 60)
print(df.duplicated().sum())

print("\n" + "=" * 60)
print("ACTIVITY CLASS DISTRIBUTION")
print("=" * 60)
print(df["Pattern"].value_counts())