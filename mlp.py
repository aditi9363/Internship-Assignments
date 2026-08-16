import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, Dropout


# ============================================================
# Q1) Data Preparation and Standardisation
# ============================================================

# ------------------------------------------------------------
# Load the Dataset
# ------------------------------------------------------------

df = pd.read_csv("Master_DF.csv")

print("Original Dataset Shape:", df.shape)


# ------------------------------------------------------------
# Select the Six Sensor Features
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# Take a Stratified 15,000-row Sample
# ------------------------------------------------------------

# A stratified sample preserves the original class proportions.
# This reduces the dataset size for faster neural-network training
# while maintaining a representative distribution of the two classes.

X_sample, _, y_sample, _ = train_test_split(
    X,
    y,
    train_size=15000,
    stratify=y,
    random_state=42
)

print("Sample Shape:", X_sample.shape)

print("Sample Class Distribution:")
print(y_sample.value_counts())


# ------------------------------------------------------------
# Split the Sample into Training and Testing Sets
# ------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X_sample,
    y_sample,
    test_size=0.25,
    stratify=y_sample,
    random_state=42
)

print("Training Shape:", X_train.shape)
print("Testing Shape:", X_test.shape)


# ------------------------------------------------------------
# Standardise the Features
# ------------------------------------------------------------

scaler = StandardScaler()

# Fit the scaler ONLY on the training data.
# This prevents information from the test set from leaking
# into the training process.

X_train_scaled = scaler.fit_transform(X_train)

# Use the same scaler to transform the test data.
X_test_scaled = scaler.transform(X_test)


# ------------------------------------------------------------
# Display the Scaled Data
# ------------------------------------------------------------

print("\nFirst 5 rows of scaled training data:")
print(X_train_scaled[:5])

print("\nFirst 5 rows of scaled testing data:")
print(X_test_scaled[:5])



# Why scaling is needed:
# Neural networks are commonly trained using gradient descent.
# If input features have very different numerical scales, the
# gradients can become unbalanced, causing the optimizer to take
# inefficient steps and converge slowly.
#
# Standardising the input features to a common scale
# (mean ≈ 0 and standard deviation ≈ 1) makes gradient descent
# more stable and helps the neural network converge faster.


# ============================================================
# Q2) Build the MLP
# ============================================================

model = Sequential([
    Input(shape=(6,)),
    Dense(32, activation="relu"),
    Dropout(0.2),
    Dense(16, activation="relu"),
    Dense(1, activation="sigmoid")
])


# ------------------------------------------------------------
# Display the Model Architecture
# ------------------------------------------------------------

model.summary()

# ReLU is used in the hidden layers because it introduces
# non-linearity, allowing the network to learn complex
# relationships between the input features.
#
# Dropout(0.2) randomly disables 20% of neurons during training.
# It acts as regularisation and helps reduce overfitting.
#
# A single sigmoid output neuron is used because this is a
# binary classification problem. Sigmoid produces an output
# between 0 and 1, which can be interpreted as a probability
# of the positive class.

# Parameter calculation:
# Dense(32):
# (6 × 32) + 32 = 224 parameters
#
# Dropout:
# 0 parameters because it has no learnable weights or biases
#
# Dense(16):
# (32 × 16) + 16 = 528 parameters
#
# Dense(1):
# (16 × 1) + 1 = 17 parameters
#
# Total trainable parameters:
# 224 + 528 + 17 = 769


# ============================================================
# Q3) Compile and Train the MLP
# ============================================================

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

# ------------------------------------------------------------
# Train the Model
# ------------------------------------------------------------

history = model.fit(
    X_train_scaled,
    y_train,
    validation_split=0.2,
    epochs=40,
    batch_size=64
)

# Training parameters:
#
# validation_split=0.2:
# 20% of the training data is reserved for validation.
#
# epochs=40:
# An epoch is one complete pass through the training data.
# The model makes 40 complete passes through the training data.
#
# batch_size=64:
# The model processes 64 samples at a time before updating
# its weights.
#
# history:
# Stores loss, accuracy, validation loss, and validation
# accuracy for every epoch. This history can be used later
# to plot training and validation curves.

# ============================================================
# Q4) Evaluate & Compare
# ============================================================

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay
)

import matplotlib.pyplot as plt


# ------------------------------------------------------------
# 1. Make predictions on the unseen test set
# ------------------------------------------------------------

# The model returns probabilities between 0 and 1 because
# the output layer uses the sigmoid activation function.

y_test_prob = model.predict(X_test_scaled).ravel()

# Convert probabilities into binary class predictions.
# Probability >= 0.5 is classified as class 1,
# otherwise it is classified as class 0.

y_test_pred = (y_test_prob >= 0.5).astype(int)


# ------------------------------------------------------------
# 2. Calculate test-set performance metrics
# ------------------------------------------------------------

accuracy = accuracy_score(y_test, y_test_pred)

f1 = f1_score(y_test, y_test_pred)

roc_auc = roc_auc_score(y_test, y_test_prob)


print("\n============================================================")
print("Q4) MLP TEST SET PERFORMANCE")
print("============================================================")

print(f"Accuracy : {accuracy:.4f}")
print(f"F1 Score : {f1:.4f}")
print(f"ROC-AUC  : {roc_auc:.4f}")


# ------------------------------------------------------------
# 3. Confusion Matrix
# ------------------------------------------------------------

cm = confusion_matrix(y_test, y_test_pred)

print("\nConfusion Matrix:")
print(cm)


# Display confusion matrix as a plot

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Class 0", "Class 1"]
)

disp.plot()
plt.title("MLP Confusion Matrix")
plt.tight_layout()
plt.show()


# ============================================================
# 4. Plot Training vs Validation Learning Curves
# ============================================================

# ------------------------------------------------------------
# Accuracy Learning Curve
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    history.history["accuracy"],
    label="Training Accuracy"
)

plt.plot(
    history.history["val_accuracy"],
    label="Validation Accuracy"
)

plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.title("MLP Training vs Validation Accuracy")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# Loss Learning Curve
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    history.history["loss"],
    label="Training Loss"
)

plt.plot(
    history.history["val_loss"],
    label="Validation Loss"
)

plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("MLP Training vs Validation Loss")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# Learning Curves: Training vs Validation
# ------------------------------------------------------------
# The training and validation accuracy curves are plotted for
# all 40 epochs to observe how the model learns over time.
#
# The training and validation loss curves are also plotted to
# see whether the model's prediction error decreases during
# training.
#
# In this model, the training and validation accuracy remain
# relatively close to each other throughout training. The loss
# values also decrease, without a large and persistent gap
# between training and validation performance.
#
# Therefore, the model does not show strong signs of overfitting.
# It also does not appear to be severely underfitting because
# both training and validation performance reach around 85%.
#
# Overall, the MLP appears to generalise reasonably well to
# unseen validation data.

# ------------------------------------------------------------
# Comparison with Classical ML Models
# ------------------------------------------------------------
#
# In the previous ML assignment, Random Forest was the best
# classical model with an F1 score of approximately 0.91.
#
# The MLP achieved:
# Accuracy = 0.8552
# F1 Score = 0.8929
# ROC-AUC  = 0.9380
#
# Therefore, the MLP did NOT beat the Random Forest in terms
# of F1 score:
# MLP F1            = 0.8929
# Random Forest F1  ≈ 0.91
#
# Random Forest performed slightly better on this dataset.
#
# This shows that a neural network is not automatically better
# than classical ML models. This dataset is relatively small
# and tabular, with only six sensor features, where tree-based
# ensemble models such as Random Forest can perform very well.
#
# Therefore, for this small tabular classification problem,
# Random Forest was the better model based on F1 score.