
from fastapi import APIRouter, HTTPException
from services.review_queue import list_pending, update_status

router = APIRouter(prefix="/review", tags=["Review"])

@router.get("/pending")
def pending(limit: int = 50):
    rows = list_pending(limit)
    pending = []
    for r in rows:
        pending.append({"id": r[0], "prompt": r[1], "label": r[2], "score": r[3], "metadata": r[4], "created_at": r[5]})
    return {"pending": pending}

@router.post("/resolve")
def resolve(payload: dict):
    rid = int(payload.get("id"))
    action = payload.get("action")
    note = payload.get("note", "")
    update_status(rid, action, resolution=note)
    return {"ok": True}
