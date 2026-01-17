from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.teacher import Teacher
from app.schemas.auth import TeacherLogin,TeacherSignup
from app.core.password import hash_password, verify_password
from app.core.security import create_token

router = APIRouter()

@router.post("/signup")
def teacher_signup(data: TeacherSignup, db: Session = Depends(get_db)):
    teacher = Teacher(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password)
    )
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    token = create_token({"role": "teacher", "teacher_id": teacher.id})

    return {
        "message": "Teacher registered",
        "access_token": token,
        "name": teacher.name
    }

@router.post("/login")
def teacher_login(data: TeacherLogin, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.email == data.email).first()
    if not teacher or not verify_password(data.password, teacher.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"role": "teacher", "teacher_id": teacher.id})
    return {"access_token": token,"name":teacher.name}
