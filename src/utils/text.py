import re

def normalize_whitespace(text: str) -> str:
    """Collapse multiple spaces and trim ends."""
    return re.sub(r"\s+", " ", text).strip()

def sentence_split(text: str) -> list[str]:
    """Naive sentence splitter by punctuation. Replace with nltk/spacy later."""
    return re.split(r"[.!?]+", text)

def word_tokenize(text: str) -> list[str]:
    """Naive whitespace tokenizer."""
    return text.split()
