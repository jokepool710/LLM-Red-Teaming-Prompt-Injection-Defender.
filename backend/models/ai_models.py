from pydantic import BaseModel, Field

class ThreatRequest(BaseModel):
    text: str = Field(..., min_length=5, description="Input text to analyze for prompt injection")

class ThreatResponse(BaseModel):
    threat_level: str
    confidence: float
    details: str
