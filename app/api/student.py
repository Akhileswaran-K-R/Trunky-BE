from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.result import Result

router = APIRouter()

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
