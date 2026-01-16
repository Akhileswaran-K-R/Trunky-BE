from pydantic import BaseModel

class EvaluationRequest(BaseModel):
    time_taken: float
    accuracy: float

class EvaluationResponse(BaseModel):
    probabilities: dict
    recommendations: dict
