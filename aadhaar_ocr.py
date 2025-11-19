import re
from paddleocr import PaddleOCR

class AadhaarOCR:
    def __init__(self):
        self.ocr = PaddleOCR(lang='en')

    def extract_text(self, img_path):
        """Extract text from image using PaddleOCR"""
        result = self.ocr.ocr(img_path)
        lines = []

        for block in result:
            for line in block:
                lines.append(line[1][0])

        return "\n".join(lines)

    def parse_fields(self, text):
        fields = {}

        # -------------------------
        # BASIC CLEANING
        # -------------------------
        clean = text.replace("\n", " ").replace("-", " ")
        clean = clean.replace(":", " ").replace("|", " ")
        clean = " ".join(clean.split())

        # -------------------------
        # DIGIT CORRECTION
        # Fix common OCR mistakes
        # -------------------------
        corrected = (
            clean.replace("O", "0").replace("o", "0")
                 .replace("I", "1").replace("l", "1")
                 .replace("B", "8").replace("S", "5")
                 .replace("Z", "2")
        )

        # -------------------------
        # AADHAAR NUMBER EXTRACTION
        # Very tolerant regex (digits with noise)
        # -------------------------
        aadhaar = re.search(r"(?:\d[\s-]*){12,}", corrected)

        if aadhaar:
            num = re.sub(r"\D", "", aadhaar.group(0))  # keep ONLY digits
            num = num[:12]  # ensure exactly 12 digits
            fields["aadhaar_number"] = num if len(num) == 12 else None
        else:
            fields["aadhaar_number"] = None

        # -------------------------
        # DOB EXTRACTION
        # -------------------------
        dob = re.search(r"\b\d{2}/\d{2}/\d{4}\b", clean)
        fields["dob"] = dob.group(0) if dob else None

        # -------------------------
        # GENDER EXTRACTION
        # -------------------------
        if "male" in clean.lower():
            fields["gender"] = "MALE"
        elif "female" in clean.lower():
            fields["gender"] = "FEMALE"
        else:
            fields["gender"] = None

        # -------------------------
        # NAME EXTRACTION
        # Skip unwanted lines
        # -------------------------
        name = None
        for line in text.split("\n"):
            line_clean = line.strip()

            if ("Government" in line_clean or
                "DOB" in line_clean or
                "Male" in line_clean or
                "MALE" in line_clean or
                "Female" in line_clean or
                "FEMALE" in line_clean):
                continue

            # assume name has at least 2 words
            if len(line_clean.split()) >= 2:
                name = line_clean
                break

        fields["name"] = name

        return fields
