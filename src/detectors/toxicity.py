from typing import List, Tuple

# Very small lexicon for MVP. Step-2 will swap to a trained model.
TOXIC_LEXICON = {
    "hate", "hates", "hateful",
    "idiot", "stupid", "dumb",
    "trash", "garbage", "disgusting",
    "kill", "shut up",
}

def score_toxicity(text: str) -> Tuple[int, List[Tuple[str, int]]]:
    """
    Returns:
      score (0-100), list of (term, count)
    Heuristic: proportional to hits (cap at 100).
    """
    tlower = text.lower()
    spans = []
    hits = 0
    for term in TOXIC_LEXICON:
        c = tlower.count(term)
        if c > 0:
            spans.append((term, c))
            hits += c

    # simple mapping: each hit = +15 risk, capped
    score = min(100, hits * 15)
    return score, spans
