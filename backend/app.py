from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

# App configuration
app = FastAPI()
origins = ["http://localhost:3001"]
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_methods=["*"]
                   )

# Routes definitions
@app.post("/predict")
async def predict(file: UploadFile):
    file_content = await file.read()
    with open('fle.jpeg', 'wb') as fle:
        fle.write(file_content)
    return {'prediction': False, 'confidence': 0.0} 