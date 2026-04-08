# main.py

from fastapi import FastAPI, Depends, HTTPException, Request
from routes import facilities, events, transport, clubs
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from models import user, event, club, facility, transport as transport_model
import logging
from database import SessionLocal
from models.club import Club
from models.event import Event
from models.facility import Facility
from models.transport import Transport
from datetime import date
from datetime import time

# ------------------------------------------------
# A05: Security Misconfiguration / Information Exposure
# Disable automatic API documentation in production
# ------------------------------------------------
app = FastAPI(
    title="Campus Hub API",
    docs_url=None,
    redoc_url=None
)

Base.metadata.create_all(bind=engine)


# ------------------------------------------------
# Seed database with initial data
# ------------------------------------------------
def seed_database():
    db = SessionLocal()
    
    if db.query(Club).first() is None:

        db.add_all([
            Club(name="Coding Club", description= "Learn programming and build projects together", location="Room 303", session_date=date(2026, 10, 15), session_time=time(18, 0)),
            Club(name="Cyber Security Club", description="Learn about cyber security ", location="Room 43", session_date=date(2026, 10, 16), session_time=time(19, 0)),
            Club(name="Dance Club", description="Express yourself through dance and meet new people", location="Room 763", session_date=date(2026, 10, 17), session_time=time(20, 0))
        ])

        db.add_all([
            Event(title="Hackathon", time=time(18, 0), date=date(2026, 10, 15)),
            Event(title="Quiz Night", time=time(19, 30), date=date(2026, 10, 16)),
            Event(title="AI Workshop", time=time(17, 0), date=date(2026, 10, 17))
        ])

        db.add_all([
    Facility(
        name="Gym",
        status=True,
        description="Fully equipped gym with treadmills, weights and more",
        opening_time=time(6, 0),
        closing_time=time(21, 0)
    ),
    Facility(
        name="Library",
        status=True,
        description="Quiet study space with computers, resources and more",
        opening_time=time(8, 0),
        closing_time=time(20, 0)
    ),
    Facility(
        name="Sports Hall",
        status=False,
        description="Indoor sports facility with courts, equipment and more",
        opening_time=time(9, 0),
        closing_time=time(18, 0)
    )
])
            

        db.add_all([
            Transport(bus="Bus 529"),
            Transport(bus="Bus 51")
        ])

        db.commit()

    db.close()

seed_database()


# ------------------------------------------------
# A09: Security Logging and Monitoring Failures
# Logging to monitor API activity
# ------------------------------------------------
logging.basicConfig(level=logging.INFO)


# ------------------------------------------------
# A01: Broken Access Control
# Token-based authentication for all protected routes
# ------------------------------------------------
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    if token != "securetoken":
        raise HTTPException(status_code=403, detail="Invalid authentication token")


# ------------------------------------------------
# A05: Security Misconfiguration
# Restrict allowed hosts
# ------------------------------------------------
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1"]
)


# ------------------------------------------------
# A05 / A07: CORS restrictions
# Restrict which websites can call the API
# ------------------------------------------------
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------------
# Routers (NOW PROTECTED WITH TOKEN SECURITY)
# ------------------------------------------------
app.include_router(facilities.router, dependencies=[Depends(verify_token)])
app.include_router(events.router, dependencies=[Depends(verify_token)])
app.include_router(transport.router, dependencies=[Depends(verify_token)])
app.include_router(clubs.router, dependencies=[Depends(verify_token)])


# ------------------------------------------------
# A09: Logging & Monitoring
# ------------------------------------------------
@app.get("/")
def home(request: Request):
    logging.info("Home endpoint accessed")
    return {"message": "Live Campus Hub API running"}


# ------------------------------------------------
# A01: Broken Access Control
# Example protected endpoint
# ------------------------------------------------
@app.get("/secure-data", dependencies=[Depends(verify_token)])
def secure_data(request: Request):
    logging.info("Secure endpoint accessed")
    return {"message": "Authenticated access granted"}
