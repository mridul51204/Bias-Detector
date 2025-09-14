from .stereotypes import detect_stereotypes
from .toxicity import detect_toxicity
from .factuality import detect_factuality
from utils.scoring import combine_scores

def analyze_text(text: str) -> dict:
    """Run all detectors and return a combined, stable structure."""
    text = text or ""
    ster = detect_stereotypes(text)
    tox  = detect_toxicity(text)
    fac  = detect_factuality(text)

    overall = combine_scores({
        "stereotypes": ster["score"],
        "toxicity": tox["score"],
        "factuality": fac["score"],
    })

    return {
        "input_len": len(text),
        "stereotypes": ster,
        "toxicity": tox,
        "factuality": fac,
        "overall": overall,
    }

def detectors_health() -> dict:
    """Lightweight self-check useful in Streamlit expander."""
    try:
        _ = detect_stereotypes("health check")
        _ = detect_toxicity("health check")
        _ = detect_factuality("health check")
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": repr(e)}
