from app.core.security import get_current_user
from fastapi import HTTPException,Depends

def get_current_student(user=Depends(get_current_user)):
    if user["role"] != "student":
        raise HTTPException(status_code=403, detail="Students only")
    return user
