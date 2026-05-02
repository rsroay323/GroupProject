from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session
from datetime import datetime
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
    if credentials.credentials != "securetoken":
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
@limiter.limit("100/minute")
def get_clubs(request: Request, db: Session = Depends(get_db)):
    """
    Returns a list of campus clubs.
    Only accessible to authenticated users.
    Rate-limited to prevent abuse.
    """
    # Logging access for Repudiation / Monitoring (A09)
    return db.query(Club).all()

@router.post("/clubs", dependencies=[Depends(verify_token)])
@limiter.limit("100/minute")
def create_club(request: Request, club: dict, db: Session = Depends(get_db)):
    
    new_club = Club(
        name=club["name"],
        description=club["description"],
        location=club["location"],
        session_date=datetime.strptime(club["session_date"], "%Y-%m-%d").date(),
        session_time=datetime.strptime(club["session_time"], "%H:%M").time()
    )
    db.add(new_club)
    db.commit()
    db.refresh(new_club)
    return new_club



@router.put("/clubs/{club_id}", dependencies=[Depends(verify_token)])
@limiter.limit("100/minute")
def update_club(
    request: Request,
    club_id: int,
    updated_club: dict,
    db: Session = Depends(get_db)
):
    print("Update club endpoint accessed")
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    club.name = updated_club["name"]
    club.description = updated_club["description"]
    club.location = updated_club["location"]
    club.session_date = datetime.strptime(updated_club["session_date"], "%Y-%m-%d").date()
    club.session_time = datetime.strptime(updated_club["session_time"], "%H:%M").time()
    db.commit()
    db.refresh(club)
    return club


@router.delete("/clubs/{club_id}", dependencies=[Depends(verify_token)])
@limiter.limit("100/minute")
def delete_club(
    request: Request,
    club_id: int,
    db: Session = Depends(get_db)
):
    print("Delete club endpoint accessed")
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    db.delete(club)
    db.commit()
    return {"message": "Club deleted successfully"}