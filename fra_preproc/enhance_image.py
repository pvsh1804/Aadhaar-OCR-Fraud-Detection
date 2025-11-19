import cv2

def enhance_for_ocr(image_path, out_path="enhanced.png"):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    bin_img = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 10
    )

    denoise = cv2.fastNlMeansDenoising(bin_img, h=15)

    h, w = denoise.shape
    sharp = cv2.resize(denoise, (w * 2, h * 2), interpolation=cv2.INTER_CUBIC)

    cv2.imwrite(out_path, sharp)
    return out_path
