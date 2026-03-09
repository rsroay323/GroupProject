from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    tablename = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    points = Column(Integer, default=0)
