# app/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import uuid
import os

from app.pipeline import analyze_image
from app.ui import router as ui_router

# ✅ create app FIRST
app = FastAPI(title="Aadhaar OCR Fraud Detection API")

# ✅ include UI router AFTER app is created
app.include_router(ui_router)


# -------------------------------
# Root endpoint (FIXES 404)
# -------------------------------
@app.get("/")
def root():
    return {
        "message": "Aadhaar OCR Fraud Detection API is running",
        "ui": "/ui",
        "docs": "/docs",
        "health": "/health",
        "analyze": "/analyze (POST)",
    }


# -------------------------------
# Health check
# -------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -------------------------------
# Analyze endpoint
# -------------------------------
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    os.makedirs("temp", exist_ok=True)

    file_ext = os.path.splitext(file.filename)[1] or ".jpg"
    temp_file = os.path.join("temp", f"{uuid.uuid4()}{file_ext}")

    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = analyze_image(temp_file)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
