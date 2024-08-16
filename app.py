import base64
from PIL import Image
from fastapi import FastAPI
from pydantic import BaseModel
import io
from captcha_solver import base64_to_cv_image, preprocess_image, image_to_text

app = FastAPI()

class ImageData(BaseModel):
    img_data: str


@app.post("/")
async def root(image: ImageData):
    img_data = image.img_data
    if img_data.startswith('data:image/png;base64,'):
        img_data = img_data.replace('data:image/png;base64,', '')
    image_data = base64.b64decode(img_data)
    image = Image.open(io.BytesIO(image_data))
    
    # Görüntüyü işlemeye tabi tut
    open_cv_image = base64_to_cv_image(image)
    processed_image = preprocess_image(open_cv_image)
    
    # OCR işlemi (metin çıkarma)
    text = image_to_text(processed_image)
    return {"message": text}
