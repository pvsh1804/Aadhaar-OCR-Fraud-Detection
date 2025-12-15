# app/config.py

FRAUD_MODEL_PATH = "fraud_detection/model/fraud_cnn_keras"
YOLO_QR_MODEL_PATH = "uid.v2.yolov8/runs/detect/train/weights/best.pt"

FRAUD_THRESHOLD = 0.7

WEIGHTS = {
    "cnn": 0.5,
    "ela": 0.2,
    "clone": 0.2,
    "sharpness": 0.1
}
