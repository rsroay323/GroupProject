# main.py

from fastapi import FastAPI, Depends, HTTPException, Request
from routes import facilities, events, transport, clubs
from fastapi.security import HTTPBearer
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from models import user, event, club, facility, transport as transport_model
import logging

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
# A09: Security Logging and Monitoring Failures
# Logging to monitor API activity
# ------------------------------------------------
logging.basicConfig(level=logging.INFO)

# ------------------------------------------------
# A01: Broken Access Control
# Require authentication for protected routes
# ------------------------------------------------
security = HTTPBearer()

def verify_token(credentials=Depends(security)):
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
# A05: Security Misconfiguration / A07: Identification
# Restrict which websites can call the API
# ------------------------------------------------
origins = [
    "http://localhost",
    "http://127.0.0.1"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------
# Routers
# ------------------------------------------------
app.include_router(facilities.router)
app.include_router(events.router)
app.include_router(transport.router)
app.include_router(clubs.router)

# ------------------------------------------------
# A09: Logging & Monitoring
# ------------------------------------------------
@app.get("/")
def home(request: Request):
    logging.info("Home endpoint accessed")
    return {"message": "Live Campus Hub API running"}

# ------------------------------------------------
# A01: Broken Access Control
# Protected endpoint
# ------------------------------------------------
@app.get("/secure-data", dependencies=[Depends(verify_token)])
def secure_data(request: Request):
    logging.info("Secure endpoint accessed")
    return {"message": "Authenticated access granted"}