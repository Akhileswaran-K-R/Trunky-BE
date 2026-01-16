from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime
import os, json
from anthropic import Anthropic

# ===================== SETUP =====================
app = FastAPI(title="Assessment API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-sonnet-4-20250514"

sessions: Dict[str, Dict[str, Any]] = {}

# ===================== MODELS =====================
class QuestionReq(BaseModel):
    session_id: str
    age: int

class ResponseReq(BaseModel):
    session_id: str
    level: int
    type: str
    data: Dict[str, Any]
    time_taken: float

class AnalysisReq(BaseModel):
    session_id: str
    results: List[Dict[str, Any]]

# ===================== AI HELPERS =====================
def ask_ai(prompt: str, tokens=3000):
    res = client.messages.create(
        model=MODEL,
        max_tokens=tokens,
        messages=[{"role": "user", "content": prompt}]
    )
    return res.content[0].text.strip().replace("```json", "").replace("```", "")

def question_prompt(level, age):
    return f"""
Create 4 fun questions for a {age}-year-old child.
Level: {level}

Return ONLY JSON:

{{
 "questions":[
  {{ "type":"mcq","question":"...","options":["A","B","C","D"],"answer":0 }},
  {{ "type":"match","left":["A","B"],"right":["1","2"],"pairs":{{"0":1,"1":0}} }},
  {{ "type":"memory","show":["🍎","🚗"],"choices":["🍎","🚗","⭐","🎈"] }},
  {{ "type":"gesture","gesture":"Thumbs Up 👍"}}
 ]
}}
"""

def analysis_prompt(results):
    return f"""
Analyze child learning patterns.
NO medical diagnosis.
Return ONLY JSON.

Results:
{json.dumps(results)}

Format:
{{
 "summary":"...",
 "strengths":[],
 "growth":[],
 "scores":{{"attention":0,"memory":0,"processing":0,"motor":0}}
}}
"""

# ===================== ROUTES =====================
@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/level/{level}")
def get_questions(level: int, req: QuestionReq):
    if level < 1 or level > 10:
        raise HTTPException(400, "Invalid level")

    sessions.setdefault(req.session_id, {
        "age": req.age,
        "responses": [],
        "started": datetime.now().isoformat()
    })

    ai_json = ask_ai(question_prompt(level, req.age))
    return {
        "level": level,
        "questions": json.loads(ai_json)["questions"]
    }

@app.post("/response")
def save_response(r: ResponseReq):
    if r.session_id not in sessions:
        raise HTTPException(404, "Session not found")

    sessions[r.session_id]["responses"].append({
        "level": r.level,
        "type": r.type,
        "data": r.data,
        "time": r.time_taken
    })
    return {"saved": True}

@app.post("/analysis")
def analyze(req: AnalysisReq):
    ai_json = ask_ai(analysis_prompt(req.results))
    sessions[req.session_id]["analysis"] = json.loads(ai_json)
    return sessions[req.session_id]["analysis"]
