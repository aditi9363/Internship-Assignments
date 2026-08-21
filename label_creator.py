import pandas as pd

# Read the combined dataset
df = pd.read_csv("ALL_ACTIVITY_PATTERN.csv")

# Display first five rows
print(df.head())

# Display shape
print("\nShape:", df.shape)

# Display the seven activity classes
print("\nActivity Classes:")
print(df["Pattern"].value_counts())

# Save the dataset
df.to_csv("Master_DF.csv", index=False)

print("\nMaster_DF.csv created successfully.")