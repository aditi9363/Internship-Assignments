import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve

df = pd.read_csv("Master_DF.csv")

print("Original Dataset Shape:", df.shape)

print("\nDataset Columns")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

# =====================================================
# Select features and target
# =====================================================

features = [
    "avg_rss12",
    "var_rss12",
    "avg_rss13",
    "var_rss13",
    "avg_rss23",
    "var_rss23"
]
X = df[features]

y = df["Pattern"]

print("\nFeatures:")
print(features)

print("\nTarget Classes:")
print(y.unique())

print("\nClass Distribution:")
print(y.value_counts())

# ============================================================
# Q2 - Stratified Sampling
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

# ===========================================================
# Train/Test Split
# ===========================================================
X_train, X_test, y_train, y_test = train_test_split(
    X_sample,
    y_sample,
    test_size=0.25,
    stratify=y_sample,
    random_state=42
)

print("\nTraining Shape:", X_train.shape)
print("Testing Shape:", X_test.shape)

print("\nTraining Class Distribution:")
print(y_train.value_counts())

print("\nTesting Class Distribution:")
print(y_test.value_counts())

# ============================================================
# Feature Scaling
# ============================================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)

X_test_scaled = scaler.transform(X_test)

print("\nFeature scaling completed successfully.")

# Why is the scaler fitted only on the training data?
# StandardScaler calculates the mean and standard deviation of the
# features. If we fit the scaler on the complete dataset before the
# train/test split, information from the test set would be used to
# calculate these values.
# This would cause data leakage because the training process would
# indirectly receive information from the test data.
# Therefore, we fit the scaler only on X_train and use the same
# fitted scaler to transform both X_train and X_test.


# ============================================================
# Q3 - Linear and Probabilistic Baseline Models
# ============================================================

# ------------------------------------------------------------
# Logistic Regression
# ------------------------------------------------------------

lr_model = LogisticRegression(max_iter=1000)

lr_model.fit(X_train_scaled,y_train)

lr_pred = lr_model.predict(X_test_scaled)

# ------------------------------------------------------------
# Gaussian Naive Bayes
# ------------------------------------------------------------

nb_model = GaussianNB()

nb_model.fit(X_train_scaled,y_train)

nb_pred = nb_model.predict(X_test_scaled)

# ============================================================
# Q4 - Instance-Based and Tree-Based Models
# ============================================================

# ------------------------------------------------------------
# K-Nearest Neighbors (KNN)
# ------------------------------------------------------------

knn_model = KNeighborsClassifier(n_neighbors=5)

knn_model.fit(X_train_scaled,y_train)

knn_pred = knn_model.predict(X_test_scaled)

# ------------------------------------------------------------
# Decision Tree Classifier
# ------------------------------------------------------------

tree_model = DecisionTreeClassifier(random_state=42)

tree_model.fit(X_train_scaled,y_train)

tree_pred = tree_model.predict(X_test_scaled)

# ============================================================
# Q5 - Ensemble Models
# ============================================================

# ------------------------------------------------------------
# Random Forest Classifier
# ------------------------------------------------------------

rf_model = RandomForestClassifier(n_estimators=200,random_state=42)

rf_model.fit(X_train_scaled,y_train)

rf_pred = rf_model.predict(X_test_scaled)


# ------------------------------------------------------------
# Gradient Boosting Classifier
# ------------------------------------------------------------

gb_model = GradientBoostingClassifier(random_state=42)

gb_model.fit(X_train_scaled,y_train)

gb_pred = gb_model.predict(X_test_scaled)

# ------------------------------------------------------------
# Bagging vs Boosting
# ------------------------------------------------------------

# Bagging and Boosting are both ensemble learning techniques,
# but they work differently.

# Bagging builds multiple models independently and in parallel
# and combines their predictions. Its main goal is to reduce
# variance and make the model more stable.
# Random Forest is an example of bagging because it builds many
# decision trees independently using different bootstrap samples
# and combines their predictions.

# Boosting builds models sequentially. Each new model focuses
# on correcting errors made by previous models.
# Gradient Boosting is an example of boosting. Its main goal is
# to improve the model by reducing bias and correcting previous
# errors.

# ============================================================
# Q6 - Support Vector Machine
# ============================================================

svm_model = SVC(
    kernel="rbf",
    probability=True,
    random_state=42
)

svm_model.fit(X_train_scaled,y_train)

svm_pred = svm_model.predict(X_test_scaled)


# ============================================================
# Q7 - Performance Metrics for Every Model
# ============================================================

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report
)

import matplotlib.pyplot as plt


# Store all trained models
models = {
    "Logistic Regression": lr_model,
    "Gaussian Naive Bayes": nb_model,
    "KNN": knn_model,
    "Decision Tree": tree_model,
    "Random Forest": rf_model,
    "Gradient Boosting": gb_model,
    "SVM": svm_model
}


# Class names
class_names = sorted(y_test.unique())


# Store performance results
results = []


# Calculate metrics for every model
for name, model in models.items():

    # Predict class labels
    y_pred = model.predict(X_test_scaled)

    # Predict probabilities for all 7 classes
    y_prob = model.predict_proba(X_test_scaled)

    # Accuracy
    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    # Weighted Precision
    precision = precision_score(
        y_test,
        y_pred,
        average="weighted"
    )

    # Weighted Recall
    recall = recall_score(
        y_test,
        y_pred,
        average="weighted"
    )

    # Weighted F1 Score
    f1_weighted = f1_score(
        y_test,
        y_pred,
        average="weighted"
    )

    # Macro F1 Score
    f1_macro = f1_score(
        y_test,
        y_pred,
        average="macro"
    )

    # Multiclass ROC-AUC
    roc_auc = roc_auc_score(
        y_test,
        y_prob,
        multi_class="ovr",
        average="weighted"
    )

    # Store results
    results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Weighted": f1_weighted,
        "F1 Macro": f1_macro,
        "ROC-AUC": roc_auc
    })


# Create comparison dataframe
results_df = pd.DataFrame(results)


print("\n============================================================")
print("Performance Metrics - All Multiclass Models")
print("============================================================")

print(
    results_df.to_string(index=False)
)

# ============================================================
# Confusion Matrix for Every Model
# ============================================================

for name, model in models.items():

    y_pred = model.predict(X_test_scaled)

    cm = confusion_matrix(
        y_test,
        y_pred,
        labels=class_names
    )

    print("\n============================================================")
    print(name)
    print("============================================================")

    print("Confusion Matrix:")
    print(cm)

    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=class_names
    )

    disp.plot(
        xticks_rotation=45
    )

    plt.title(f"Confusion Matrix - {name}")
    plt.xlabel("Predicted Activity")
    plt.ylabel("Actual Activity")

    plt.tight_layout()
    plt.show()

# ============================================================
# Best Model Based on Weighted F1 Score
# ============================================================

best_model_name = results_df.loc[
    results_df["F1 Weighted"].idxmax(),
    "Model"
]

best_model = models[best_model_name]

print("\n============================================================")
print("Best Model")
print("============================================================")

print(
    "Best Model based on Weighted F1 Score:",
    best_model_name
)

# ============================================================
# Classification Report - Best Model
# ============================================================

best_pred = best_model.predict(
    X_test_scaled
)

print("\n============================================================")
print("Classification Report - Best Model")
print("============================================================")

print(
    classification_report(
        y_test,
        best_pred,
        target_names=class_names
    )
)

# Mean F1 Score = 0.7768
# Standard Deviation = 0.0083
#
# The mean F1-score represents the average performance of the Random Forest
# model across the 5 cross-validation folds, while the standard deviation
# shows how much the performance varies between the folds.
#
# 5-fold stratified cross-validation is more trustworthy than a single
# train-test split because the model is evaluated on five different
# validation sets while maintaining the class distribution in each fold.
# This reduces the dependence on one particular split and provides a more
# reliable estimate of the model's general performance.
#
# The small standard deviation (0.0083) indicates that the Random Forest
# performance is relatively consistent across the five folds.

# ============================================================
# Q9 - Comparison Plots
# ============================================================

# ============================================================
# Grouped Bar Chart of Performance Metrics
# ============================================================

metrics = [
    "Accuracy",
    "Precision",
    "Recall",
    "F1 Weighted",
    "F1 Macro",
    "ROC-AUC"
]

x = range(len(results_df))

width = 0.13

plt.figure(figsize=(15, 7))

for i, metric in enumerate(metrics):

    plt.bar(
        [value + (i - 2.5) * width for value in x],
        results_df[metric],
        width=width,
        label=metric
    )

plt.xlabel("Models")

plt.ylabel("Score")

plt.title(
    "Comparison of Performance Metrics Across Multiclass Models"
)

plt.xticks(
    list(x),
    results_df["Model"],
    rotation=30,
    ha="right"
)

plt.legend()

plt.tight_layout()

plt.show()

# ============================================================
# Multiclass ROC Curves - One-vs-Rest
# ============================================================

# Class order
class_names = sorted(y.unique())

# Convert multiclass labels into binary format
# for One-vs-Rest ROC calculation
y_test_bin = label_binarize(
    y_test,
    classes=class_names
)

plt.figure(figsize=(12, 8))

for name, model in models.items():

    # Predict probabilities for all 7 classes
    y_prob = model.predict_proba(X_test_scaled)

    # Calculate macro-average ROC curve
    all_fpr = []
    all_tpr = []

    for i in range(len(class_names)):

        fpr, tpr, thresholds = roc_curve(
            y_test_bin[:, i],
            y_prob[:, i]
        )

        all_fpr.append(fpr)
        all_tpr.append(tpr)

    # Create common FPR points
    import numpy as np

    mean_fpr = np.linspace(
        0,
        1,
        100
    )

    mean_tpr = np.zeros_like(mean_fpr)

    for fpr, tpr in zip(all_fpr, all_tpr):

        mean_tpr += np.interp(
            mean_fpr,
            fpr,
            tpr
        )

    mean_tpr /= len(class_names)

    # Calculate multiclass ROC-AUC
    auc = roc_auc_score(
        y_test,
        y_prob,
        multi_class="ovr",
        average="macro"
    )

    plt.plot(
        mean_fpr,
        mean_tpr,
        label=f"{name} (AUC = {auc:.3f})"
    )


# Random classifier reference line

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--",
    label="Random Classifier"
)

plt.xlabel(
    "False Positive Rate"
)

plt.ylabel(
    "True Positive Rate"
)

plt.title(
    "Multiclass ROC Curves - One-vs-Rest"
)

plt.legend(
    loc="lower right"
)

plt.tight_layout()

plt.show()

# ============================================================
# Random Forest Feature Importance
# ============================================================

feature_names = [
    "avg_rss12",
    "var_rss12",
    "avg_rss13",
    "var_rss13",
    "avg_rss23",
    "var_rss23"
]


# Get feature importance from Random Forest

feature_importance = rf_model.feature_importances_


feature_importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": feature_importance
})


# Sort from highest to lowest

feature_importance_df = feature_importance_df.sort_values(
    by="Importance",
    ascending=False
)


print("\n============================================================")
print("Random Forest Feature Importance")
print("============================================================")


print(
    feature_importance_df.to_string(index=False)
)


# ============================================================
# Feature Importance Plot
# ============================================================

plt.figure(figsize=(10, 6))

plt.barh(
    feature_importance_df["Feature"],
    feature_importance_df["Importance"]
)

plt.xlabel(
    "Importance"
)

plt.ylabel(
    "Sensor Features"
)

plt.title(
    "Random Forest Feature Importance - Multiclass Classification"
)


# Display most important feature at top

plt.gca().invert_yaxis()

plt.tight_layout()

plt.show()

# -------------------------------------------------------
# Build the Comparison Table (Q10)
# -------------------------------------------------------

# Sort models by Weighted F1 Score in descending order
model_comparison = results_df.sort_values(
    by="F1 Weighted",
    ascending=False
)

print("\n=======================================================")
print("Multiclass Model Comparison Table")
print("=======================================================")

print(
    model_comparison.to_string(index=False)
)

# Save comparison table
model_comparison.to_csv(
    "multiclass_model_comparison.csv",
    index=False
)

print(
    "\nMulticlass model comparison table saved as "
    "multiclass_model_comparison.csv"
)