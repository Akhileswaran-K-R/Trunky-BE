from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.session import BulkSessionCreate
from app.models.result import Result
from app.db.session import get_db
from app.models.student_session import StudentSession
from app.core.security import get_current_user, create_token

router = APIRouter()

@router.post("/create-sessions")
def create_student_sessions(
    data: BulkSessionCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user["role"] != "teacher":
        raise HTTPException(status_code=403, detail="Teacher access only")

    result = []

    for roll_no in data.roll_nos:
        token = create_token({
            "role": "student",
            "roll_no": roll_no
        })

        session = StudentSession(
            roll_no=roll_no,
            session_token=token,
            teacher_id=user["teacher_id"]
        )

        db.add(session)
        result.append({
            "roll_no": roll_no,
            "token": token
        })

    db.commit()

    return {
        "count": len(result),
        "sessions": result
    }

@router.get("/results")
def view_results(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user["role"] != "teacher":
        return {"error": "Unauthorized"}

    return db.query(Result).all()
