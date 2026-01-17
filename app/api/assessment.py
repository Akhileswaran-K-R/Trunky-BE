from fastapi import APIRouter, HTTPException
from datetime import datetime
import json

from app.core.ai import ask_ai
from app.services.prompts import question_prompt

router = APIRouter()

sessions = {}

@router.post("/level/{level}")
def get_questions(level: int, req: dict):
    if level < 1 or level > 10:
        raise HTTPException(400, "Invalid level")

    sessions.setdefault(req["session_id"], {
        "age": req["age"],
        "responses": [],
        "started": datetime.now().isoformat()
    })

    raw = ask_ai(question_prompt(level, req["age"]))

    # Gemini sometimes wraps markdown
    clean = raw.replace("```json", "").replace("```", "")
    data = json.loads(clean)

    return {
        "level": level,
        "questions": data["questions"]
    }
