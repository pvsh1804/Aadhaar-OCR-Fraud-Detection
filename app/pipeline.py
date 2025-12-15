# app/pipeline.py
import time
from ocr.tesseract_ocr import AadhaarTesseractOCR
from fraud_detection.fraud_detector import compute_fraud_score

# initialize once
ocr_engine = AadhaarTesseractOCR()


def analyze_image(image_path: str):
    start_time = time.time()

    # OCR
    enhanced = ocr_engine.enhance(image_path)
    raw_text = ocr_engine.extract_text(enhanced)
    extracted_data = ocr_engine.parse_fields(raw_text)

    # Fraud detection
    fraud_analysis = compute_fraud_score(image_path)

    # 🔥 THIS IS THE IMPORTANT PART
    score = fraud_analysis["fraud_score"]
    decision = "GENUINE" if score <= 15 else "SUSPECT"
    fraud_analysis["decision"] = decision

    return {
        "extracted_data": extracted_data,
        "ocr_meta": {
            "raw_text_preview": raw_text[:300]
        },
        "fraud_analysis": fraud_analysis,
        "meta": {
            "processing_time_ms": int((time.time() - start_time) * 1000)
        }
    }
