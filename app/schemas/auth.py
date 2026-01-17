from pydantic import BaseModel, EmailStr

class TeacherSignup(BaseModel):
    name: str
    email: EmailStr
    password: str

class TeacherLogin(BaseModel):
    email: EmailStr
    password: str
