from fastapi import APIRouter
from sqlalchemy.orm import Session
from database import get_db
from models.facility import Facility
from fastapi import Depends

router = APIRouter()

@router.get("/facilities")
def get_facilities(db: Session = Depends(get_db)):
    facilities = db.query(Facility).all()
    return facilities           
    