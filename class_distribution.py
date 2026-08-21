import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Master_DF.csv")

print("=" * 60)
print("MULTI-CLASS DISTRIBUTION")
print("=" * 60)

class_counts = df["Pattern"].value_counts()

print(class_counts)

print("\nNumber of classes:", df["Pattern"].nunique())

print("\nClass names:")
print(sorted(df["Pattern"].unique()))

# Plot class distribution
plt.figure(figsize=(10, 5))

sns.countplot(
    data=df,
    x="Pattern",
    hue="Pattern"
)

plt.title("Distribution of Activity Classes")
plt.xlabel("Activity Pattern")
plt.ylabel("Number of Samples")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()