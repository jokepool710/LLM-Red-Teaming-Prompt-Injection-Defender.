from fastapi import APIRouter
from models.ai_models import ThreatRequest, ThreatResponse
from services.ai_service import analyze_prompt
from utils.logger import logger

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/analyze", response_model=ThreatResponse)
async def analyze_endpoint(request: ThreatRequest):
    logger.info(f"Received input: {request.text}")
    return analyze_prompt(request.text)

