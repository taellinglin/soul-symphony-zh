import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input

# Path to the dataset file
DATASET_FILE = "dataset.json"

# Load the dataset
def load_dataset(dataset_file):
    with open(dataset_file, "r") as f:
        dataset = json.load(f)

    features = []
    labels = []

    for entry in dataset:
        num_objects = len(entry.get("objects", []))
        total_vertices = sum(len(obj.get("vertices", [])) for obj in entry.get("objects", []))
        avg_scale = np.mean(
            [np.mean(obj.get("scale", [1, 1, 1])) for obj in entry.get("objects", [])]
        ) if num_objects > 0 else 1.0

        features.append([num_objects, total_vertices, avg_scale])
        labels.append([total_vertices, avg_scale])  # Example of regression labels

    features = np.array(features, dtype=np.float32)
    labels = np.array(labels, dtype=np.float32)

    return features, labels

# Build a more complex neural network model
def build_model(input_dim):
    model = Sequential([
        Input(shape=(input_dim,)),
        Dense(128, activation="relu"),
        Dropout(0.3),
        Dense(64, activation="relu"),
        Dropout(0.3),
        Dense(2, activation="linear")  # Two outputs: vertices and scale
    ])

    model.compile(
        optimizer="adam",
        loss="mean_squared_error",
        metrics=["mae"]
    )

    return model

# Train the model
def train_model(features, labels):
    model = build_model(features.shape[1])

    split_idx = int(0.8 * len(features))
    x_train, x_test = features[:split_idx], features[split_idx:]
    y_train, y_test = labels[:split_idx], labels[split_idx:]

    model.fit(
        x_train, y_train,
        validation_data=(x_test, y_test),
        epochs=2048,  # Increased epochs for extended training
        batch_size=128
    )

    loss, mae = model.evaluate(x_test, y_test)
    print(f"Test MAE: {mae:.2f}")

    return model

# Main function
def main():
    features, labels = load_dataset(DATASET_FILE)

    model = train_model(features, labels)

    model.save("enhanced_blend_model.h5")
    print("Enhanced model saved as enhanced_blend_model.h5")

if __name__ == "__main__":
    main()
