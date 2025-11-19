from PIL import Image

def crop_text_region(image_path, qr_box, out_path="text_region.png"):
    """
    Crop the left side of the Aadhaar (where English text is) using the QR box as reference.
    qr_box is (x1, y1, x2, y2) from YOLO on the SAME image.
    """
    img = Image.open(image_path).convert("RGB")
    w, h = img.size

    x1, y1, x2, y2 = qr_box

    # Region: left of QR, ignore bottom Hindi line
    left = 0
    top = int(h * 0.10)      # skip a bit of top header
    right = max(10, x1 - 10) # stop just before QR code
    bottom = int(h * 0.85)   # skip bottom Hindi slogan

    # Safety clamp
    left = max(0, left)
    top = max(0, top)
    right = min(w, right)
    bottom = min(h, bottom)

    if right <= left or bottom <= top:
        # fallback – return original
        img.save(out_path)
        return out_path

    roi = img.crop((left, top, right, bottom))
    roi.save(out_path)
    return out_path
