from fastapi import FastAPI
from app.api import auth, teacher, student

app = FastAPI(title="Learning Disability Screening API")

app.include_router(auth.router, prefix="/auth")
app.include_router(teacher.router, prefix="/teacher")
app.include_router(student.router, prefix="/student")
