import os
import cv2, numpy as np
from pdf2image import convert_from_path
from PIL import Image
import pathlib

# Optional: set this if Poppler isn't on PATH
POPPLER_PATH = os.getenv("POPPLER_PATH")  # e.g., C:\poppler\Library\bin

def _load_as_image(path):
    p = pathlib.Path(path)
    if p.suffix.lower() == ".pdf":
        kwargs = {"dpi": 300}
        if POPPLER_PATH:
            kwargs["poppler_path"] = POPPLER_PATH
        pages = convert_from_path(str(p), **kwargs)  # list of PIL Images
        pil_img = pages[0]
        # PIL (RGB) -> OpenCV BGR
        return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    # image file
    return cv2.imread(str(p), cv2.IMREAD_COLOR)

def _deskew(gray):
    edges = cv2.Canny(gray, 50, 150)
    coords = np.column_stack(np.where(edges > 0))
    angle = 0.0
    if len(coords) > 0:
        rect = cv2.minAreaRect(coords)
        angle = rect[-1]
        angle = -(90 + angle) if angle < -45 else -angle
    (h, w) = gray.shape[:2]
    M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
    rot = cv2.warpAffine(gray, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return rot, float(angle)

def normalize_image(src, dst, dpi=300):
    img = _load_as_image(src)
    if img is None:
        raise ValueError(f"Could not read {src}")
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    d = cv2.fastNlMeansDenoising(g, h=7)
    rot, angle = _deskew(d)
    norm = cv2.convertScaleAbs(rot, alpha=1.2, beta=10)
    # Save as PNG @300 DPI
    Image.fromarray(norm).save(str(dst), dpi=(dpi, dpi))
    h, w = norm.shape[:2]
    return {"w": int(w), "h": int(h), "deskew_deg": angle, "denoise_strength": 7}
