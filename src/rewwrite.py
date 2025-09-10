import re

ABSOLUTES = r"\b(always|never|everyone|no one|all|none|every|nobody|nothing)\b"
INTENSIFIERS = r"\b(obviously|clearly|undeniably|plainly|definitely|certainly|surely)\b"
SWEARS = r"\b(dumb|stupid|idiot|trash|garbage|hate|disgusting)\b"

def _soften_absolutes(text: str) -> str:
    return re.sub(ABSOLUTES, "often", text, flags=re.I)

def _soften_intensifiers(text: str) -> str:
    return re.sub(INTENSIFIERS, "it appears", text, flags=re.I)

def _remove_swears_near_identities(text: str) -> str:
    # very light neutralization—keeps meaning while removing spikes
    return re.sub(SWEARS, "inappropriate", text, flags=re.I)

def suggest_rewrite(text: str, stereotype_score: int, toxicity_score: int, factual_error: int) -> str:
    """
    MVP rewrite:
    - soften absolutes & intensifiers
    - remove loaded adjectives/epithets
    - hedge first strong copular claim
    (We’ll replace with span-aware, model-guided edits in Step-3.)
    """
    rewrite = text
    rewrite = _soften_absolutes(rewrite)
    rewrite = _soften_intensifiers(rewrite)
    rewrite = _remove_swears_near_identities(rewrite)

    # hedge the first "X is Y" into "X can be Y" (once)
    rewrite = re.sub(r"\b(are|is)\s+(\w+)\b", r"can be \2", rewrite, count=1)

    # compact excessive whitespace
    rewrite = re.sub(r"\n{3,}", "\n\n", rewrite)
    return rewrite.strip()
