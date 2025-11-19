import cv2
import numpy as np
from tensorflow.keras.models import load_model
from fraud_detection.rules_based_checks import ela_score, sharpness_score, clone_detection

MODEL_PATH = "fraud_detection/model/fraud_cnn.keras"
cnn_model = load_model(MODEL_PATH)

def cnn_fraud_probability(path):
    img = cv2.imread(path)
    img = cv2.resize(img, (224, 224)) / 255.0
    img = np.expand_dims(img, axis=0)
    return float(cnn_model.predict(img)[0][0])

def compute_fraud_score(path):
    cnn_prob = cnn_fraud_probability(path)
    ela = ela_score(path)
    sharp = sharpness_score(path)
    clone = clone_detection(path)

    final = (
        (cnn_prob * 0.5) +
        (ela * 0.2) +
        ((1 - sharp) * 0.15) +
        (clone * 0.15)
    ) * 100

    return {
        "fraud_score": round(final, 2),
        "cnn_fake_probability": round(cnn_prob, 3),
        "ela_artifact_score": round(ela, 3),
        "clone_region_score": round(clone, 3),
        "sharpness_score": round(sharp, 3)
    }
