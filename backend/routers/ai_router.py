
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.ai_service import analyze_prompt
from services.policies import evaluate as eval_policy
from services.review_queue import enqueue
from utils.redact import redact_output
import json

router = APIRouter(prefix="/ai", tags=["AI"])

class AnalyzeRequest(BaseModel):
    prompt: str

class AnalyzeResponse(BaseModel):
    action: str
    result: dict

THRESHOLD_BLOCK = 0.9
THRESHOLD_QUEUE = 0.5

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_route(req: AnalyzeRequest):
    prompt = req.prompt
    # run policy checks first
    policy_action, reason = eval_policy(prompt)
    if policy_action == "BLOCK":
        return {"action":"BLOCK","result":{"label":"policy_block","score":1.0,"explanation":reason}}
    if policy_action == "REVIEW":
        rid = enqueue(prompt=prompt, label="policy_review", score=0.75, metadata=reason)
        return {"action":"QUEUE","result":{"queue_id":rid}}

    # call detector
    res = analyze_prompt(prompt)
    score = float(res.get("score", 0.0))
    if score >= THRESHOLD_BLOCK:
        return {"action":"BLOCK","result":res}
    if score >= THRESHOLD_QUEUE:
        rid = enqueue(prompt=prompt, label=res.get("label","unknown"), score=score, metadata=json.dumps(res))
        return {"action":"QUEUE","result":{"queue_id":rid, "analysis":res}}

    # ALLOW: redact outputs before returning
    res_out = res.copy()
    if "explanation" in res_out:
        res_out["explanation"] = redact_output(res_out.get("explanation",""))
    return {"action":"ALLOW","result":res_out}

