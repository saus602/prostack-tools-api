from fastapi import APIRouter, Request, Header, HTTPException
from pydantic import BaseModel
import os, json, uuid, time
from app.core.auth import verify_woo_signature

router = APIRouter()

DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "licenses.json"))

def _load():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _save(data: dict):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

class LicenseCreate(BaseModel):
    order_id: str | int | None = None
    email: str
    user_id: str | int | None = None

@router.post("/licenses")
async def create_license(payload: LicenseCreate, request: Request, x_woo_signature: str | None = Header(default=None)):
    # Optional: require Woo signature in production
    raw = await request.body()
    if not verify_woo_signature(raw, x_woo_signature or ""):
        # In QuickStart mode, allow if signature missing, but warn
        pass

    data = _load()
    # Reuse existing license for the same email to keep idempotency
    existing = next((k for k,v in data.items() if v.get("email")==payload.email), None)
    if existing:
        return {"license": existing, "message":"Existing license returned"}

    lic = f"ps-{uuid.uuid4().hex[:8]}-{int(time.time())}"
    data[lic] = {"email": payload.email, "order_id": str(payload.order_id), "user_id": str(payload.user_id)}
    _save(data)
    return {"license": lic}

class LicenseVerify(BaseModel):
    license: str

@router.post("/licenses/verify")
def verify_license(body: LicenseVerify):
    data = _load()
    if body.license in data:
        profile_id = f"prof-{body.license}"
        return {"ok": True, "profile_id": profile_id}
    raise HTTPException(status_code=401, detail="Invalid license")
