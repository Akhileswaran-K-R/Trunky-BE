from app.rules.normalization import normalize

# Expert-defined weights
DISABILITIES = {
    "Dyslexia":     {"wt_time": 0.6, "wt_acc": 0.4},
    "Dyscalculia":  {"wt_time": 0.7, "wt_acc": 0.3},
    "ADHD":         {"wt_time": 0.5, "wt_acc": 0.5},
    "Dysgraphia":   {"wt_time": 0.4, "wt_acc": 0.6}
}

def calculate_score(time_norm, accuracy_norm, wt_time, wt_acc):
    return (time_norm * wt_time) + ((1 - accuracy_norm) * wt_acc)

def compute_probabilities(time_taken: float, accuracy: float):
    # Normalize inputs
    time_norm = normalize(time_taken, 10, 120)
    accuracy_norm = normalize(accuracy, 0, 100)

    scores = {}

    for d, w in DISABILITIES.items():
        scores[d] = calculate_score(
            time_norm,
            accuracy_norm,
            w["wt_time"],
            w["wt_acc"]
        )

    total = sum(scores.values())

    probabilities = {
        d: round((s / total) * 100, 2)
        for d, s in scores.items()
    }

    return probabilities
