import pandas as pd

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression 
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier 
from sklearn.svm import SVC

df = pd.read_csv("Master_DF.csv")

features = [
    "avg_rss12",
    "var_rss12",
    "avg_rss13",
    "var_rss13",
    "avg_rss23",
    "var_rss23"
]

X = df[features]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    stratify=y,
    random_state=42
)

# -----------------------------------------------------
# Define 5-fold Stratified Cross-Validation
# -----------------------------------------------------
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

models = {
    "Logistics Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000))
    ]),

    "Naive Bayes": Pipeline([
        ("scaler", StandardScaler()),
        ("model", GaussianNB())
    ]),

    "KNN": Pipeline([
        ("scaler", StandardScaler()),
        ("model", KNeighborsClassifier())
    ]),

    "Decision Tree": DecisionTreeClassifier(
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
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

# --------------------------------------------------------
# Perform 5-fold Stratified Cross-Validation
# --------------------------------------------------------
results = []

for name, model in models.items():
    scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring="f1"
    )

    mean_f1 = scores.mean()
    std_f1 = scores.std()

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    print("F1 Scores for 5 folds:", scores)
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

# ----------------------------------------------------
# Create comparison table
# ----------------------------------------------------
results_df = pd.DataFrame(results)

print("\n\n")
print("=" * 80)
print("CROSS-VALIDATION RESULTS")
print("=" * 80)

print(
    results_df[
        ["Model", "Mean F1", "Std F1"]
    ].to_string(index=False)
)

# Mean F1 shows average performance across the 5 folds, while
# standard deviation shows performance consistency. Using multiple
# folds gives a more reliable estimate than a single train-test split.