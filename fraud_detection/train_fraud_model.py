import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# ==============================
# PATHS
# ==============================
DATA_DIR = "fraud_detection/dataset/"

# Merge dataset folders into two classes
train_dir = {
    "real":      os.path.join(DATA_DIR, "real"),
    "tampered":  os.path.join(DATA_DIR, "tampered"),
    "ai_clean":  os.path.join(DATA_DIR, "ai_generated/clean"),
    "ai_defect": os.path.join(DATA_DIR, "ai_generated/defective"),
}

# ==============================
# CREATE COMBINED TRAINING SET
# ==============================
def create_master_folder():
    master_real = "fraud_detection/dataset/_train/real"
    master_fake = "fraud_detection/dataset/_train/fake"

    os.makedirs(master_real, exist_ok=True)
    os.makedirs(master_fake, exist_ok=True)

    # Copy real data
    for f in os.listdir(train_dir["real"]):
        src = os.path.join(train_dir["real"], f)
        dst = os.path.join(master_real, f)
        tf.io.gfile.copy(src, dst, overwrite=True)

    # Copy fake data (tampered + AI + defective)
    for folder in ["tampered", "ai_clean", "ai_defect"]:
        for f in os.listdir(train_dir[folder]):
            src = os.path.join(train_dir[folder], f)
            dst = os.path.join(master_fake, f)
            tf.io.gfile.copy(src, dst, overwrite=True)

    print("✔ Master dataset created successfully!")

create_master_folder()

MASTER_DATASET = "fraud_detection/dataset/_train/"

# ==============================
# IMAGE GENERATOR
# ==============================
datagen = ImageDataGenerator(
    rescale=1.0/255,
    validation_split=0.2
)

train_gen = datagen.flow_from_directory(
    MASTER_DATASET,
    target_size=(224, 224),
    batch_size=32,
    class_mode="binary",
    subset="training"
)

val_gen = datagen.flow_from_directory(
    MASTER_DATASET,
    target_size=(224, 224),
    batch_size=32,
    class_mode="binary",
    subset="validation"
)

# ==============================
# MODEL ARCHITECTURE (CNN)
# ==============================
model = Sequential([
    Conv2D(32, (3,3), activation="relu", input_shape=(224,224,3)),
    MaxPooling2D(2,2),

    Conv2D(64, (3,3), activation="relu"),
    MaxPooling2D(2,2),

    Conv2D(128, (3,3), activation="relu"),
    MaxPooling2D(2,2),

    Flatten(),
    Dense(256, activation="relu"),
    Dropout(0.3),
    Dense(1, activation="sigmoid")   # Fake or Real
])

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# ==============================
# TRAIN MODEL
# ==============================
history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=15
)

# ==============================
# SAVE MODEL
# ==============================
model.save("fraud_detection/model/fraud_cnn_v2.keras")

print("\n✔ Training Completed & Model Saved!")
