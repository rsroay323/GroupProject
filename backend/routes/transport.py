from fastapi import APIRouter
from sqlalchemy.orm import Session
from database import get_db
from models.transport import Transport
from fastapi import Depends

router = APIRouter()

@router.get("/transport")
def get_transport(db: Session = Depends(get_db)):
    transport = db.query(Transport).all()
    return transport
