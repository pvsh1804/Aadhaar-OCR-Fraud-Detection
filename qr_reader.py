import cv2
import json
import re
from PIL import Image
from pyzbar.pyzbar import decode
import zxingcpp
import numpy as np
from ultralytics import YOLO


class AadhaarQRReader:

    def __init__(self, yolo_model_path="runs/detect/train9/weights/best.pt"):
        # Load YOLO QR Detector
        try:
            self.yolo = YOLO(yolo_model_path)
            self.use_yolo = True
        except Exception as e:
            print("⚠ YOLO model not found, fallback to direct QR decoding.")
            print(e)
            self.use_yolo = False

    # ---------------------------------------------------------
    # 1. YOLO QR DETECTION (crop QR region)
    # ---------------------------------------------------------
    def detect_qr_yolo(self, img_path):
        if not self.use_yolo:
            return None

        results = self.yolo(img_path)[0]

        if len(results.boxes) == 0:
            return None

        x1, y1, x2, y2 = results.boxes.xyxy[0].cpu().numpy().astype(int)

        img = cv2.imread(img_path)
        if img is None:
            return None

        crop = img[y1:y2, x1:x2]

        return crop

    # ---------------------------------------------------------
    # 2. Enhance QR Crop (CRITICAL FIX)
    # ---------------------------------------------------------
    def enhance_qr(self, crop):

        # Upscale
        crop = cv2.resize(crop, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        # GRAY
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

        # CLAHE contrast
        clahe = cv2.createCLAHE(clipLimit=3)
        gray = clahe.apply(gray)

        # Sharpen
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        sharp = cv2.filter2D(gray, -1, kernel)

        # Threshold
        thresh = cv2.adaptiveThreshold(
            sharp, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31, 3
        )
        return thresh

    # ---------------------------------------------------------
    # 3. Decode QR (ZXingCPP → Pyzbar → OpenCV)
    # ---------------------------------------------------------
    def decode_qr(self, crop):

        if crop is None:
            return None

        enhanced = self.enhance_qr(crop)
        pil_img = Image.fromarray(enhanced)

        # ZXing
        try:
            result = zxingcpp.read_barcodes(pil_img)
            if result:
                return result[0].text
        except:
            pass

        # Pyzbar
        try:
            decoded = decode(pil_img)
            if decoded:
                return decoded[0].data.decode("utf-8")
        except:
            pass

        # OpenCV
        try:
            qrd = cv2.QRCodeDetector()
            txt, pts, _ = qrd.detectAndDecode(enhanced)
            if txt:
                return txt
        except:
            pass

        return None

    # ---------------------------------------------------------
    # 4. Parse Aadhaar QR (JSON + XML)
    # ---------------------------------------------------------
    def parse_qr(self, qr_text):

        fields = {
            "aadhaar_number": None,
            "name": None,
            "dob": None,
            "gender": None,
            "address": None
        }

        # JSON format
        try:
            obj = json.loads(qr_text)
            fields["aadhaar_number"] = obj.get("uid")
            fields["name"] = obj.get("name")
            fields["dob"] = obj.get("dob")
            fields["gender"] = obj.get("gender")
            fields["address"] = obj.get("address")
            return fields
        except:
            pass

        # XML format
        if 'uid="' in qr_text:
            def get(tag):
                m = re.search(f'{tag}="(.*?)"', qr_text)
                return m.group(1) if m else None

            fields["aadhaar_number"] = get("uid")
            fields["name"] = get("name")
            fields["dob"] = get("dob") or get("yob")
            fields["gender"] = get("gender")
            fields["address"] = get("address")
            return fields

        return None

    # ---------------------------------------------------------
    # 5. Public Function for test_ocr.py
    # ---------------------------------------------------------
    def read_qr(self, img_path):

        # Try YOLO crop first
        crop = self.detect_qr_yolo(img_path)
        if crop is not None:
            text = self.decode_qr(crop)
            if text:
                return self.parse_qr(text)

        # ZXing direct
        try:
            result = zxingcpp.read_barcodes(Image.open(img_path))
            if result:
                return self.parse_qr(result[0].text)
        except:
            pass

        # Pyzbar direct
        try:
            decoded = decode(Image.open(img_path))
            if decoded:
                return self.parse_qr(decoded[0].data.decode("utf-8"))
        except:
            pass

        # OpenCV direct
        try:
            qrd = cv2.QRCodeDetector()
            txt, pts, _ = qrd.detectAndDecode(cv2.imread(img_path))
            if txt:
                return self.parse_qr(txt)
        except:
            pass

        return None


# Wrapper for test_ocr.py
_reader = AadhaarQRReader()

def read_aadhaar_qr(image_path):
    return _reader.read_qr(image_path)
