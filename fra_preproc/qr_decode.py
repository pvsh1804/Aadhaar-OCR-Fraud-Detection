import cv2

def try_decode_qr(img_path):
    img = cv2.imread(str(img_path))
    if img is None:
        return None
    det = cv2.QRCodeDetector()
    data, points, _ = det.detectAndDecode(img)
    if points is not None and data:
        ok = len(data) > 10
        return {"payload": data, "ok": ok}
    return None
