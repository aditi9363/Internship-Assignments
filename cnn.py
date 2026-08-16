import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf


# =========================================================
# Q5) Load & Prepare MNIST
# =========================================================

# Load the provided MNIST dataset from the local file.
data = np.load("mnist.npz")

# Extract training images and labels.
X_train = data["x_train"]
y_train = data["y_train"]

# Extract test images and labels.
X_test = data["x_test"]
y_test = data["y_test"]


# Display the original dataset shapes.
print("Original X_train shape:", X_train.shape)
print("Original y_train shape:", y_train.shape)
print("Original X_test shape:", X_test.shape)
print("Original y_test shape:", y_test.shape)


# Normalize pixel values from 0-255 to 0-1.
X_train = X_train.astype("float32") / 255.0
X_test = X_test.astype("float32") / 255.0


# Add a channel dimension for CNN input.
# MNIST is grayscale, so it has 1 channel.
X_train = X_train[..., np.newaxis]
X_test = X_test[..., np.newaxis]


# Display the final shapes after preprocessing.
print("\nAfter preprocessing:")
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)


# Plot a grid of sample digits with their labels.
plt.figure(figsize=(10, 5))

for i in range(10):
    plt.subplot(2, 5, i + 1)
    plt.imshow(X_train[i].squeeze(), cmap="gray")
    plt.title(f"Label: {y_train[i]}")
    plt.axis("off")

plt.tight_layout()
plt.show()


# =========================================================
# Q6) Dense-Network Baseline
# =========================================================

# Build a plain dense neural network.
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28, 1)),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


# Display the model architecture and parameter counts.
print("\nDense Network Summary:")
model.summary()


# Train the dense network.
history = model.fit(
    X_train,
    y_train,
    epochs=10,
    batch_size=128,
    validation_split=0.1
)


# Evaluate the trained model on the unseen test dataset.
test_loss, test_accuracy = model.evaluate(
    X_test,
    y_test,
    verbose=0
)


# Display the test performance.
print("\nDense Network Test Results:")
print("Test Loss:", test_loss)
print("Test Accuracy:", test_accuracy)
print("Test Accuracy (%):", test_accuracy * 100)

# Flatten converts each 28x28x1 image into a 784-element
# vector. It does not remove the pixel values, but it removes
# their 2D spatial arrangement. Therefore, the Dense network
# no longer explicitly knows which pixels were neighbours
# in the original image. This means local spatial patterns
# such as edges and shapes are not naturally preserved.
# CNNs address this limitation by using convolutional layers
# that operate directly on local regions of the image.

# =========================================================
# Q7) Build the CNN
# =========================================================

cnn_model = tf.keras.Sequential([
    tf.keras.Input(shape=(28, 28, 1)),

    tf.keras.layers.Conv2D(
        32,
        kernel_size=3,
        activation="relu"
    ),

    tf.keras.layers.MaxPooling2D(pool_size=2),

    tf.keras.layers.Conv2D(
        64,
        kernel_size=3,
        activation="relu"
    ),

    tf.keras.layers.MaxPooling2D(pool_size=2),

    tf.keras.layers.Flatten(),

    tf.keras.layers.Dense(
        64,
        activation="relu"
    ),

    tf.keras.layers.Dropout(0.3),

    tf.keras.layers.Dense(
        10,
        activation="softmax"
    )
])


# Compile the CNN
cnn_model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


# Display CNN architecture
print("\nCNN Model Summary:")
cnn_model.summary()

# Q7) CNN Architecture Explanation
#
# Model architecture:
# Conv2D(32, 3, ReLU) → MaxPooling2D(2) →
# Conv2D(64, 3, ReLU) → MaxPooling2D(2) →
# Flatten → Dense(64, ReLU) → Dropout(0.3) →
# Dense(10, Softmax)
#
# 1. Conv2D(32, 3, ReLU):
#    This layer uses 32 learnable filters of size 3x3 to detect
#    local patterns such as edges, curves, and simple shapes.
#    The input image is 28x28x1. Because the default padding is
#    "valid", a 3x3 filter reduces the spatial size from 28x28
#    to 26x26. Since there are 32 filters, the output becomes
#    26x26x32.
#
# 2. MaxPooling2D(2):
#    A 2x2 max-pooling operation reduces the height and width
#    by approximately half, changing 26x26x32 to 13x13x32.
#    It keeps the maximum value from each 2x2 region, preserving
#    the strongest detected feature while reducing computation.
#
# 3. Conv2D(64, 3, ReLU):
#    This layer uses 64 filters to learn more complex and
#    higher-level features from the patterns detected by the
#    previous convolution layer. The 3x3 valid convolution
#    reduces 13x13 to 11x11, while the number of channels grows
#    from 32 to 64. Therefore, the output is 11x11x64.
#
# 4. MaxPooling2D(2):
#    Another 2x2 max-pooling operation reduces the spatial
#    dimensions from 11x11 to 5x5 (with valid pooling), while
#    keeping the 64 channels. The output becomes 5x5x64.
#
# 5. Flatten:
#    The 5x5x64 feature maps are converted into a single
#    one-dimensional vector of 1600 values (5*5*64).
#    Spatial structure is no longer represented explicitly after
#    this point, allowing the features to be passed to dense layers.
#
# 6. Dense(64, ReLU):
#    This fully connected layer combines the extracted features
#    to learn patterns useful for distinguishing the 10 MNIST
#    digit classes.
#
# 7. Dropout(0.3):
#    During training, randomly drops 30% of the neurons to reduce
#    overfitting and improve the model's ability to generalise.
#
# 8. Dense(10, Softmax):
#    The final layer has 10 neurons, one for each digit (0-9).
#    Softmax converts the outputs into probabilities whose sum
#    is 1. The class with the highest probability is the predicted
#    digit.
#
# Why does height/width shrink while channel count grows?
#    The height and width shrink because 3x3 convolutions with
#    "valid" padding remove border positions, and max-pooling
#    reduces the spatial dimensions. This gradually creates
#    smaller but more informative feature maps.
#
#    The channel count grows from 1 → 32 → 64 because each filter
#    produces one feature map. More filters allow the network to
#    learn and represent a larger variety of features. Early
#    filters may detect simple edges, while deeper filters can
#    detect more complex shapes and digit patterns.
#
# What are filters?
#    Filters are small learnable matrices (kernels) that slide
#    across the image and detect specific patterns. During training,
#    the CNN learns the filter values automatically.
#
# What are feature maps?
#    A feature map is the output produced by applying one filter
#    to an input. It shows where the feature detected by that
#    filter occurs in the image. With 32 filters, Conv2D produces
#    32 feature maps; with 64 filters, it produces 64 feature maps.
#
# What does max-pooling do?
#    Max-pooling selects the largest value from each small region,
#    such as a 2x2 region. It reduces the spatial dimensions,
#    decreases computation, and keeps the strongest detected
#    features. It also makes the model somewhat less sensitive
#    to small shifts in the position of a feature.

# =========================================================
# Q8) Train the CNN and Plot Learning Curves
# =========================================================

# Compile the CNN using Adam optimizer and sparse categorical
# crossentropy because the labels are integer values from 0 to 9.
cnn_model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


# Train the CNN for approximately 5 epochs.
# validation_split=0.1 reserves 10% of the training data
# for validation during training.
cnn_history = cnn_model.fit(
    X_train,
    y_train,
    epochs=5,
    batch_size=128,
    validation_split=0.1
)


# Evaluate the trained CNN on the unseen test dataset.
cnn_test_loss, cnn_test_accuracy = cnn_model.evaluate(
    X_test,
    y_test,
    verbose=0
)


print("\nCNN Test Results:")
print("Test Loss:", cnn_test_loss)
print("Test Accuracy:", cnn_test_accuracy)
print("Test Accuracy (%):", cnn_test_accuracy * 100)


# =========================================================
# Plot Learning Curves
# =========================================================

# Plot training and validation loss.
plt.figure(figsize=(8, 5))

plt.plot(
    cnn_history.history["loss"],
    label="Training Loss"
)

plt.plot(
    cnn_history.history["val_loss"],
    label="Validation Loss"
)

plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("CNN Training vs Validation Loss")
plt.legend()
plt.grid(True)
plt.show()


# Plot training and validation accuracy.
plt.figure(figsize=(8, 5))

plt.plot(
    cnn_history.history["accuracy"],
    label="Training Accuracy"
)

plt.plot(
    cnn_history.history["val_accuracy"],
    label="Validation Accuracy"
)

plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.title("CNN Training vs Validation Accuracy")
plt.legend()
plt.grid(True)
plt.show()


# Evaluate the CNN on the test dataset
cnn_test_loss, cnn_test_accuracy = cnn_model.evaluate(
    X_test,
    y_test,
    verbose=0
)

# Display CNN test performance
print("\nCNN Test Results:")
print("Test Loss:", cnn_test_loss)
print("Test Accuracy:", cnn_test_accuracy)
print("Test Accuracy (%):", cnn_test_accuracy * 100)


# =========================================================
# Q9) Evaluate the CNN
# =========================================================
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# ---------------------------------------------------------
# 1. Evaluate CNN on the test dataset
# ---------------------------------------------------------
cnn_test_loss, cnn_test_accuracy = cnn_model.evaluate(
    X_test,
    y_test,
    verbose=0
)
print("\nQ9 - CNN Evaluation:")
print("Test Loss:", cnn_test_loss)
print("Test Accuracy:", cnn_test_accuracy)
print("Test Accuracy (%):", cnn_test_accuracy * 100)

# ---------------------------------------------------------
# 2. Generate predictions for the test images
# ---------------------------------------------------------

# The CNN outputs probabilities for all 10 classes.
predicted_probabilities = cnn_model.predict(
    X_test,
    verbose=0
)

# Select the class with the highest probability.
y_pred = np.argmax(predicted_probabilities, axis=1)

# ---------------------------------------------------------
# 3. Create and plot the 10x10 confusion matrix
# ---------------------------------------------------------

cm = confusion_matrix(
    y_test,
    y_pred
)

print("\nConfusion Matrix:")
print(cm)

plt.figure(figsize=(8, 8))

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=np.arange(10)
)

disp.plot(
    cmap="Blues",
    values_format="d",
    ax=plt.gca(),
    colorbar=False
)

plt.title("CNN Confusion Matrix - MNIST")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.show()


# ---------------------------------------------------------
# 4. Find incorrectly classified test images
# ---------------------------------------------------------

wrong_indices = np.where(y_pred != y_test)[0]

print("\nNumber of incorrect predictions:", len(wrong_indices))


# ---------------------------------------------------------
# 5. Plot sample predictions
# ---------------------------------------------------------

num_samples = 20

# Select up to 20 incorrectly classified images.
sample_indices = wrong_indices[:num_samples]

plt.figure(figsize=(12, 8))

for i, index in enumerate(sample_indices):

    plt.subplot(4, 5, i + 1)

    # Remove the channel dimension for displaying the image.
    plt.imshow(
        X_test[index].squeeze(),
        cmap="gray"
    )

    # Show the predicted and actual labels.
    plt.title(
        f"True: {y_test[index]} | Pred: {y_pred[index]}"
    )

    plt.axis("off")

plt.suptitle("Incorrect CNN Predictions")
plt.tight_layout()
plt.show()


# ---------------------------------------------------------
# 6. Compare CNN with Dense baseline
# ---------------------------------------------------------

dense_test_accuracy = 0.9775999784469604
dense_parameters = 101770

cnn_parameters = cnn_model.count_params()

print("\nModel Comparison:")
print("--------------------------------------")
print(f"Dense Baseline Accuracy: {dense_test_accuracy * 100:.2f}%")
print(f"Dense Baseline Parameters: {dense_parameters:,}")
print(f"CNN Accuracy: {cnn_test_accuracy * 100:.2f}%")
print(f"CNN Parameters: {cnn_parameters:,}")

accuracy_difference = (
    cnn_test_accuracy - dense_test_accuracy
) * 100

parameter_difference = (
    cnn_parameters - dense_parameters
)

print(f"CNN Accuracy Improvement: {accuracy_difference:.2f} percentage points")
print(f"Additional CNN Parameters: {parameter_difference:,}")

# Q9) Evaluate the CNN
# The CNN achieved 99.07% test accuracy on the 10,000 MNIST
# test images, showing that it generalises very well to unseen data.
#
# The 10x10 confusion matrix shows the actual labels against the
# predicted labels for all 10 digit classes (0-9). Values on the
# diagonal represent correct predictions, while off-diagonal values
# represent misclassifications.
#
# The CNN made 93 incorrect predictions out of 10,000 test images.
# Sample incorrect predictions are displayed with their true and
# predicted labels, with the wrong predictions marked clearly.
#
# Comparison with the dense baseline:
#
# Dense baseline:
# Test Accuracy = 97.74%
# Parameters = 101,770
#
# CNN:
# Test Accuracy = 99.07%
# Parameters = 121,930
#
# The CNN improves test accuracy by approximately 1.33 percentage
# points compared with the dense baseline, while using 20,160 more
# parameters. The CNN performs better because convolutional layers
# preserve spatial information and learn local image features,
# whereas the dense network flattens the image and loses its
# original spatial structure.