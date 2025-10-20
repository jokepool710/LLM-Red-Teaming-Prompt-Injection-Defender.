# backend/routers/ai_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.ai_service import ai_service

router = APIRouter()

class ThreatInput(BaseModel):
    text: str

@router.post("/predict")
def predict_threat(input_data: ThreatInput):
    try:
        result = ai_service.analyze_text(input_data.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
