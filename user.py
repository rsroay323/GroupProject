from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"  # Corrected: __tablename__ with double underscores

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=100), nullable=False)  # Specify max length and not nullable
    email = Column(String(length=255), unique=True, nullable=False, index=True)
    points = Column(Integer, default=0, nullable=False)