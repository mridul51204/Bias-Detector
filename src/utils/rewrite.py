# src/utils/rewrite.py
from __future__ import annotations
import re

# Simple lexical softeners (keep it deterministic + safe)
_SOFT_MAP = {
    r"\bidiot\b": "person",
    r"\bstupid\b": "unhelpful",
    r"\bdumb\b": "unhelpful",
    r"\bshut\s+up\b": "please be quiet",
    r"\bhate\b": "dislike",
}

def _collapse_punct(s: str) -> str:
    # Collapse sequences of ! or ? to a single char
    s = re.sub(r"!{2,}", "!", s)
    s = re.sub(r"\?{2,}", "?", s)
    return s

def _limit_repeated_words(s: str) -> str:
    # Reduce 3+ consecutive repeats of the same word to 2
    # e.g., "bad bad bad" -> "bad bad"
    return re.sub(r"\b(\w+)(\s+\1){2,}\b", r"\1\1", s, flags=re.IGNORECASE)

def _soften_all_caps(s: str) -> str:
    # Lowercase words that are shouting (ALL CAPS, len>=3)
    return re.sub(r"\b[A-Z]{3,}\b", lambda m: m.group(0).lower(), s)

def _apply_lexical_softeners(s: str) -> str:
    for pat, repl in _SOFT_MAP.items():
        s = re.sub(pat, repl, s, flags=re.IGNORECASE)
    # De-intensify common amplifiers
    s = re.sub(r"\b(so|very|extremely|really)\b", "quite", s, flags=re.IGNORECASE)
    return s

def rewrite_text(text: str) -> str:
    """
    Heuristic, non-ML rewrite to ‘soften’ tone:
      - collapse !!!/??? -> !/?
      - cap repeated words
      - soften ALL-CAPS words
      - replace a few toxic phrases with neutral ones
      - keep whitespace neat
    """
    if not text:
        return ""

    out = text
    out = _collapse_punct(out)
    out = _limit_repeated_words(out)
    out = _soften_all_caps(out)
    out = _apply_lexical_softeners(out)

    # Tidy whitespace
    out = re.sub(r"\s+", " ", out).strip()

    # Capitalize first character if sentence starts lowercase
    if out and out[0].islower():
        out = out[0].upper() + out[1:]
    return out
