from typing import Tuple, List
import re

# Very light heuristic for Step-1:
# If we see absolute numeric claims without sources, give a small error score.
ABSOLUTE_CLAIM = re.compile(r"\b(100%|always|never|everyone|no one|all|none)\b", re.I)
NUMERIC_CLAIM = re.compile(r"\b\d{2,}%|\b\d{3,}(?:,\d{3})*\b")

def check_factuality(text: str) -> Tuple[int, List[str]]:
    """
    Returns: (factual_error 0-100, notes)
    Step-2 will add: retrieval + NLI verdicts (Supported/Refuted/NEI) with citations.
    """
    notes: List[str] = []
    score = 0

    if ABSOLUTE_CLAIM.search(text):
        score += 15
        notes.append("Absolute/universal wording detected (consider hedging).")

    # naive numeric risk without citations/links
    has_numbers = bool(NUMERIC_CLAIM.search(text))
    has_link = "http://" in text or "https://" in text or "wikipedia.org" in text
    if has_numbers and not has_link:
        score += 20
        notes.append("Numeric claim without cited evidence.")

    # cap
    score = min(100, score)
    return score, notes
