def run_stage1_model(features):
    # Placeholder logic (replace with ML later)
    risk_score = 0.0

    if features["avg_rt"] > 1.2:
        risk_score += 0.4
    if features["accuracy"] < 0.7:
        risk_score += 0.4

    return {
        "risk_score": min(risk_score, 1.0),
        "flag": risk_score >= 0.5
    }
