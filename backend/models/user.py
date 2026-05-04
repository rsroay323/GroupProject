from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=100), nullable=False) 
    email = Column(String(length=255), unique=True, nullable=False, index=True)
    password_hash = Column(String(length=255), nullable=False)
    points = Column(Integer, default=0, nullable=False)