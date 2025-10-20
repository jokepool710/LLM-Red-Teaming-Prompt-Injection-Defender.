from fastapi import APIRouter
from services.ai_service import model

router = APIRouter(prefix="/ai", tags=["AI"])

@router.get("/test")
def test_ai():
    return 
