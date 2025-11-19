import cv2
import numpy as np
import imutils

def auto_rotate(image):
    """Rotate image based on text orientation score."""
    import pytesseract
    try:
        osd = pytesseract.image_to_osd(image)
        rot_angle = int(osd.split("Rotate:")[1].split("\n")[0].strip())
        rotated = imutils.rotate_bound(image, -rot_angle)
        return rotated
    except:
        return image


def deskew(image):
    """Deskew tilted Aadhaar card."""

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)

    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    coords = np.column_stack(np.where(thresh > 0))

    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    rotated = imutils.rotate_bound(image, angle)
    return rotated


def preprocess_image(path):
    """Final pipeline → load → rotate → deskew → return enhanced image."""
    img = cv2.imread(path)

    # 1. auto rotate
    img = auto_rotate(img)

    # 2. deskew tilt
    img = deskew(img)

    # 3. optional sharpen
    kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
    img = cv2.filter2D(img, -1, kernel)

    return img
