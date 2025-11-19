🇮🇳 Aadhaar OCR & Fraud Detection System
AI-Powered OCR • QR Parsing • Fraud Detection • Synthetic Aadhaar Generator
📌 Overview

This project provides a complete end-to-end pipeline for processing Aadhaar card images using Artificial Intelligence.

It includes:

Aadhaar text extraction (OCR) using Tesseract + PaddleOCR

QR code reading (XML & JSON UIDAI formats)

QR detection using YOLOv8

Fraud/Tampering Detection using CNN + Image Forensics

Synthetic Aadhaar dataset generation

Training pipeline for deep-learning fraud classifier

This system works on real, low-quality, blurred, and compressed Aadhaar images.

🧱 Features

✔ OCR Extraction

Extracts Name, DOB, Gender, Aadhaar Number

Uses Tesseract OCR + preprocessing

Multi-language support (hin, eng, guj)

✔ QR Code Processing

Detects QR using YOLOv8

Decodes Aadhaar QR (XML + JSON)

Validates QR data

✔ Fraud Detection

CNN classifier trained on synthetic vs real Aadhaar images

ELA (Error Level Analysis)

Sharpness & Blur detection

Copy-Move cloning detection

Final combined fraud score

✔ Synthetic Aadhaar Dataset Generation

Generates thousands of synthetic Aadhaar-like images

Auto QR embedding

Random fonts, text positions, degradations

Tampered images for fraud model training

🎯 Milestones Completed
🚀 Milestone 1 — Aadhaar OCR + QR Reader

Includes:

Image preprocessing

Tesseract + PaddleOCR extraction

Field parsing using regex

YOLO-based QR detection

Full merged output (OCR + QR)

🔍 Milestone 2 — Fraud Detection Model

Includes:

Custom CNN classifier

Training on synthetic and real Aadhaar images

Tampering detection (ELA, blur, cloning, artifacts)

Unified fraud scoring system

🧪 Milestone 3 — Synthetic Aadhaar Image Generator

Includes:

Automated Aadhaar image generator

Random: name, gender, DOB, UID, fonts

QR embedding (JSON format)

Random distortions: blur, noise, scratches, compression

Output size: 640×400

Used to train the fraud model

🧩 System Architecture
Input Image
    │
    ├── QR Detection (YOLOv8)
    │       └── QR Parsing (XML + JSON)
    │
    ├── OCR Extraction (Tesseract/PaddleOCR)
    │
    └── Field Merging (Best Match)
            │
            ▼
    Fraud Detection Engine
        ├── CNN Fake Probability
        ├── ELA Artifact Score
        ├── Clone Region Score
        ├── Sharpness Score
        └── Final Fraud Score

📦 Folder Structure
Aadhaar-OCR-Fraud-Detection/
│
├── ocr/
│   ├── tesseract_ocr.py
│   └── paddle_ocr.py
│
├── qr_reader/
│   └── qr_detector.py
│
├── fraud_detection/
│   ├── fraud_detector.py
│   ├── train_fraud_model.py
│   ├── generate_ai_aadhaar.py
│   └── model/
│
├── dataset/
│   ├── real/
│   ├── synthetic/
│
├── test_ocr.py
├── test_fraud.py
├── README.md
└── requirements.txt

⚙️ Installation

Clone repo
git clone https://github.com/<your-username>/Aadhaar-OCR-Fraud-Detection

Create virtual environment
python -m venv venv

Activate

Windows: venv\Scripts\activate

Linux/Mac: source venv/bin/activate

Install dependencies
pip install -r requirements.txt

▶️ Usage
1. Run OCR

python test_ocr.py

2. Run Fraud Detection

python test_fraud.py

3. Generate Synthetic Aadhaar Dataset

python fraud_detection/generate_ai_aadhaar.py

4. Train Fraud Model

python fraud_detection/train_fraud_model.py

📚 Module Descriptions
OCR Module

Extracts necessary Aadhaar details:

Name

Aadhaar Number

DOB

Gender

QR Module

Parses Aadhaar QR (UIDAI JSON/XML).
Used for authenticity validation.

Fraud Detection

Combines:

Deep learning (CNN)

Image forensics

Blur / Sharpness detection
