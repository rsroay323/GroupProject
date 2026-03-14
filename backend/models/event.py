from sqlalchemy import Column, Integer, String
from database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    time = Column(String(50), nullable=False)