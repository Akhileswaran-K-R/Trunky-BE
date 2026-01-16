from fastapi import APIRouter
from app.schemas.evaluation import EvaluationRequest, EvaluationResponse
from app.rules.rule_engine import compute_probabilities
from app.rules.thresholds import evaluate_risk

router = APIRouter(
    prefix="/evaluate",
    tags=["Evaluation"]
)

@router.post("/", response_model=EvaluationResponse)
def evaluate_student(data: EvaluationRequest):
    probabilities = compute_probabilities(
        time_taken=data.time_taken,
        accuracy=data.accuracy
    )

    recommendations = evaluate_risk(probabilities)

    return {
        "probabilities": probabilities,
        "recommendations": recommendations
    }
