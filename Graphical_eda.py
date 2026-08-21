import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# Load Dataset
# ---------------------------------------------------------

df = pd.read_csv("Master_DF.csv")

print(df.head())
print("\nShape:", df.shape)

# ---------------------------------------------------------
# Features
# ---------------------------------------------------------

features = [
    "avg_rss12",
    "var_rss12",
    "avg_rss13",
    "var_rss13",
    "avg_rss23",
    "var_rss23"
]

# =========================================================
# 1. COUNT PLOT - ACTIVITY PATTERN
# =========================================================

plt.figure(figsize=(10, 5))

sns.countplot(
    data=df,
    x="Pattern",
    hue="Pattern"
)

plt.title("Number of Samples per Activity Pattern")
plt.xlabel("Activity Pattern")
plt.ylabel("Number of Samples")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# Interpretation:
# The count plot shows the number of observations belonging to
# each of the seven activity patterns.
# Most activities contain approximately 7,200 observations,
# while bending1 and bending2 contain fewer observations.
# Therefore, the multi-class dataset is not perfectly balanced.


# =========================================================
# 2. HISTOGRAMS WITH KDE
# =========================================================

for feature in features:

    plt.figure(figsize=(8, 5))

    sns.histplot(
        data=df,
        x=feature,
        kde=True,
        bins=30
    )

    plt.title(f"Histogram of {feature} with KDE")
    plt.xlabel(feature)
    plt.ylabel("Frequency")

    plt.tight_layout()
    plt.show()

# Interpretation:
# The histograms show the distribution of the six sensor features.
# The average RSS features are relatively concentrated around
# their central values, while the variance features are generally
# right-skewed with longer tails.
# KDE provides a smooth estimate of the underlying distribution.


# =========================================================
# 3. BOXPLOTS - FEATURES ACROSS ACTIVITY PATTERNS
# =========================================================

for feature in features:

    plt.figure(figsize=(10, 5))

    sns.boxplot(
        data=df,
        x="Pattern",
        y=feature
    )

    plt.title(
        f"{feature} across Activity Patterns"
    )

    plt.xlabel("Activity Pattern")
    plt.ylabel(feature)

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

# Interpretation:
# The boxplots compare the distribution of each sensor feature
# across all seven activity classes.
# Differences in medians, spread and outliers indicate that
# sensor measurements vary according to the activity being performed.
# These differences can provide useful information for
# multi-class classification.


# =========================================================
# 4. BOXPLOT - avg_rss12 ACROSS PATTERNS
# =========================================================

plt.figure(figsize=(10, 5))

sns.boxplot(
    data=df,
    x="Pattern",
    y="avg_rss12"
)

plt.title("avg_rss12 across Activity Patterns")
plt.xlabel("Activity Pattern")
plt.ylabel("avg_rss12")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# Interpretation:
# The boxplot compares avg_rss12 across the seven activity classes.
# Differences in the median and spread of avg_rss12 indicate
# that this sensor measurement changes depending on the activity.


# =========================================================
# 5. VIOLIN PLOTS - FEATURES ACROSS ACTIVITY PATTERNS
# =========================================================

for feature in features:

    plt.figure(figsize=(10, 5))

    sns.violinplot(
        data=df,
        x="Pattern",
        y=feature
    )

    plt.title(
        f"{feature} by Activity Pattern"
    )

    plt.xlabel("Activity Pattern")
    plt.ylabel(feature)

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

# Interpretation:
# Violin plots show the distribution and density of each
# sensor feature for all seven activity classes.
# The width of each violin indicates where observations are
# more concentrated.
# They can reveal differences in spread, skewness and
# multimodal distributions between activity classes.


# =========================================================
# 6. CORRELATION HEATMAP
# =========================================================

corr_matrix = df[features].corr()

plt.figure(figsize=(8, 6))

sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="coolwarm",
    center=0,
    fmt=".2f",
    linewidths=0.5
)

plt.title("Feature Correlation Heatmap")

plt.tight_layout()
plt.show()

# Interpretation:
# The correlation heatmap shows the linear relationships
# between the six sensor features.
# Positive values indicate that two features tend to increase
# together, while negative values indicate an inverse relationship.
# In the dataset, var_rss12 and var_rss13 have the strongest
# positive correlation, while avg_rss12 and var_rss12 have
# the strongest negative correlation.


# =========================================================
# 7. SCATTER PLOT - avg_rss12 vs avg_rss13
# =========================================================

plt.figure(figsize=(9, 7))

sns.scatterplot(
    data=df,
    x="avg_rss12",
    y="avg_rss13",
    hue="Pattern",
    alpha=0.6
)

plt.title(
    "Scatter Plot of avg_rss12 vs avg_rss13 by Activity Pattern"
)

plt.xlabel("Average RSS12")
plt.ylabel("Average RSS13")

plt.tight_layout()
plt.show()

# Interpretation:
# The scatter plot displays the relationship between avg_rss12
# and avg_rss13 while using different colours for the seven
# activity classes.
# Some activities may form partially separated regions,
# while others may overlap.
# This indicates that these two features alone may not be
# sufficient to perfectly distinguish all seven activities.


# =========================================================
# 8. PAIR PLOT
# =========================================================

# Sample 1000 observations from each activity class
sample_df = (
    df.groupby(
        "Pattern",
        group_keys=False
    )
    .sample(
        n=1000,
        random_state=42
    )
)

sns.pairplot(
    sample_df,
    vars=[
        "avg_rss12",
        "avg_rss13",
        "avg_rss23"
    ],
    hue="Pattern",
    diag_kind="kde"
)

plt.show()

# Interpretation:
# The pair plot shows pairwise relationships among the
# average RSS features for all seven activity classes.
# Different activity classes may form partially distinct
# clusters, but there can also be considerable overlap.
# This demonstrates why multiple sensor features are useful
# for multi-class classification.


# =========================================================
# 9. TIME-SERIES LINE PLOT
# =========================================================

COLS = [
    "time",
    "avg_rss12",
    "var_rss12",
    "avg_rss13",
    "var_rss13",
    "avg_rss23",
    "var_rss23"
]

# Example: walking recording
single_df = pd.read_csv(
    "Dataset/walking/dataset1.csv",
    comment="#",
    header=None,
    sep=r"[,\s]+",
    engine="python",
    usecols=range(7),
    names=COLS
)

plt.figure(figsize=(12, 6))

plt.plot(
    single_df["time"],
    single_df["avg_rss12"],
    label="avg_rss12"
)

plt.plot(
    single_df["time"],
    single_df["avg_rss13"],
    label="avg_rss13"
)

plt.plot(
    single_df["time"],
    single_df["avg_rss23"],
    label="avg_rss23"
)

plt.title(
    "Time Series of Average RSS Signals (Walking)"
)

plt.xlabel("Time")
plt.ylabel("Average RSS")

plt.legend()

plt.tight_layout()
plt.show()

# Interpretation:
# The time-series plot shows how the average RSS signals
# change over time during a walking activity.
# The signals fluctuate as the sensor measurements change
# during the activity.
# Time-series behaviour can help understand the nature of
# sensor measurements collected during human activities.

