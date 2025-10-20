from fastapi import APIRouter
from pydantic import BaseModel
from services.ai_service import analyze_prompt

router = APIRouter(prefix="/ai", tags=["AI"])

class AnalyzeRequest(BaseModel):
    prompt: str

@router.post("/analyze")
async def analyze_route(req: AnalyzeRequest):
    res = analyze_prompt(req.prompt)
    return {"result": res}
