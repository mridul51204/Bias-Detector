def combine_scores(parts: dict) -> dict:
    """
    Weighted overall score for detectors.
    parts = {"stereotypes": x, "toxicity": y, "factuality": z}
    """
    weights = {"toxicity": 0.45, "stereotypes": 0.35, "factuality": 0.20}
    score = sum(weights[k] * float(parts.get(k, 0.0)) for k in weights)
    score = round(min(score, 10.0), 2)
    return {"score": score, "weights": weights, "components": parts}
