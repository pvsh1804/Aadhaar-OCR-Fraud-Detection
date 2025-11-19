import cv2
import numpy as np
from skimage import exposure
import imutils


class ImageCleaner:

    def enhance(self, img_path):
        """Returns a cleaned image optimized for QR + OCR"""

        img = cv2.imread(img_path)

        # 1️⃣ Rotate automatically (deskew)
        rotated = self.auto_rotate(img)

        # 2️⃣ Denoise
        den = cv2.fastNlMeansDenoisingColored(rotated, None, 10, 10, 7, 21)

        # 3️⃣ Sharpening
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        sharp = cv2.filter2D(den, -1, kernel)

        # 4️⃣ Increase contrast (CLAHE)
        lab = cv2.cvtColor(sharp, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        lab = cv2.merge((cl, a, b))
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        out = "cleaned.jpg"
        cv2.imwrite(out, enhanced)
        return out

    def auto_rotate(self, img):
        """Auto deskew using largest contour text region"""

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        contours = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        if not contours:
            return img

        cnt = max(contours, key=cv2.contourArea)
        rect = cv2.minAreaRect(cnt)
        angle = rect[-1]

        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        return imutils.rotate(img, angle)
