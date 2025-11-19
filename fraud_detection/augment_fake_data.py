import os
import cv2
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
REAL_DIR = BASE_DIR / "dataset" / "real"
FAKE_DIR = BASE_DIR / "dataset" / "fake"

FAKE_DIR.mkdir(parents=True, exist_ok=True)


def add_gaussian_noise(image):
    row, col, ch = image.shape
    mean = 0
    sigma = 15
    gauss = np.random.normal(mean, sigma, (row, col, ch)).reshape(row, col, ch)
    noisy = image + gauss
    noisy = np.clip(noisy, 0, 255).astype(np.uint8)
    return noisy


def blur_region(image):
    h, w = image.shape[:2]
    # take central region as "suspicious" (where photo/text usually is)
    x1, y1 = int(w * 0.3), int(h * 0.3)
    x2, y2 = int(w * 0.7), int(h * 0.7)
    roi = image[y1:y2, x1:x2]
    roi_blur = cv2.GaussianBlur(roi, (35, 35), 0)
    fake = image.copy()
    fake[y1:y2, x1:x2] = roi_blur
    return fake


def add_text_overlay(image):
    fake = image.copy()
    h, w = fake.shape[:2]
    text = "UPDATED"
    cv2.putText(
        fake,
        text,
        (int(w * 0.05), int(h * 0.15)),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 0, 255),
        3,
        cv2.LINE_AA,
    )
    return fake


def add_rectangle_patch(image):
    fake = image.copy()
    h, w = fake.shape[:2]
    x1, y1 = int(w * 0.55), int(h * 0.55)
    x2, y2 = int(w * 0.9), int(h * 0.9)
    cv2.rectangle(fake, (x1, y1), (x2, y2), (255, 255, 255), -1)
    return fake


def generate_fake_images():
    image_files = [f for f in REAL_DIR.iterdir() if f.suffix.lower() in [".jpg", ".jpeg", ".png"]]
    print(f"Found {len(image_files)} real images")

    count = 0
    for img_path in image_files:
        img = cv2.imread(str(img_path))
        if img is None:
            print(f"Skipping {img_path}, cannot read")
            continue

        # 1. Noise
        noisy = add_gaussian_noise(img)
        cv2.imwrite(str(FAKE_DIR / f"{img_path.stem}_fake_noise.jpg"), noisy)

        # 2. Blur region
        blurred = blur_region(img)
        cv2.imwrite(str(FAKE_DIR / f"{img_path.stem}_fake_blur.jpg"), blurred)

        # 3. Text overlay
        overlay = add_text_overlay(img)
        cv2.imwrite(str(FAKE_DIR / f"{img_path.stem}_fake_overlay.jpg"), overlay)

        # 4. Rect patch
        rect = add_rectangle_patch(img)
        cv2.imwrite(str(FAKE_DIR / f"{img_path.stem}_fake_rect.jpg"), rect)

        count += 4

    print(f"Generated {count} fake images in {FAKE_DIR}")


if __name__ == "__main__":
    generate_fake_images()
