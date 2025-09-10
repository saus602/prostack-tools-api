from fastapi import APIRouter, Depends, Request
from app.models import PrequalRunRequest, PrequalOffer
from app.deps import require_license

router = APIRouter(dependencies=[Depends(require_license)])

@router.post("/prequal/run", response_model=list[PrequalOffer])
def run_prequal(req: PrequalRunRequest, request: Request):
    # Mock results; swap with aggregator/partners later.
    return [
        {"issuer":"Amex", "product":"Blue Business Plus", "apr_range":"18.49-26.49%", "notes":"Firm prequal"},
        {"issuer":"Chase", "product":"Ink Business Unlimited", "apr_range":"See terms", "notes":"Soft match"},
    ]
