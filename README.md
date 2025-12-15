📌 Aadhaar OCR & Fraud Detection System (AlOCR)

An end-to-end AI-powered system for Aadhaar card OCR extraction and fraud detection, combining image preprocessing, OCR, QR validation, and deep learning–based forgery detection, delivered with a FastAPI backend and interactive UI.

🚀 Project Overview

The Aadhaar OCR & Fraud Detection system aims to:

Extract Aadhaar details accurately from images

Validate UID using OCR + QR cross-verification

Detect tampering and forgery using CNN and forensic techniques

Provide a user-friendly web interface for verification

Expose APIs for easy integration with external systems

🧩 Technology Stack

Backend: FastAPI, Python

OCR: Tesseract OCR

Computer Vision: OpenCV, Pyzbar

Deep Learning: TensorFlow / Keras (CNN)

Fraud Detection: ELA, Clone Detection, Sharpness Analysis

UI: HTML, CSS, JavaScript (served via FastAPI)

Deployment: Render (API), GitHub

🟢 Milestone 1: Image Preprocessing & Data Preparation
📅 Objective

Prepare Aadhaar images to ensure high OCR accuracy under real-world conditions.

✅ Key Deliverables

Image normalization and resizing

Skew and rotation correction

Noise removal and contrast enhancement

Dataset organization for training and testing

🔧 Features Implemented

Resolution standardization for OCR input

Deskewing rotated Aadhaar images

Preprocessing pipeline for consistent OCR results

Support for multiple image formats (JPG, PNG, JPEG)

📈 Outcome

Significant improvement in OCR readability

Stable preprocessing pipeline for downstream tasks

🟡 Milestone 2: OCR Extraction & QR Code Processing
📅 Objective

Extract Aadhaar details reliably using OCR and QR-based validation.

✅ Key Deliverables

English OCR extraction using Tesseract

QR code detection and decoding

Regex-based parsing for Aadhaar fields

Fallback OCR when QR is missing

🔧 Features Implemented

Extraction of Name, DOB, Gender, Aadhaar Number

QR detection using OpenCV and Pyzbar

Cross-validation of UID from OCR and QR

UID format and checksum validation

📈 Outcome

Reliable Aadhaar data extraction

Reduced dependency on QR-only verification

Robust fallback mechanisms

🔵 Milestone 3: Fraud Detection Logic & Rule-Based Analysis
📅 Objective

Detect Aadhaar tampering and inconsistencies using rule-based fraud checks.

✅ Key Deliverables

UID mismatch detection

Rule-based fraud flag generation

Aggregation of multiple fraud indicators

Decision logic (Genuine vs Suspicious)

🔧 Features Implemented

OCR–QR UID cross-verification

Fraud flag generation on mismatch

Regex and checksum-based UID validation

Initial fraud scoring logic

📈 Outcome

Early detection of forged or tampered Aadhaar cards

Explainable fraud indicators for audit and review

🔴 Milestone 4: AI-Based Forgery Detection, UI & Deployment
📅 Objective

Integrate deep learning, build UI, and deploy the system.

✅ Key Deliverables

CNN-based forgery detection model

Image forensics (ELA, clone detection, sharpness)

Final fraud score scaling (0–10)

Web UI and API deployment

🔧 Features Implemented

CNN model to detect forged Aadhaar images

Error Level Analysis (ELA) for compression artifacts

Clone region detection for copy-paste fraud

Sharpness scoring for blur detection

Weighted fraud score (0–10 scale)

Final decision: Genuine / Suspicious

Interactive web UI for upload & verification

REST API (/analyze) with JSON response

Deployment on Render

📈 Outcome

End-to-end production-ready system

User-friendly UI + scalable API

Explainable and measurable fraud detection

🌐 API Endpoints
Endpoint	Method	Description
/	GET	Root status
/health	GET	Health check
/analyze	POST	Aadhaar OCR + Fraud analysis
/docs	GET	Swagger API docs
📊 Sample Output

<img width="860" height="560" alt="Screenshot (84)" src="https://github.com/user-attachments/assets/7e7a716a-cb8a-41bd-adab-bcd8dcc2ecba" /> 

<img width="860" height="560" alt="Screenshot (83)" src="https://github.com/user-attachments/assets/7362b7ad-183c-4670-b805-2f5a001d44f9" />

<img width="860" height="560" alt="Screenshot (85)" src="https://github.com/user-attachments/assets/ca18c513-0677-497e-8e9c-62cb777afa46" />

🏁 Final Status


✅ All milestones completed successfully
✅ System tested with real and synthetic samples
✅ Ready for academic submission and demo

👨‍💻 Author

Prakhar Vishwakarma
B.Tech CSE (AI & DS)
MIT World Peace University, Pune
