import cv2
from fra_preproc.qr_detector import QRDetector

# --------------------------
# CONFIG
# --------------------------
MODEL_PATH = "runs/detect/train9/weights/best.pt"
TEST_IMAGE = "C:/Users/nikku/projects/AlOCR_Project/data/raw/aadhar_dataset/train/images/6cc303eb6be78797fd871ec8cad3a65d_jpg.rf.414442c3565448f06e11aedcb8634be1.jpg"   # <-- put your test image path here

# --------------------------
# RUN TEST
# --------------------------
detector = QRDetector(model_path=MODEL_PATH)

print("🔍 Running QR detection...")

crop, bbox = detector.detect_and_crop(TEST_IMAGE)

if crop is None:
    print("❌ No QR code detected!")
else:
    print("✅ QR detected at:", bbox)

    # show QR crop
    cv2.imshow("QR Crop", crop)
    cv2.waitKey(0)

    # decode QR
    text = detector.decode_qr(crop)

    if text:
        print("\n✅ Decoded QR:")
        print(text)
    else:
        print("\n❌ Could not decode QR text.")