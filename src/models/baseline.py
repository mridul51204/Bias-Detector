from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# --- tiny in-repo dataset (balanced, small, fast) ---
def _samples() -> Tuple[List[str], List[int]]:
    pos = [
        "Obviously this is the only correct view",
        "Everyone knows they are stupid",
        "Shut up you idiot",
        "Those boomers are dumb",
        "This group is typically lazy",
        "Clearly the facts support me",
        "You are a loser and pathetic",
        "It is undeniably true",
        "Garbage opinion from a moron",
        "Third-world people are like this",
    ]
    neg = [
        "There are several perspectives to consider",
        "The results may vary by context",
        "This statement requires evidence",
        "The method seems reasonable",
        "We should verify the claim",
        "The team discussed multiple options",
        "The article presents two viewpoints",
        "There is no strong language here",
        "A neutral sentence without bias markers",
        "Further analysis is recommended",
    ]
    X = pos + neg
    y = [1]*len(pos) + [0]*len(neg)
    return X, y

@dataclass
class _ModelBundle:
    vect: TfidfVectorizer
    clf: LogisticRegression

_MODEL: _ModelBundle | None = None

def _train() -> _ModelBundle:
    X, y = _samples()
    vect = TfidfVectorizer(ngram_range=(1,2), stop_words="english", min_df=1)
    Xv = vect.fit_transform(X)
    clf = LogisticRegression(max_iter=1000, n_jobs=None, class_weight="balanced")
    clf.fit(Xv, y)
    return _ModelBundle(vect=vect, clf=clf)

def get_model() -> _ModelBundle:
    global _MODEL
    if _MODEL is None:
        _MODEL = _train()
    return _MODEL

def predict_proba(text: str) -> float:
    """Return P(class=1 | text) ∈ [0,1]."""
    bundle = get_model()
    X = bundle.vect.transform([text or ""])
    proba = bundle.clf.predict_proba(X)[0, 1]
    return float(proba)
