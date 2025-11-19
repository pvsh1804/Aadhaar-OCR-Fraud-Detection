import os
import cv2
import qrcode
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import json

# ==============================
#  CONFIG
# ==============================
WIDTH, HEIGHT = 640, 400
OUTPUT_CLEAN = "fraud_detection/dataset/ai_generated/clean/"
OUTPUT_DEFECT = "fraud_detection/dataset/ai_generated/defective/"
FONT_PATH = "C:\\Windows\\Fonts\\arial.ttf"   # change if needed

# Random name components
FIRST_NAMES = ["Rohan", "Amit", "Sanjay", "Vivek", "Anjali", "Priya", "Kiran", "Sneha"]
LAST_NAMES = ["Patil", "Sharma", "Khan", "Joshi", "Mehta", "Deshmukh", "Gupta"]

# ==============================
#  Generate Synthetic Face (solid color block)
# ==============================
def generate_fake_face():
    img = np.full((160, 120, 3), (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200)),
                  dtype=np.uint8)
    cv2.putText(img, "PHOTO", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
    return img


# ==============================
#  Generate Random Aadhaar Info
# ==============================
def generate_random_data():
    name = random.choice(FIRST_NAMES) + " " + random.choice(LAST_NAMES)
    year = random.randint(1980, 2004)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    dob = f"{day:02d}/{month:02d}/{year}"
    gender = random.choice(["MALE", "FEMALE"])
    uid = "".join(str(random.randint(0, 9)) for _ in range(12))

    qr_data = {
        "uid": uid,
        "name": name,
        "dob": dob,
        "gender": gender,
        "address": "MG Road, Pune"
    }

    return name, dob, gender, uid, qr_data


# ==============================
#  Generate QR Code (JSON)
# ==============================
def generate_qr(qr_json):
    qr = qrcode.QRCode(version=1, box_size=2, border=1)
    qr.add_data(json.dumps(qr_json))
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    img = img.resize((120, 120))
    return np.array(img)


# ==============================
#  Create Aadhaar Layout
# ==============================
def create_card(name, dob, gender, uid, qr_img, face_img):
    canvas = Image.new("RGB", (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(FONT_PATH, 22)
    small_font = ImageFont.truetype(FONT_PATH, 18)

    # Header Text
    draw.text((20, 20), "Government of India", fill=(0,0,0), font=font)

    # Insert fake face
    face_pil = Image.fromarray(face_img)
    canvas.paste(face_pil, (20, 80))

    # Insert QR
    qr_pil = Image.fromarray(qr_img)
    canvas.paste(qr_pil, (500, 20))

    # Text fields
    draw.text((160, 90), name, fill=(0,0,0), font=font)
    draw.text((160, 135), f"DOB: {dob}", fill=(0,0,0), font=font)
    draw.text((160, 180), gender, fill=(0,0,0), font=font)
    draw.text((160, 230), f"{uid[:4]} {uid[4:8]} {uid[8:]}", fill=(0,0,0), font=font)

    return np.array(canvas)


# ==============================
#  Apply Defects
# ==============================
def apply_defects(img):
    defective = img.copy()

    # Random blur
    if random.random() < 0.4:
        defective = cv2.GaussianBlur(defective, (5,5), 0)

    # Noise
    if random.random() < 0.4:
        noise = np.random.normal(0, 12, defective.shape).astype(np.uint8)
        defective = cv2.add(defective, noise)

    # Brightness/contrast shift
    if random.random() < 0.4:
        alpha = random.uniform(0.7, 1.3)
        beta = random.randint(-20, 20)
        defective = cv2.convertScaleAbs(defective, alpha=alpha, beta=beta)

    # Shadow overlay
    if random.random() < 0.2:
        shadow = np.zeros_like(defective, dtype=np.uint8)
        cv2.rectangle(shadow, (0,0), (random.randint(200,450), random.randint(150,350)), (50,50,50), -1)
        defective = cv2.addWeighted(defective, 0.8, shadow, 0.5, 0)

    # JPEG compression
    if random.random() < 0.5:
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), random.randint(20, 60)]
        _, enc = cv2.imencode('.jpg', defective, encode_param)
        defective = cv2.imdecode(enc, 1)

    return defective


# ==============================
#  Main Generator Function
# ==============================
def generate_dataset(count=150):
    for i in range(count):
        name, dob, gender, uid, qr_json = generate_random_data()
        face = generate_fake_face()
        qr_img = generate_qr(qr_json)

        card = create_card(name, dob, gender, uid, qr_img, face)

        clean_path = os.path.join(OUTPUT_CLEAN, f"clean_{i}.jpg")
        cv2.imwrite(clean_path, card)

        defective = apply_defects(card)
        defect_path = os.path.join(OUTPUT_DEFECT, f"defect_{i}.jpg")
        cv2.imwrite(defect_path, defective)

        print(f"[{i+1}/{count}] Generated synthetic Aadhaar images.")

    print("\n✔ Dataset generation completed!")


if __name__ == "__main__":
    generate_dataset(150)
