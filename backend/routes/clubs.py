from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session

from database import get_db
from models.club import Club

# Initialize router
router = APIRouter()

# -------------------------------
# STRIDE & OWASP Controls
# -------------------------------
# 1. Spoofing / Broken Access Control (A01)
# Require a valid token to access this endpoint
security = HTTPBearer()

def verify_token(credentials=Depends(security)):
    token = credentials.credentials
    if token != "securetoken":
        raise HTTPException(status_code=403, detail="Invalid token")

# 2. Denial of Service (A06)
# Limit number of requests per minute
limiter = Limiter(key_func=get_remote_address)

# Middleware will be applied in main.py
# Just use the limiter decorator here

# -------------------------------
# Endpoint with security
# -------------------------------
@router.get("/clubs", dependencies=[Depends(verify_token)])
@limiter.limit("5/minute")
def get_clubs(request: Request, db: Session = Depends(get_db)):
    """
    Returns a list of campus clubs.
    Only accessible to authenticated users.
    Rate-limited to prevent abuse.
    """
    # Logging access for Repudiation / Monitoring (A09)
    print("Clubs endpoint accessed")
    
    clubs = db.query(Club).all()
    return clubs