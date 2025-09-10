import hmac, hashlib, os

def verify_woo_signature(payload: bytes, signature: str) -> bool:
    secret = os.getenv("WOO_WEBHOOK_SECRET","")
    if not secret:
        return False
    digest = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, signature or "")
