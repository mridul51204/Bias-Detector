from models.baseline import predict_proba

def detect_mlsignal(text: str) -> dict:
    """
    ML probability from a tiny TF-IDF + LogisticRegression model.
    Map probability to a 0–10 score with a mild gamma to separate highs.
    """
    p = predict_proba(text or "")
    gamma = 0.75  # < 1.0 => boosts values above ~0.5 a bit
    score = round((p ** gamma) * 10.0, 2)
    label = "biased_like" if p >= 0.5 else "neutral_like"
    return {"score": score, "proba": round(p, 4), "label": label}
