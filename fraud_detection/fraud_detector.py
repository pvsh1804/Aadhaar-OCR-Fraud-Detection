# fraud_detection/fraud_detector.py
import cv2
import numpy as np
from tensorflow.keras.models import load_model

from fraud_detection.rules_based_checks import (
    ela_score,
    sharpness_score,
    clone_detection,
)

MODEL_PATH = "fraud_detection/model/fraud_cnn.keras"

# Lazy-loaded global (prevents uvicorn import-time failures)
_cnn_model = None


def get_cnn_model():
    """Load CNN model once and reuse (safe for API)."""
    global _cnn_model
    if _cnn_model is None:
        _cnn_model = load_model(MODEL_PATH)
    return _cnn_model


def _read_image_any_format(path: str) -> np.ndarray:
    """
    Robust image read:
    - Try OpenCV first
    - If fails (TIFF, some JPEG/JFIF issues), fallback to PIL
    Returns BGR numpy array (OpenCV-like).
    """
    img = cv2.imread(path)

    if img is None:
        try:
            from PIL import Image
            pil_img = Image.open(path).convert("RGB")
            img = np.array(pil_img)
            # PIL gives RGB; convert to BGR to stay consistent with OpenCV
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        except Exception as e:
            raise ValueError(f"Could not read image from path: {path}. Error: {e}")

    return img


def preprocess_image(path: str, size=(224, 224)) -> np.ndarray:
    """Read + resize + normalize image for CNN."""
    img = _read_image_any_format(path)

    img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)  # (1, H, W, C)
    return img


def cnn_fraud_probability(path: str, model=None) -> float:
    """
    Returns fake probability from CNN (0–1).
    model: optional; if not provided, uses cached model.
    """
    if model is None:
        model = get_cnn_model()

    x = preprocess_image(path)
    pred = model.predict(x, verbose=0)

    # handle different output shapes safely
    return float(np.ravel(pred)[0])


def compute_fraud_score(path: str, model=None) -> dict:
    """
    Combined fraud score using CNN + forensics.
    Output fraud_score is 0–100.
    """
    cnn_prob = cnn_fraud_probability(path, model=model)

    ela = float(ela_score(path))
    sharp = float(sharpness_score(path))
    clone = float(clone_detection(path))

    # Your weighted scoring (0–100)
    final = (
        (cnn_prob * 0.5)
        + (ela * 0.2)
        + ((1 - sharp) * 0.15)
        + (clone * 0.15)
    ) * 100

    return {
        "fraud_score": round(final, 2),
        "cnn_fake_probability": round(cnn_prob, 3),
        "ela_artifact_score": round(ela, 3),
        "clone_region_score": round(clone, 3),
        "sharpness_score": round(sharp, 3),
    }
