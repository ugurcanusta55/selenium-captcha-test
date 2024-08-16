import cv2
import pytesseract
import numpy as np


def base64_to_cv_image(image):
    open_cv_image = np.array(image)
    if open_cv_image.shape[2] == 3:  # Renkli görüntü için RGB'den BGR'ye dönüşüm
        open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
    return open_cv_image


def preprocess_image(image):
    # Gri tonlamaya çevir
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Binarize et (siyah-beyaz görüntü)
    _, binary_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)
    
    # Gürültüyü azaltmak için Gaussian blur kullan
    processed_image = cv2.GaussianBlur(binary_image, (1, 1), 0)
    
    return processed_image


# Metin çıkarma fonksiyonu
def image_to_text(image):
    # OCR yapılandırması: Hem harf hem rakam içeren config
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    
    # Görüntüden metin çıkarma
    text = pytesseract.image_to_string(image, config=custom_config)
    return text
