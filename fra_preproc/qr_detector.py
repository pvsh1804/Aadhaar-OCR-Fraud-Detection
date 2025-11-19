from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import zxingcpp

class QRDetector:
    def __init__(self, model_path="runs/detect/train9/weights/best.pt"):
        """
        Initialize YOLO QR detector.
        Update model_path to point to your trained best.pt file.
        """
        self.model = YOLO(model_path)

    def detect_and_crop(self, image_path):
        """
        Detect QR bounding box using YOLO and return cropped QR region.
        """
        results = self.model(image_path)[0]

        # No detections found
        if len(results.boxes) == 0:
            return None, None

        # Select biggest detected box (QR is usually largest)
        boxes = results.boxes.xyxy.cpu().numpy()
        x1, y1, x2, y2 = boxes[0].astype(int)

        # Load image
        img = cv2.imread(image_path)

        if img is None:
            print(f"ERROR: Cannot read image {image_path}")
            return None, None

        # Crop QR region
        crop = img[y1:y2, x1:x2]

        return crop, (x1, y1, x2, y2)

    def decode_qr(self, crop):
        """
        Decode QR code using ZXingCPP.
        """
        if crop is None:
            return None
        
        pil_img = Image.fromarray(crop)
        result = zxingcpp.read_barcodes(pil_img)

        if result:
            return result[0].text
        
        return None
