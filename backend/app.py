from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

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
    detail: str = None

# Routes definitions
@app.post("/predict")
async def predict(file: UploadFile) -> Prediction:
    file_content = await file.read()
    with open('fle.jpeg', 'wb') as fle:
        fle.write(file_content)
    return Prediction(prediction=True, confidence=0.0)