import cv2
from realesrgan import RealESRGAN
from PIL import Image
import numpy as np

def upscale_image(input_path, output_path="superres_output.png"):
    model = RealESRGAN("cuda", scale=4)  # use "cpu" if no GPU
    model.load_weights(RealESRGAN.weights("RealESRGAN_x4plus"))
    
    img = Image.open(input_path).convert("RGB")
    sr = model.predict(img)
    sr.save(output_path)

    return output_path
