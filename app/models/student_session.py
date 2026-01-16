from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base

class StudentSession(Base):
    __tablename__ = "student_sessions"

    id = Column(Integer, primary_key=True)
    roll_no = Column(String)
    session_token = Column(String, unique=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
