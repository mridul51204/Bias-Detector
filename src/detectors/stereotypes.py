import re

# Tiny demo lexicon; expand later
GROUP_TERMS = {
    "gender": ["emotional", "bossy", "hysterical", "manly", "girly"],
    "age": ["boomer", "zoomers", "old-timers", "kids these days"],
    "region": ["third-world", "western", "eastern", "developed", "underdeveloped"],
}

def detect_stereotypes(text: str) -> dict:
    t = text.lower()
    hits = []
    for group, vocab in GROUP_TERMS.items():
        found = []
        for w in vocab:
            # word boundary or hyphenated; keep simple and fast
            if re.search(rf"(?<!\w){re.escape(w)}(?!\w)", t):
                found.append(w)
        if found:
            hits.append({"group": group, "matches": sorted(set(found))})

    # scoring: 2.0 per distinct match, capped
    raw = sum(2.0 * len(h["matches"]) for h in hits)
    score = round(min(raw, 10.0), 2)

    return {"score": score, "flags": hits}
