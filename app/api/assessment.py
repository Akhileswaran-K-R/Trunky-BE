from fastapi import APIRouter, HTTPException
from datetime import datetime
import json

from app.core.ai import ask_ai
from app.services.prompts import question_prompt
from app.core.deps import get_current_student

router = APIRouter()

sessions = {}

from fastapi import Depends, HTTPException
from datetime import datetime
import json

@router.post("/level/{level}")
def get_questions(
    level: int,
    student=Depends(get_current_student)
):
    if level < 1 or level > 10:
        raise HTTPException(status_code=400, detail="Invalid level")

    # Unique session per student per room
    session_key = f"{student['room_id']}:{student['roll_no']}"

    # Initialize session if first time
    sessions.setdefault(session_key, {
        "room_id": student["room_id"],
        "roll_no": student["roll_no"],
        "responses": [],
        "started": datetime.utcnow().isoformat()
    })

    # Age can be fetched from DB or room config
    age = 8  # TEMP default, replace later

    raw = ask_ai(question_prompt(level, age))

    clean = raw.replace("```json", "").replace("```", "")
    data = json.loads(clean)

    return {
        "level": level,
        "questions": data["questions"]
    }
