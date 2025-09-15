import re

TOXIC_WORDS = [
    "stupid", "idiot", "dumb", "trash", "garbage", "hate", "shut up",
    "loser", "moron", "pathetic", "terrible person",
]

def detect_toxicity(text: str) -> dict:
    t = text.lower()

    # collect all matches (so we can count repeats)
    found_all = []
    for w in TOXIC_WORDS:
        found_all += re.findall(rf"(?<!\w){re.escape(w)}(?!\w)", t)

    found_unique = sorted(set(found_all))

    # base weight per unique hit; phrases get a bump
    raw = 0.0
    for w in found_unique:
        raw += 2.0 if " " in w else 1.2

    # small bonus for repeats beyond the first
    repeats = max(0, len(found_all) - len(found_unique))
    raw += 0.3 * repeats

    score = round(min(raw, 10.0), 2)
    flags = [{"group": "toxicity", "matches": found_unique}] if found_unique else []
    return {"score": score, "flags": flags}
