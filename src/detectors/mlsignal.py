from models.baseline import predict_proba

def detect_mlsignal(text: str) -> dict:
    """
    ML probability from a tiny TF-IDF + LogisticRegression model.
    Map probability to a 0-10 score for UI consistency.
    """
    p = predict_proba(text or "")
    score = round(p * 10.0, 2)
    label = "biased_like" if p >= 0.5 else "neutral_like"
    return {"score": score, "proba": round(p, 4), "label": label}
