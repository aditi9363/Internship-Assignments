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

df = pd.read_csv("Master_DF.csv")

X = df[
    [
        "avg_rss12",
        "var_rss12",
        "avg_rss13",
        "var_rss13",
        "avg_rss23",
        "var_rss23"
    ]
]

y = df["label"]

# Stratified sampling
X_sample, _, y_sample, _ = train_test_split(
    X,
    y,
    train_size=15000,
    stratify=y,
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X_sample,
    y_sample,
    test_size=0.25,
    stratify=y_sample,
    random_state=42
)

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Explain why fitting the scaler on the whole dataset (before splitting) 
# leaks test information into training :-
# We should not fit the scaler on the entire dataset before splitting because
# StandardScaler would calculate the mean and standard deviation using both
# training and test data. This allows information from the test set to influence
# the training process, causing data leakage and overly optimistic performance.
# Therefore, we fit the scaler only on X_train and use the same scaler to
# transform X_test without fitting it again.

# ----------------------------------------------
# Logistic Regression
# ----------------------------------------------
lr_model = LogisticRegression(max_iter=1000)

lr_model.fit(X_train_scaled, y_train)

lr_pred = lr_model.predict(X_test_scaled)

# -----------------------------------------------
# GaussianNB - Naive Bayes
# -----------------------------------------------
nb_model = GaussianNB()

nb_model.fit(X_train_scaled, y_train)

nb_pred = nb_model.predict(X_test_scaled)

# ------------------------------------------------
# K-Nearest Neighbors (KNN)
# ------------------------------------------------
knn_model = KNeighborsClassifier(n_neighbors=5)

knn_model.fit(X_train_scaled, y_train)

knn_pred = knn_model.predict(X_test_scaled)

# --------------------------------------------------
# Decision Tree Classifier
# --------------------------------------------------
tree_model = DecisionTreeClassifier(random_state=42)

tree_model.fit(X_train_scaled, y_train)

tree_pred = tree_model.predict(X_test_scaled)

# --------------------------------------------------
# Random Forest Classifier
# --------------------------------------------------
rf_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

rf_model.fit(X_train_scaled, y_train)

rf_pred = rf_model.predict(X_test_scaled)

# ---------------------------------------------------
# Gradient Boosting Classifier
# ---------------------------------------------------
gb_model = GradientBoostingClassifier(random_state=42)

gb_model.fit(X_train_scaled, y_train)

gb_pred = gb_model.predict(X_test_scaled)

# Bagging vs Boosting
# Bagging and Boosting are both ensemble learning techniques, but they work differently.
# Bagging builds multiple models independently and in parallel, then combines their predictions.
# Its main goal is to reduce variance and make the model more stable.
# Example: Random Forest uses bagging.
#
# Boosting builds models sequentially, where each new model focuses on correcting the
# errors made by the previous models. Its main goal is to reduce bias and improve accuracy.
# Example: Gradient Boosting uses boosting.

# ---------------------------------------------------
# Support Vector Machine
# ---------------------------------------------------

svm_model = SVC(
    kernel="rbf",
    probability=True,
    random_state=42
)
svm_model.fit(X_train_scaled, y_train)

svm_pred = svm_model.predict(X_test_scaled)

# ---------------------------------------------------
# Performance Metrics for Every Model
# ---------------------------------------------------
from sklearn.metrics import(
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

models = {
    "Logistic Regression": lr_model,
    "Gaussian Naive Bayes": nb_model,
    "KNN": knn_model,
    "Decision Tree": tree_model,
    "Random Forest": rf_model,
    "Gradient Boosting": gb_model,
    "SVM": svm_model
}

# Calculate performance metrics for every model

results = []

for name, model in models.items():

    # Predict class labels
    y_pred = model.predict(X_test_scaled)

    # Predict probability for positive class
    y_prob = model.predict_proba(X_test_scaled)[:, 1]

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)

    # Store results
    results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "ROC-AUC": roc_auc
    })

# Create performance comparison table

results_df = pd.DataFrame(results)

print("\n==================================================")
print("Performance Metrics - All Models")
print("\n==================================================")

print(results_df.to_string(index=False))

# Confusion Matrix for every model
for name, model in models.items():
    y_pred = model.predict(X_test_scaled)

    cm = confusion_matrix(y_test, y_pred)

    print(f"\n{name}")
    print("Confusion Matrix:")
    print(cm)

    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=["Unhealthy", "Healthy"]
    )
    disp.plot()

    plt.title(f"Confusion Matrix - {name}")
    plt.xlabel("Predicted Label")
    plt.ylabel("Actual Label")
    plt.show()

# Find the best model based on F1 score
best_model_name = results_df.loc[
    results_df["F1 Score"].idxmax(),
    "Model"
]

best_model = models[best_model_name]

print("\n===============================================")
print("Best Model")
print("=================================================")

print("Best Model based on F1 Score:", best_model_name)

# Classification Report for the best model

best_pred = best_model.predict(X_test_scaled)

print("\n===============================================")
print("Classification Report - Best Model")
print("=================================================")

print(
    classification_report(
        y_test,
        best_pred,
        target_names=["Unhealthy", "Healthy"]
    )
)
# Because the classes are imbalanced (~66% healthy), explain why accuracy alone is misleading and F1 / ROC-AUC
# matter more  :-
# The dataset is imbalanced, with approximately 66% Healthy samples
# and 34% Unhealthy samples. Therefore, accuracy alone can be misleading.
# A model could achieve relatively high accuracy by mostly predicting
# the majority Healthy class, while performing poorly on Unhealthy samples.
#
# F1-score is more informative because it balances Precision and Recall,
# helping evaluate how well the model performs without relying only on
# the majority class.
#
# ROC-AUC is also important because it measures how well the model
# distinguishes between Healthy and Unhealthy classes across different
# classification thresholds.
#
# Therefore, for this imbalanced dataset, F1-score and ROC-AUC provide
# more informative measures of model performance than accuracy alone.

# --------------------Comparison Plots------------------------

# ============================================================
# Grouped Bar Chart of Performance Metrics
# ============================================================

metrics = [
    "Accuracy",
    "Precision",
    "Recall",
    "F1 Score",
    "ROC-AUC"
]

x = range(len(results_df))

width = 0.15

plt.figure(figsize=(14, 7))

for i, metric in enumerate(metrics):
    plt.bar(
        [value + (i - 2) * width for value in x],
        results_df[metric],
        width=width,
        label=metric
    )

plt.xlabel("Models")
plt.ylabel("Score")

plt.title(
    "Comparison of Performance Metrics Across Models"
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

# ======================================================
# ROC Curves for All Models
# ======================================================
from sklearn.metrics import roc_curve

plt.figure(figsize=(10, 7))

for name, model in models.items():

    # Predict probability for positive class
    y_prob = model.predict_proba(X_test_scaled)[:, 1]

    # Calculate ROC curve
    fpr, tpr, thresholds = roc_curve(
        y_test,
        y_prob
    )

    # Calculate AUC
    auc = roc_auc_score(
        y_test,
        y_prob
    )

    # Plot ROC curve
    plt.plot(
        fpr,
        tpr,
        label=f"{name} (AUC = {auc:.3f})"
    )

# Random Classifier Reference Line
plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--", 
    label="Random Classifier"
)

plt.xlabel("False Positive Rate")

plt.ylabel("True Positive Rate")

plt.title("ROC Curves for All Models")

plt.legend(loc="lower right")

plt.tight_layout()

plt.show()

# ===================================================
# Random Forest Feature Importance
# ===================================================
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
print("==========================================================")

print(feature_importance_df.to_string(index=False)
)

# Plot feature importance
plt.figure(figsize=(10, 6))

plt.barh(
    feature_importance_df["Feature"],
    feature_importance_df["Importance"]
)

plt.xlabel("Importance")

plt.ylabel("Sensor Features")

plt.title("Random Forest Feature Importance")

# Display most important feature at top
plt.gca().invert_yaxis()

plt.tight_layout()

plt.show()

# -------------------------------------------------------
# Build the Comparison Table (Q10)
# -------------------------------------------------------

# Sort models by F1 Score in descending order
model_comparison = results_df.sort_values(
    by="F1 Score",
    ascending=False
)

print("\n=======================================================")
print("Model Comparison Table")
print("=========================================================")

print(
    model_comparison.to_string(index=False)
)

model_comparison.to_csv(
    "model_comparison.csv",
    index=False
)

print("\nModel comparison table saved as model_comparison.csv")

#print("Training Shape :", X_train.shape)
#print("Testing Shape :", X_test.shape)

#print("\nTraining Labels")
#print(y_train.value_counts())

#print("\nTesting Labels")
#print(y_test.value_counts())

#print("\nFeature scaling completed successfully")
