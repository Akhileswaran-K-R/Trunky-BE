from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, teacher, student,evaluation,assessment

app = FastAPI(title="Learning Disability Screening API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-domain.com",
        "http://localhost:3000"  # dev
    ],
    allow_credentials=False,  # important
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(teacher.router, prefix="/teacher")
app.include_router(student.router, prefix="/student")
app.include_router(evaluation.router)
app.include_router(assessment.router)
