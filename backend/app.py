import io, base64
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from PIL import Image, UnidentifiedImageError

from . import models
from .exceptions import *

# App configuration
app = FastAPI()
origins = ["http://localhost:3001"]
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_methods=["*"]
                   )

class Prediction(BaseModel):
    prediction: bool
    confidence: float = Field(..., ge=0, le=1)
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
    model = models.ResNet()
    inference_class, confidence = model.infere(image)
    inference = inference_class.lower() == 'pneumonia'
    response = Prediction(prediction=inference, confidence=confidence)
    return response