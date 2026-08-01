import pandas as pd
from loader import load_dataset

df = load_dataset()

# ----------------------Shape----------------------------
print("=" * 60)
print("Dataset Shape:")
print("=" * 60)
print(df.shape)

# Interpretation :
# The dataset contains 42,239 rows & 8 columns indicating a large collection of sensor observations.
# The size of the dataset is sufficient for performing meaningful exploratory data analysis.

# --------------------Data Types--------------------------
print("\n" + "=" * 60)
print("Data Types:")
print("=" * 60)
print(df.dtypes)

# Interpretation : 
# The sensor measurement columns are stored as numeric(int64 & float64) making them suitable for statistical analysis.
# The Pattern column is of type object, representing the activity category for each observation.

# --------------------First Rows--------------------------
print("\n" + "=" * 60)
print("First 5 Rows:")
print("=" * 60)
print(df.head())

# Interpretation :
# The first 5 rows confirm that the dataset has been loaded correctly with the expected column names & values.
# They provide a quick preview of the data structure & the initial activity records.

# --------------------Last Rows----------------------------
print("\n" + "=" * 60)
print("Last 5 Rows:")
print("=" * 60)
print(df.tail())

# Interpretation : 
# The last 5 rows confirm that the dataset has been read completely from beginning to end.
# They also provide a preview of the final records in the dataset.

# --------------------Summary Statistics---------------------
print("\n" + "=" * 60)
print("Summary Statistics:")
print("=" * 60)
print(df.describe())

# Interpretation : 
# The summary statistics provide information about the distribution of each numeric feature,
# including average, variability, minimum, maximum, and quartile values.
# These statistics help in understanding the overall characteristics & spread of the sensor data.

# ---------------------Missing Values--------------------------
print("\n" + "=" * 60)
print("Missing Values:")
print("=" * 60)
print(df.isna().sum())

# Interpretation :
# All columns contain 0 missing values, indicating that the dataset is complete.
# No missing-value preprocessing is required before further analysis.

# --------------------Duplicate Rows-----------------------------
print("\n" + "=" * 60)
print("Duplicate Rows:")
print("=" * 60)
print(df.duplicated().sum())

# Interpretation :
# The dataset contain 3,359 rows meaning some observations have identical values across all columns.
# These duplicates should be reviewed to determine whether they are valid repeated measurements or should be removed before further analysis.