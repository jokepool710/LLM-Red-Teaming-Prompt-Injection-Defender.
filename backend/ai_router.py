from fastapi import APIRouter
from services.ai_service import analyze_prompt

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/analyze")
async def analyze_prompt_route(payload: dict):
    text = payload.get("prompt", "")
    result = analyze_prompt(text)
    return {"result": result}
