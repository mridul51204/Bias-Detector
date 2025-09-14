import re

SOFTENERS = {
    r"\bobviously\b": "it appears",
    r"\bclearly\b": "it seems",
    r"\bundeniably\b": "arguably",
    r"\beveryone knows\b": "many believe",
    r"\bshut up\b": "please stop",
    r"\b(stupid|idiot|moron)\b": "unhelpful",
}

def rewrite_text(text: str) -> str:
    """Light-touch rewrite: replace extreme/absolute phrases with softer ones."""
    out = text or ""
    for pat, repl in SOFTENERS.items():
        out = re.sub(pat, repl, out, flags=re.IGNORECASE)
    out = re.sub(r"\s{2,}", " ", out).strip()
    return out
