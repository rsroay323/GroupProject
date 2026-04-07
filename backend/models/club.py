from sqlalchemy import Column, Integer, String, Date, Time
from database import Base
from datetime import date, time

class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    location = Column(String(100), nullable=False)
    session_date = Column(Date, nullable=False)
    session_time = Column(Time, nullable=False)