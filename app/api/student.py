from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.test_room import TestRoom
from app.core.security import get_current_user,create_token
from app.db.session import get_db
from app.models.student_session import StudentSession
from app.models.result import Result

router = APIRouter()

@router.post("/join-room")
def join_room(
    room_code: str,
    roll_no: str,
    db: Session = Depends(get_db)
):
    room = db.query(TestRoom).filter(
        TestRoom.room_code == room_code,
        TestRoom.is_active == True
    ).first()

    if not room:
        raise HTTPException(status_code=404, detail="Invalid room code")

    if room.expires_at < datetime.utcnow():
        raise HTTPException(status_code=403, detail="Test session expired")

    existing = db.query(StudentSession).filter(
        StudentSession.room_id == room.id,
        StudentSession.roll_no == roll_no
    ).first()

    if existing:
        raise HTTPException(status_code=403, detail="Test already started")

    session = StudentSession(
        roll_no=roll_no,
        room_id=room.id
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    token = create_token(
        {
            "role": "student",
            "roll_no": roll_no,
            "room_id": room.id,
            "session_id": session.id
        },
        expires_minutes=30
    )

    return {
        "access_token": token,
        "message": "Test started"
    }

@router.post("/submit-test")
def submit_test(
    score: int,
    risk_level: str,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user["role"] != "student":
        return {"error": "Unauthorized"}

    result = Result(
        roll_no=user["roll_no"],
        score=score,
        risk_level=risk_level
    )
    db.add(result)
    db.commit()

    return {"message": "Test submitted"}
