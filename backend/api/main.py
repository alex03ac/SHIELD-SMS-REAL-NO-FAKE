from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PLN.preprocessing import normalize
from ModeloML.rules_model import classify_text

app = FastAPI(title="Shield-SMS API", version="1.0.0")

class ClassifyRequest(BaseModel):
    message: str

class ClassifyResponse(BaseModel):
    label: str
    score: float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/classify", response_model=ClassifyResponse)
def classify(req: ClassifyRequest):
    try:
        text = normalize(req.message)
        label, score = classify_text(text)
        return ClassifyResponse(label=label, score=score)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
