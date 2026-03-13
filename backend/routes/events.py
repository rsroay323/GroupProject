from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from slowapi import Limiter
from slowapi.util import get_remote_address

# Initialize router
router = APIRouter()

# -------------------------------
# STRIDE & OWASP Security Controls
# -------------------------------

# 1. Spoofing / Broken Access Control (A01)
security = HTTPBearer()

def verify_token(credentials=Depends(security)):
    token = credentials.credentials
    if token != "securetoken":
        raise HTTPException(status_code=403, detail="Invalid token")

# 2. Denial of Service (A06)
# Limiter will be applied in main.py
limiter = Limiter(key_func=get_remote_address)

# -------------------------------
# Endpoint with security
# -------------------------------
@router.get("/events", dependencies=[Depends(verify_token)])
@limiter.limit("5/minute")
def get_events(request: Request):
    """
    Returns a list of campus events.
    Only accessible to authenticated users.
    Rate-limited to prevent abuse.
    """
    # Logging access for Repudiation / Monitoring (A09)
    print("Events endpoint accessed")

    return [
        {"title": "Quiz Night", "time": "8 PM"},
        {"title": "Coding Club", "time": "5 PM"}
    ]