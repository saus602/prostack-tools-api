from fastapi import APIRouter, Depends, Request
from app.models import ApplicationCreate, ApplicationResp, ApplicationStatusPatch
from app.deps import require_license
import uuid

router = APIRouter(dependencies=[Depends(require_license)])

# QS: In-memory "DB"
_APPS = {}

@router.post("/applications", response_model=ApplicationResp)
def create_app(req: ApplicationCreate, request: Request):
    app_id = uuid.uuid4().hex[:10]
    _APPS[app_id] = {"status":"created", "limit":None, "issuer": req.issuer, "card": req.card, "rank": req.rank}
    return ApplicationResp(application_id=app_id)

@router.patch("/applications/{app_id}/status")
def patch_app_status(app_id: str, payload: ApplicationStatusPatch, request: Request):
    if app_id not in _APPS:
        return {"ok": False, "error":"not_found"}
    _APPS[app_id].update({"status": payload.status, "limit": payload.limit, "notes": payload.notes})
    return {"ok": True, "application": _APPS[app_id]}
