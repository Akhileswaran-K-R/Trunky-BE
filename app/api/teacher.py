import random, string
from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.result import Result
from app.models.test_room import TestRoom
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.student_session import StudentSession

router = APIRouter()

def generate_room_code():
    return "TRK-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=4))

@router.post("/create-room")
def create_test_room(
    duration_minutes: int = 30,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    room_code = generate_room_code()
    expires_at = datetime.utcnow() + timedelta(minutes=duration_minutes)

    room = TestRoom(
        room_code=room_code,
        teacher_id=user["teacher_id"],
        expires_at=expires_at
    )

    db.add(room)
    db.commit()
    db.refresh(room)

    return {
        "room_code": room.room_code,
        "expires_at": room.expires_at
    }

@router.get("/room/{room_code}/results")
def view_room_results(
    room_code: str,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    room = db.query(TestRoom).filter(
        TestRoom.room_code == room_code,
        TestRoom.teacher_id == user["teacher_id"]
    ).first()

    if not room:
        return {"error": "Room not found"}

    sessions = db.query(StudentSession).filter(
        StudentSession.room_id == room.id
    ).all()

    return sessions