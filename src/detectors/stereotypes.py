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
            if re.search(rf"(?<!\w){re.escape(w)}(?!\w)", t):
                found.append(w)
        if found:
            hits.append({"group": group, "matches": sorted(set(found))})

    # ↑ slightly stronger per-match weight (was 2.0)
    raw = sum(2.5 * len(h["matches"]) for h in hits)
    score = round(min(raw, 10.0), 2)

    return {"score": score, "flags": hits}
