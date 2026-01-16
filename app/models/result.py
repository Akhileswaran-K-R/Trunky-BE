from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True)
    roll_no = Column(String)
    score = Column(Integer)
    risk_level = Column(String)
