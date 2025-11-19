from fra_preproc.qr_detector import QRDetector
from ocr.tesseract_ocr import AadhaarTesseractOCR

IMAGE = "sample_aadhaar.jpg"

# Step 1: detect QR (optional)
qr = QRDetector("runs/detect/train9/weights/best.pt")
crop, box = qr.detect_and_crop(IMAGE)

# Step 2: run OCR
ocr = AadhaarTesseractOCR()
text = ocr.extract_text(IMAGE)

print("\n=== OCR RAW TEXT ===")
print(text)

fields = ocr.parse_fields(text)
print("\n=== PARSED FIELDS ===")
print(fields)
