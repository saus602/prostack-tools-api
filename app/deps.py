from fastapi import Header, HTTPException, Request
import json, os

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "data", "licenses.json")
DATA_FILE = os.path.abspath(DATA_FILE)

def _load_licenses():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def require_license(x_ps_license: str | None = Header(default=None), request: Request = None):
    # Permit open access to health and license creation endpoints
    path = request.url.path if request else ""
    if path.startswith("/health") or path.endswith("/v1/licenses") or path.endswith("/v1/webhooks/woo"):
        return

    if not x_ps_license:
        raise HTTPException(status_code=401, detail="Missing x-ps-license")

    licenses = _load_licenses()
    if x_ps_license not in licenses:
        raise HTTPException(status_code=401, detail="Invalid license")
    # Optionally, attach license context to request.state
    request.state.license = x_ps_license
    request.state.client_info = licenses.get(x_ps_license, {})
    return
