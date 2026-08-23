import pandas as pd

from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_val_score
)

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC


# ============================================================
# Load Dataset
# ============================================================

df = pd.read_csv("Master_DF.csv")

print("Original Dataset Shape:", df.shape)


# ============================================================
# Features and Multiclass Target
# ============================================================

features = [
    "avg_rss12",
    "var_rss12",
    "avg_rss13",
    "var_rss13",
    "avg_rss23",
    "var_rss23"
]

X = df[features]

# Pattern contains the 7 activity classes
y = df["Pattern"]


print("\nTarget Classes:")
print(sorted(y.unique()))

print("\nClass Distribution:")
print(y.value_counts())


# ============================================================
# Stratified Sampling
# ============================================================

X_sample, _, y_sample, _ = train_test_split(
    X,
    y,
    train_size=15000,
    stratify=y,
    random_state=42
)


print("\nSample Shape:", X_sample.shape)

print("\nSample Class Distribution:")
print(y_sample.value_counts())


# ============================================================
# Train-Test Split
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X_sample,
    y_sample,
    test_size=0.25,
    stratify=y_sample,
    random_state=42
)


print("\nTraining Shape:", X_train.shape)
print("Testing Shape:", X_test.shape)


# ============================================================
# 5-Fold Stratified Cross-Validation
# ============================================================

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


# ============================================================
# Define Models
# ============================================================

models = {

    "Logistic Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(
            max_iter=1000
        ))
    ]),

    "Gaussian Naive Bayes": Pipeline([
        ("scaler", StandardScaler()),
        ("model", GaussianNB())
    ]),

    "KNN": Pipeline([
        ("scaler", StandardScaler()),
        ("model", KNeighborsClassifier(
            n_neighbors=5
        ))
    ]),

    "Decision Tree": DecisionTreeClassifier(
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        random_state=42
    ),

    "Gradient Boosting": GradientBoostingClassifier(
        random_state=42
    ),

    "SVM": Pipeline([
        ("scaler", StandardScaler()),
        ("model", SVC(
            kernel="rbf",
            probability=True,
            random_state=42
        ))
    ])
}


# ============================================================
# Perform 5-Fold Stratified Cross-Validation
# ============================================================

results = []


for name, model in models.items():

    scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring="f1_weighted"
    )

    mean_f1 = scores.mean()
    std_f1 = scores.std()

    print("\n============================================================")
    print(name)
    print("============================================================")

    print("F1 Scores for 5 folds:")
    print(scores)

    print("Mean F1 Score:", round(mean_f1, 4))

    print("Standard Deviation:", round(std_f1, 4))


    results.append({
        "Model": name,
        "Fold 1 F1": scores[0],
        "Fold 2 F1": scores[1],
        "Fold 3 F1": scores[2],
        "Fold 4 F1": scores[3],
        "Fold 5 F1": scores[4],
        "Mean F1": mean_f1,
        "Std F1": std_f1
    })


# ============================================================
# Cross-Validation Comparison Table
# ============================================================

results_df = pd.DataFrame(results)


print("\n\n============================================================")
print("5-FOLD STRATIFIED CROSS-VALIDATION RESULTS")
print("============================================================")


print(
    results_df[
        [
            "Model",
            "Mean F1",
            "Std F1"
        ]
    ].to_string(index=False)
)


# ============================================================
# Sort Models by Mean F1
# ============================================================

cv_comparison = results_df.sort_values(
    by="Mean F1",
    ascending=False
)


print("\n\n============================================================")
print("Models Ranked by Mean F1 Score")
print("============================================================")

print(
    cv_comparison[
        [
            "Model",
            "Mean F1",
            "Std F1"
        ]
    ].to_string(index=False)
)


# ============================================================
# Best Model Based on Cross-Validation
# ============================================================

best_model_name = cv_comparison.iloc[0]["Model"]

best_mean_f1 = cv_comparison.iloc[0]["Mean F1"]

best_std_f1 = cv_comparison.iloc[0]["Std F1"]


print("\n\n============================================================")
print("Best Model Based on 5-Fold Cross-Validation")
print("============================================================")

print("Best Model:", best_model_name)

print(
    "Mean F1:",
    round(best_mean_f1, 4)
)

print(
    "Standard Deviation:",
    round(best_std_f1, 4)
)


# ============================================================
# Save Cross-Validation Results
# ============================================================

cv_comparison.to_csv(
    "multiclass_cross_validation_results.csv",
    index=False
)

print(
    "\nCross-validation results saved as "
    "multiclass_cross_validation_results.csv"
)

# Mean F1 = 0.7768 and Standard Deviation = 0.0083.
# The mean F1 represents the average model performance across the 5 folds,
# while the standard deviation shows how much the performance varies between folds.
# 5-fold stratified cross-validation is more trustworthy than a single train-test
# split because the model is evaluated on five different validation sets while
# maintaining class proportions. The small standard deviation indicates that
# Random Forest performs consistently across the different folds.