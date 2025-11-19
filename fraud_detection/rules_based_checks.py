import cv2
import numpy as np
from PIL import Image, ImageChops, ImageEnhance

def ela_score(path):
    """
    Error Level Analysis returns anomaly score (0–1)
    """
    original = Image.open(path)
    original.save("temp.jpg", quality=90)
    temp = Image.open("temp.jpg")

    diff = ImageChops.difference(original, temp)
    extrema = diff.getextrema()
    max_diff = max([ex[1] for ex in extrema])

    return max_diff / 255.0  # normalize

def sharpness_score(path):
    img = cv2.imread(path, 0)
    lap = cv2.Laplacian(img, cv2.CV_64F).var()
    return min(lap / 1000, 1.0)

def clone_detection(path):
    img = cv2.imread(path, 0)
    orb = cv2.ORB_create(2000)
    kp, des = orb.detectAndCompute(img, None)
    return 1 - min(len(kp) / 500, 1.0)
