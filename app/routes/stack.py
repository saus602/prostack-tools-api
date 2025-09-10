from fastapi import APIRouter, Depends, Request
from app.models import OptimizeReq, OptimizeResp
from app.deps import require_license
from app.core.rules_engine import optimize_stack

router = APIRouter(dependencies=[Depends(require_license)])

@router.post("/stack/optimize", response_model=OptimizeResp)
def optimize(req: OptimizeReq, request: Request):
    sequence, total = optimize_stack(req.goals or {}, req.constraints or {})
    return OptimizeResp(sequence=sequence, estimated_total_limit=total)
