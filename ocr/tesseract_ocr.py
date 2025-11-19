import pytesseract
from PIL import Image
import re
import cv2
import numpy as np

# path for windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class AadhaarTesseractOCR:

    def enhance(self, img_path):
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        norm = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
        blur = cv2.medianBlur(norm, 3)
        out = "enhanced_tess.jpg"
        cv2.imwrite(out, blur)
        return out

    def extract_text(self, img_path):
        enhanced = self.enhance(img_path)

        text = pytesseract.image_to_string(
            Image.open(enhanced),
            lang="eng+hin+guj",     # MULTILINGUAL OCR
            config="--psm 6"        # Assume text block
        )
        return text

    def parse_fields(self, text):
        fields = {}

        # Aadhaar number
        aadhaar = re.search(r"\b\d{4}\s\d{4}\s\d{4}\b", text)
        fields["aadhaar_number"] = aadhaar.group(0) if aadhaar else None

        # DOB
        dob = re.search(r"\b\d{2}/\d{2}/\d{4}\b", text)
        fields["dob"] = dob.group(0) if dob else None

        # Gender
        if "MALE" in text.upper():
            fields["gender"] = "MALE"
        elif "FEMALE" in text.upper():
            fields["gender"] = "FEMALE"
        else:
            fields["gender"] = None

        # Name (line above DOB)
        lines = text.split("\n")
        name = None
        for i, line in enumerate(lines):
            if "DOB" in line:
                if i > 0:
                    name = lines[i - 1].strip()
                break
        fields["name"] = name

        return fields
