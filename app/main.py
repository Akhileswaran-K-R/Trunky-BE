from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, teacher, student,evaluation,assessment
from app.db.base import Base
from app.db.session import engine

app = FastAPI(title="Learning Disability Screening API")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(teacher.router, prefix="/teacher")
app.include_router(student.router, prefix="/student")
app.include_router(evaluation.router)
app.include_router(assessment.router)
