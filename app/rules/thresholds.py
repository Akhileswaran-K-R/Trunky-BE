SAFE_LIMIT = 30
WARNING_LIMIT = 45

def evaluate_risk(probabilities: dict):
    recommendations = {}

    for d, prob in probabilities.items():
        if prob >= WARNING_LIMIT:
            recommendations[d] = "HIGH RISK – Further testing required"
        elif prob >= SAFE_LIMIT:
            recommendations[d] = "MODERATE RISK – Monitor closely"
        else:
            recommendations[d] = "LOW RISK"

    return recommendations
