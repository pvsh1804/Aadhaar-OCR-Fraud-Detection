# app/models.py
from ultralytics import YOLO
from app.config import YOLO_QR_MODEL_PATH

# -------------------------------------------------
# Only YOLO model lives here
# Fraud CNN is loaded lazily in fraud_detector.py
# -------------------------------------------------
qr_detector = YOLO(YOLO_QR_MODEL_PATH)
