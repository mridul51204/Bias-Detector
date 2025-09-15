from .stereotypes import detect_stereotypes
from .toxicity import detect_toxicity
from .factuality import detect_factuality
from .mlsignal import detect_mlsignal
from utils.scoring import combine_scores

def analyze_text(text: str) -> dict:
    text = text or ""
    ster = detect_stereotypes(text)
    tox  = detect_toxicity(text)
    fac  = detect_factuality(text)
    ml   = detect_mlsignal(text)

    parts = {
        "stereotypes": ster["score"],
        "toxicity": tox["score"],
        "factuality": fac["score"],
        "mlsignal": ml["score"],
    }
    overall = combine_scores(parts)

    return {
        "input_len": len(text),
        "stereotypes": ster,
        "toxicity": tox,
        "factuality": fac,
        "mlsignal": ml,
        "overall": overall,
    }

def detectors_health() -> dict:
    try:
        _ = detect_stereotypes("health")
        _ = detect_toxicity("health")
        _ = detect_factuality("health")
        _ = detect_mlsignal("health")
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": repr(e)}
