# src/utils/rewrite.py
from __future__ import annotations
import re

_SOFT_MAP = {
    r"\bidiot\b": "person",
    r"\bstupid\b": "unhelpful",
    r"\bdumb\b": "unhelpful",
    r"\bshut\s+up\b": "please be quiet",
    r"\bhate\b": "dislike",
}

def _collapse_punct(s: str) -> str:
    s = re.sub(r"!{2,}", "!", s)
    s = re.sub(r"\?{2,}", "?", s)
    return s

def _limit_repeated_words(s: str) -> str:
    # Reduce 3+ consecutive repeats to 2, keeping spaces
    # Example: "idiot idiot idiot" -> "idiot idiot"
    def repl(m: re.Match) -> str:
        word = m.group(1)
        return f"{word} {word}"
    return re.sub(r"\b(\w+)(?:\s+\1){2,}\b", repl, s, flags=re.IGNORECASE)

def _soften_all_caps(s: str) -> str:
    return re.sub(r"\b[A-Z]{3,}\b", lambda m: m.group(0).lower(), s)

def _apply_lexical_softeners(s: str) -> str:
    for pat, repl in _SOFT_MAP.items():
        s = re.sub(pat, repl, s, flags=re.IGNORECASE)
    s = re.sub(r"\b(so|very|extremely|really)\b", "quite", s, flags=re.IGNORECASE)
    return s

def rewrite_text(text: str) -> str:
    if not text:
        return ""

    out = text
    out = _collapse_punct(out)
    out = _limit_repeated_words(out)
    out = _soften_all_caps(out)
    out = _apply_lexical_softeners(out)
    out = re.sub(r"\s+", " ", out).strip()

    if out and out[0].islower():
        out = out[0].upper() + out[1:]
    return out
