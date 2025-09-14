import re

TOXIC_WORDS = [
    "stupid", "idiot", "dumb", "trash", "garbage", "hate", "shut up",
    "loser", "moron", "pathetic", "terrible person",
]

def detect_toxicity(text: str) -> dict:
    t = text.lower()
    found = []
    for w in TOXIC_WORDS:
        if re.search(rf"(?<!\w){re.escape(w)}(?!\w)", t):
            found.append(w)

    # severity via frequency and phrase length
    raw = 0.0
    for w in found:
        raw += 1.5 if " " in w else 1.0
    score = round(min(raw, 10.0), 2)
    return {"score": score, "flags": [{"group": "toxicity", "matches": sorted(set(found))}] if found else []}
