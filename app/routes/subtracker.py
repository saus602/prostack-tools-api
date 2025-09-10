from fastapi import APIRouter, Depends, Request
from app.deps import require_license

router = APIRouter(dependencies=[Depends(require_license)])

@router.get("/sub-tracker")
def sub_tracker(request: Request):
    # QS mock
    return {
        "summary": {"cards": 3, "progress_pct": 32},
        "items": [
            {"issuer":"Amex", "card":"BBP", "min_spend": 6000, "deadline_days": 90, "progress": 2100},
            {"issuer":"Chase", "card":"Ink Unlimited", "min_spend": 7500, "deadline_days": 90, "progress": 3200},
            {"issuer":"C1", "card":"Spark Cash Select", "min_spend": 4500, "deadline_days": 90, "progress": 600},
        ]
    }
