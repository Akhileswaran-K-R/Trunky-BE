from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from datetime import datetime
from app.db.base import Base

class StudentSession(Base):
    __tablename__ = "student_sessions"

    id = Column(Integer, primary_key=True)
    roll_no = Column(String, index=True)
    room_id = Column(Integer, ForeignKey("test_rooms.id"))
    started_at = Column(DateTime, default=datetime.utcnow)
    completed = Column(Boolean, default=False)
