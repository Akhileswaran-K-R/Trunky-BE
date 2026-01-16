def normalize(value: float, min_val: float, max_val: float) -> float:
    return (value - min_val) / (max_val - min_val)
