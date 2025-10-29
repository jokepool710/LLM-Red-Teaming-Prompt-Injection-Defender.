
from pydantic import BaseModel, Field

class ThreatRequest(BaseModel):
    prompt: str = Field(..., min_length=1)

class ThreatResponse(BaseModel):
    label: str
    score: float
    explanation: str
