from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import base64
import requests
import io
import time

# PNG'yi JPEG'e dönüştüren fonksiyon (disk yerine bellek kullanır)
def convert_png_2_jpeg(png_data):
    # BytesIO kullanarak PNG'yi aç
    png_image = Image.open(io.BytesIO(png_data))

    # JPEG formatına dönüştürmek için yeni bir RGB resim oluştur
    jpeg_image = Image.new("RGB", png_image.size, (255, 255, 255))
    jpeg_image.paste(png_image, mask=png_image.split()[3])

    # JPEG'i bellek içinde kaydetmek için BytesIO kullan
    jpeg_bytes = io.BytesIO()
    jpeg_image.save(jpeg_bytes, format="JPEG")
    
    # JPEG'i base64 formatına dönüştür
    return base64.b64encode(jpeg_bytes.getvalue()).decode('utf-8')

if __name__ == "__main__":
    # Sabitler
    LOGIN_URL = "https://google.com.tr/"
    API_URL = "http://0.0.0.0:8000/"
    USERNAME = "username"
    PASSWORD = "pwd"

    # WebDriver başlat
    driver = webdriver.Chrome()

    try:
        driver.get(LOGIN_URL)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ui-button-text")))

        # Modal düğmesine tıkla
        modal_button = driver.find_element(by=By.CLASS_NAME, value="ui-button-text")
        modal_button.click()

        # Username, password ve captcha elemanlarını bul
        username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        password = driver.find_element(by=By.ID, value="password")
        txtCaptcha = driver.find_element(by=By.ID, value="txtCaptcha")
        img_kod = driver.find_element(by=By.ID, value="imgKod")

        # Captcha base64 verisini al
        img_data = img_kod.get_attribute("src")
        base64_data = img_data.split(",")[1]

        # Base64'ü decode et ve PNG verisini bellekte işle
        png_data = base64.b64decode(base64_data)

        # PNG'yi JPEG'e dönüştür ve base64'e çevir
        jpeg_base64 = convert_png_2_jpeg(png_data)

        # API'ye POST isteği gönder
        res = requests.post(API_URL, json={"img_data": jpeg_base64})
        captcha_text = res.json().get("message", "").replace("\n", "")
        print("captcha_text", captcha_text)

        # Formu doldur
        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)
        txtCaptcha.send_keys(captcha_text)

        time.sleep(3)  # Gözlemleme amaçlı süre
    finally:
        driver.quit()
