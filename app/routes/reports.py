from fastapi import APIRouter, Depends, UploadFile, File, Form, Request
from app.models import CreditMetrics
from app.deps import require_license
import re

router = APIRouter(dependencies=[Depends(require_license)])

@router.post("/reports/parse", response_model=CreditMetrics)
async def parse_report(request: Request, report_text: str = Form(default="")):
    # QuickStart mock: extract naive "scores" if present, else defaults.
    eq = re.search(r"EQ[:\s]+(\d+)", report_text or "")
    tu = re.search(r"TU[:\s]+(\d+)", report_text or "")
    ex = re.search(r"EX[:\s]+(\d+)", report_text or "")
    return CreditMetrics(
        aaoa_months=72,
        inquiries_12m=3,
        derogs=0,
        utilization_pct=9.0,
        score_eq=int(eq.group(1)) if eq else 740,
        score_tu=int(tu.group(1)) if tu else 738,
        score_ex=int(ex.group(1)) if ex else 742,
    )
