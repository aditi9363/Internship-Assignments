import pandas as pd

df = pd.read_csv("Master_DF.csv")

# ========================================================
# Pattern Distribution
# ========================================================
print("=" * 60)
print("PATTERN DISTRIBUTION")
print("=" * 60)

print(df["Pattern"].value_counts())

# Interpretation : 
# The Pattern Distribution shows the number of observations for each activity.
# Most activities contain approximately 7,200 observations, while bending1 & bending2 contain fewer observations,
# indicating that the dataset is not perfectly balanced across all activity classes.

# =========================================================
# Label Distribution
# =========================================================
print("\n" + "=" * 60)
print("LABEL DISTRIBUTION")
print("=" * 60)

print(df["label"].value_counts())

# Interpretation : 
# The label distribution shows the number of observations in each class(0 & 1).
# If one label has substantially more observations than the other, 
# the dataset is imbalanced with respect to the binary classification labels.

# =========================================================
# Correlation Matrix
# =========================================================
print("\n" + "=" * 60)
print("CORRELATION MATRIX")
print("=" * 60)

sensor_features = [
    "avg_rss12",
    "var_rss12",
    "avg_rss13",
    "var_rss13",
    "avg_rss23",
    "var_rss23"
]

corr_matrix = df[sensor_features].corr()
print(corr_matrix)

# Interpretation : 
# The correlation matrix measures the linear relationship between the six sensor features.
# Correlation values close to 1 indicate a strong positive relationship,
# values close to -1 indicate a strong negative relationship,
# values near 0 indicate little or no linear relationship.

# Strongest Positive Correlation
# The strongest positive correlation is between var_rss12 & var_rss13 with a correlation value of 0.5455.
# This indicates a moderate positive linear relationship, 
# meaning these two sensor variance features tend to increase together.

# Strongest Negative Correlation
# The strongest negative correlation is between avg_rss12 & var_rss12 with a correlation value of -0.3858.
# This indicates a moderate negative linear relationship,
# meaning that as one feature increases, the other tends to decrease.