from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class IntakeRequest(BaseModel):
    email: str
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    business_name: str | None = None
    ein: str | None = None
    address: str | None = None

class IntakeResponse(BaseModel):
    profile_id: str
    message: str = "Intake profile created"

class ParseReportRequest(BaseModel):
    # For simplicity; if you accept files, use form-data at the route level
    report_text: str | None = None

class CreditMetrics(BaseModel):
    aaoa_months: int
    inquiries_12m: int
    derogs: int
    utilization_pct: float
    score_eq: int | None = None
    score_tu: int | None = None
    score_ex: int | None = None

class PrequalRunRequest(BaseModel):
    profile_id: str

class PrequalOffer(BaseModel):
    issuer: str
    product: str
    apr_range: str | None = None
    notes: str | None = None

class OptimizeReq(BaseModel):
    goals: Dict[str, Any] = Field(default_factory=dict)
    constraints: Dict[str, Any] = Field(default_factory=dict)
    profile_id: str

class OptimizeResp(BaseModel):
    sequence: List[Dict[str, Any]]
    estimated_total_limit: int

class ApplicationCreate(BaseModel):
    profile_id: str
    issuer: str
    card: str
    rank: int

class ApplicationResp(BaseModel):
    application_id: str

class ApplicationStatusPatch(BaseModel):
    status: str # "instant", "pending", "denied", "approved"
    limit: Optional[int] = None
    notes: Optional[str] = None
