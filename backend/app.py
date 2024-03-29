import os
import io, base64
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from PIL import Image, UnidentifiedImageError

from . import models
from .exceptions import *

# App configuration
app = FastAPI()
origins = [f"http://localhost:{os.environ.get('FRONTEND_PORT')}", f"http://{os.environ.get('FRONTEND_IP')}:{os.environ.get('FRONTEND_PORT')}"]
print(origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Prediction(BaseModel):
    prediction: bool
    probability: float = Field(..., ge=0, le=1)
    detail: str = ''

# Routes definitions
@app.post("/predict")
async def predict(file: UploadFile) -> Prediction:
    # Handle image receiving
    allowed_exts = ['image/jpg', 'image/jpeg', 'image/png', 'jpg', 'jpeg', 'png']
    file_content = await file.read()

    # Validation
    if len(file_content) == 0: raise EmptyFile()
    if file.content_type.lower() not in allowed_exts: raise UnsupportedFormat(file.content_type)

    try:
        image = Image.open(io.BytesIO(file_content))
    except UnidentifiedImageError:
        decoded_image = base64.b64decode(file_content)
        image = Image.open(io.BytesIO(decoded_image))
    except OSError:
        raise BrokenImage(len(file_content))

    # Inference
    model = models.EfficientNet(weights_path='backend/weights/EfficientNetv2-SGD(0.001)-batch(4)-weightedloss.pth')
    inference_class, probability = model.infere(image)
    inference = inference_class.lower() == 'pneumonia'
    response = Prediction(prediction=inference, probability=probability)
    return response