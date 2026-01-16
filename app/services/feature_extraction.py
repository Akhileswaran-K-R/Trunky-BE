def extract_features(events):
    reaction_times = [e.reaction_time for e in events]
    accuracy = sum(e.correct for e in events) / len(events)

    return {
        "avg_rt": sum(reaction_times) / len(reaction_times),
        "accuracy": accuracy,
        "event_count": len(events)
    }
