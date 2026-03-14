from sqlalchemy import Column, Integer, String
from database import Base

class Transport(Base):
    __tablename__ = "transport"

    id = Column(Integer, primary_key=True, index=True)
    bus = Column(String(100), nullable=False)