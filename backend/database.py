# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Session
import os

# ------------------------------------------------
# A02: Cryptographic Failures
# Store database configuration in environment variables
# instead of hardcoding sensitive information
# ------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./campus.db")

# ------------------------------------------------
# A05: Security Misconfiguration
# Configure secure database engine settings
# ------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False  # prevents SQL queries from being logged in production
)

# ------------------------------------------------
# A09: Security Logging and Monitoring
# Controlled database session handling
# ------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for database models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()