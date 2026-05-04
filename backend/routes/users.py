from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
from models.user import User

from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):

    return pwd_context.hash(password)

@router.post("/register")

def register_user(user: dict, db: Session = Depends(get_db)):

    name = user.get("name", "").strip()
    email = user.get("email", "").strip().lower()
    password =  user.get("password", "")

 
    if not name or not email or not password:
        raise HTTPException(status_code=400, detail="All fields required")

    if len(password) < 6:
        raise HTTPException(status_code=400,  detail="Password too short")

    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(password)

 
    new_user = User(
         name=name,
        email=email,
        password_hash=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created"}