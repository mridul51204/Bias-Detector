def aggregate_scores(stereotype: int, toxicity: int, factual_error: int, weights: dict) -> int:
    """
    Overall = w1*stereotype + w2*toxicity + w3*(100 - factual_error)
    Returns an integer 0..100 clamped.
    """
    w1 = weights.get("stereotype", 40) / 100.0
    w2 = weights.get("toxicity", 30) / 100.0
    w3 = weights.get("factuality", 30) / 100.0

    score = (w1 * stereotype) + (w2 * toxicity) + (w3 * (100 - factual_error))
    score = max(0, min(100, round(score)))
    return score
