import google.generativeai as genai
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

MODEL_NAME = "gemini-3-flash-preview"

model = genai.GenerativeModel(MODEL_NAME)

def ask_ai(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text.strip()
