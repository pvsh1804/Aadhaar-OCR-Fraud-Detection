# create_dirs.py
import os

root = "fraud_detection/dataset/ai_generated/"

sub = ["clean", "defective"]
for s in sub:
    os.makedirs(os.path.join(root, s), exist_ok=True)

print("✔ AI dataset folders created.")
