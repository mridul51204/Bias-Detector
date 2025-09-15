def combine_scores(parts: dict) -> dict:
    """
    Weighted average over whichever detectors are present.
    Scores are on 0..10; weights renormalize to sum=1 over present keys.
    """
    base_weights = {
        "toxicity": 0.35,
        "stereotypes": 0.30,
        "factuality": 0.15,
        "mlsignal": 0.20,
    }

    used = {k: base_weights[k] for k in parts.keys() if k in base_weights}
    if not used:
        return {"score": 0.0, "weights": {}, "components": parts}

    total_w = sum(used.values())
    norm_w = {k: w / total_w for k, w in used.items()}

    score = 0.0
    for k, w in norm_w.items():
        score += w * float(parts.get(k, 0.0))

    score = round(min(score, 10.0), 2)
    return {"score": score, "weights": norm_w, "components": parts}
