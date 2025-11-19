import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

DATA = "fraud_detection/dataset"

train_datagen = ImageDataGenerator(
    rescale=1/255.0,
    validation_split=0.2,
    rotation_range=15,
    zoom_range=0.15,
    horizontal_flip=False
)

train = train_datagen.flow_from_directory(
    DATA,
    target_size=(224, 224),
    batch_size=16,
    subset="training"
)

val = train_datagen.flow_from_directory(
    DATA,
    target_size=(224, 224),
    batch_size=16,
    subset="validation"
)

base = EfficientNetB0(weights="imagenet", include_top=False, input_shape=(224, 224, 3))

x = GlobalAveragePooling2D()(base.output)
x = Dropout(0.4)(x)
output = Dense(1, activation="sigmoid")(x)

model = Model(inputs=base.input, outputs=output)

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-4),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

print("Training classifier...")
history = model.fit(train, validation_data=val, epochs=10)

model.save("fraud_detection/model/fraud_cnn.keras")
print("Model saved!")
