from fastapi import APIRouter, Depends, Request
from app.models import IntakeRequest, IntakeResponse
from app.deps import require_license
import uuid

router = APIRouter(dependencies=[Depends(require_license)])

@router.post("/intake", response_model=IntakeResponse)
def create_intake(req: IntakeRequest, request: Request):
    # In the QS, we just mint a profile id. Persist later.
    profile_id = req.email + "-" + uuid.uuid4().hex[:6]
    return IntakeResponse(profile_id=profile_id)
