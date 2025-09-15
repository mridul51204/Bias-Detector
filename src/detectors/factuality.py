import re

# Heuristic signals only (no heavy NLP yet)
CLAIMY = ["undeniably", "obviously", "everyone knows", "clearly", "without doubt"]
HEDGES = ["maybe", "perhaps", "reportedly", "apparently", "it seems", "allegedly", "sort of", "kind of"]

def detect_factuality(text: str) -> dict:
    t = text.lower()

    claim_hits = [w for w in CLAIMY if re.search(rf"(?<!\w){re.escape(w)}(?!\w)", t)]
    hedge_hits = [w for w in HEDGES if re.search(rf"(?<!\w){re.escape(w)}(?!\w)", t)]

    # ↑ stronger weights than before (was 1.5/0.5)
    raw = 2.0 * len(set(claim_hits)) + 0.7 * len(set(hedge_hits))
    score = round(min(raw, 10.0), 2)

    flags = []
    if claim_hits:
        flags.append({"group": "claiminess", "matches": sorted(set(claim_hits))})
    if hedge_hits:
        flags.append({"group": "hedges", "matches": sorted(set(hedge_hits))})

    return {"score": score, "flags": flags}
