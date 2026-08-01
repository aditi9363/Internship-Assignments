import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Master_DF.csv")

df["label"] = df["label"].map({
    0: "Unhealthy",
    1: "Healthy"
})

print(df.head())

print("\nShape:", df.shape)

#-----------------------------------------------------
# Count Plot (Pattern)
# ----------------------------------------------------
plt.figure(figsize=(10,5))

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

# Interpretation : 
# The count plot shows the number of samples for each activity pattern.
# Most activities contain around 7,200 samples, while bending1 & bending2 contain fewer samples.
# This indicates that the dataset is not perfectly balanced across all activity patterns.

#------------------------------------------------------
# Count Plot (Label)
# -----------------------------------------------------
plt.figure(figsize=(6,5))

sns.countplot(
    data=df,
    x="label",
    hue="label"
)

plt.title("Number of Samples by Health Label")
plt.xlabel("Health Label")
plt.ylabel("Number of Samples")

plt.tight_layout()

plt.show()

# Interpretation :
# The count plot compares the number of healthy & unhealthy samples.
# The healthy class contains more samples than unhealthy class because five activities were labelled as healthy,
# while only lying & sitting were labelled as unhealthy.

#--------------------------------------------------------
# Histograms with KDE
# -------------------------------------------------------
features = [
    "avg_rss12",
    "var_rss12",
    "avg_rss13",
    "var_rss13",
    "avg_rss23",
    "var_rss23"
]

for feature in features:
    plt.figure(figsize=(8,5))

    sns.histplot(
        data=df,
        x=feature,
        kde=True,
        bins=30,
        color="skyblue"
    )

    plt.title(f"Histogram of {feature} with KDE")
    plt.xlabel(feature)
    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.show()

# Interpretation :
# The average RSS features (avg_rss12, avg_rss13, and avg_rss23) are approximately symmetric and
# resemble a normal distribution, although avg_rss23 shows a slight right skew.
# The variance features (var_rss12, var_rss13, and var_rss23) are clearly right skewed,
# with most observations concentrated at lower values & a long tail extending toward higher values.

# -------------------------------------------------------
# Boxplots grouped by Health Label
# -------------------------------------------------------
for feature in features:
    plt.figure(figsize=(6,4))

    sns.boxplot(
        data=df,
        x="label",
        y=feature
    )

    plt.title(f"{feature} grouped by Health Label")
    plt.xlabel("Health Label")
    plt.ylabel(feature)

    plt.tight_layout()

    plt.show()

# ------------------------------------------------------
# One feature across Patterns
# ------------------------------------------------------
plt.figure(figsize=(10,5))

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

# Interpretation :
# The variance-based features (var_rss12, var_rss13 and var_rss23) contain the highest number of outliers.
# Among them, var_rss12 shows the largest concentration of extreme values.
# The average RSS features (avg_rss12, avg_rss13 and avg_rss23) have comparatively fewer outliers.
# These outliers indicate unusual sensor readings or high variability during certain human activities.

# ------------------------------------------------------------
# Violin Plots
# ------------------------------------------------------------
for feature in features:
    plt.figure(figsize=(6,4))

    sns.violinplot(
        data=df,
        x="label",
        y=feature
    )

    plt.title(f"{feature} by Health Label")

    plt.xlabel("Health Label")
    plt.ylabel(feature)

    plt.tight_layout()

    plt.show()

# A violin plot provides more information than a box plot because its displays the full distribution 
# (density) of the data, in addition to the median & quartiles.
# The width of the violin represents where data points are more concentrated.
# It can also reveal multimodal distributions (multiple peaks),skewness & variations in data 
# that a box plot cannot show.

# -----------------------------------------------------------
# Correlation Heatmap
# -----------------------------------------------------------
corr_matrix = df[features].corr()

plt.figure(figsize=(8,6))

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

# Interpretation :
# The correlation heatmap is a visual representation of the correlation matrix calculated in Q6
# The annotated values in the heatmap match the numerical correlation coefficients computed earlier.
# The heatmap visually confirms that var_rss12 & var_rss13 have the strongest positive correlation(0.5455),
# while avg_rss12 & var_rss12 have the strongest negative correlation (-0.3858).
# Thus, the heatmap makes it easier to identify strong, weak, positive, and negative relationships 
# among the sensor features.

# -------------------------------------------------------
# Scatter Plot
# -------------------------------------------------------
plt.figure(figsize=(8,6))

sns.scatterplot(
    data=df,
    x="avg_rss12",
    y="avg_rss13",
    hue="label",
    alpha=0.6
)

plt.title("Scatter Plot of avg_rss12 vs avg_rss13")
plt.xlabel("Average RSS12")
plt.ylabel("Average RSS13")

plt.tight_layout()
plt.show()

# -------------------------------------------------------
# Pair Plot
# -------------------------------------------------------
sample_df = (
    df.groupby("label", group_keys=False).sample(n=1000, random_state=42)
)

sns.pairplot(
    sample_df,
    vars=["avg_rss12", "avg_rss13", "avg_rss23"],
    hue="label",
    diag_kind="kde"
)
plt.show()

# Interpretation : 
# The Healthy & Unhealthy classes show partial separation in both the scatter plot & pair plot.
# Although there is considerable overlap between the two classes, some feature combinations form distinct clusters.
# The average RSS features provide useful information for distinguishing the classes, 
# but they are not sufficient to completely separate Healthy and Unhealthy samples.

# ----------------------------------------------------
# Time Series Line Plot
# ----------------------------------------------------
COLS = [
    "time",
    "avg_rss12",
    "var_rss12",
    "avg_rss13",
    "var_rss13",
    "avg_rss23",
    "var_rss23"
]

single_df = pd.read_csv(
    "Dataset/walking/dataset1.csv",
    comment="#",
    header=None,
    sep=r"[,\s]+",
    engine="python",
    usecols=range(7),
    names=COLS
)

plt.figure(figsize=(12,6))

plt.plot(single_df["time"], single_df["avg_rss12"], label="avg_rss12")
plt.plot(single_df["time"], single_df["avg_rss13"], label="avg_rss13")
plt.plot(single_df["time"], single_df["avg_rss23"], label="avg_rss23")

plt.title("Time Series of Average RSS Signals (Walking)")
plt.xlabel("Time")
plt.ylabel("Average RSS")

plt.tight_layout()
plt.show()