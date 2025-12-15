from fraud_detection.fraud_detector import compute_fraud_score

# -----------------------------------
# 1. SET IMAGE PATH
# -----------------------------------
image_path = "fake1.jpg"   # <-- change your Aadhaar image here

print(f"\n=== Running Fraud Detection on: {image_path} ===\n")

# -----------------------------------
# 2. COMPUTE FRAUD SCORE
# -----------------------------------
score = compute_fraud_score(image_path)

# -----------------------------------
# 3. PRINT RESULT
# -----------------------------------
print("\n=== FRAUD RESULT ===")
print(score)
