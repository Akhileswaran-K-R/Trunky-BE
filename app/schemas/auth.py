from pydantic import BaseModel, EmailStr

class TeacherAuth(BaseModel):
    email: EmailStr
    password: str