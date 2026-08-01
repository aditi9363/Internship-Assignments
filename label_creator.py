import pandas as pd

# Read the csv created in Q3
df = pd.read_csv("ALL_ACTIVITY_PATTERN.csv")

# Create label column
df["label"] = df["Pattern"].apply(
    lambda x: 0 if x in ["lying", "sitting"] else 1
)

# Save the updated DataFrame
df.to_csv("Master_DF.csv", index=False)

# Display first five rows
print(df.head())

# Display shape
print("\nShape:", df.shape)

# Count healthy & unhealthy labels
print("\nLabel Counts:")
print(df["label"].value_counts())
