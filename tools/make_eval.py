# tools/make_evals.py
"""
Run all detectors (toxicity, stereotypes, factuality, mlsignal) on a CSV
and save per-row metrics + overall score.

Inputs (CSV):
  id,text,tag

Outputs (CSV):
  id,text,tag,toxicity,stereotypes,factuality,ml_prob,overall

Usage:
  python tools/make_evals.py --in tests/test_snippets.csv --out tests/evals_output.csv
"""

from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ---- Weights & hyperparams (match app) ----
W_TOX = 0.40
W_ST  = 0.30
W_FACT = 0.10
W_ML  = 0.20
GAMMA = 0.75  # mlsignal blending toward 0.5

# ---- Simple lexicons / patterns to mirror app heuristics ----
BAD_WORDS = {
    "idiot", "stupid", "dumb", "shut up", "moron", "trash", "hate"
}
STEREO_PATTERNS = [
    r"\b(women|men|girls|boys|teenagers|immigrants|elderly)\s+(are|can't|shouldn't|always|never)\b",
    r"\b(people from|folks from)\s+\w+\s+(are|can't|shouldn't|always|never)\b",
]
CLAIMY_PHRASES = [
    "everyone knows", "100% true", "without a doubt", "obviously", "clearly",
]
HEDGE_PHRASES = [
    "maybe", "might", "it might", "it could", "possibly", "it may", "seems", "appears",
]

def _norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower()).strip()

def score_toxicity(text: str) -> float:
    t = _norm_ws(text)
    score = 0.0
    # phrase bump: each bad word adds 1.0
    for w in BAD_WORDS:
        if w in t:
            score += 1.0
    # repeats: any token appearing >=3 times adds 1.0
    toks = re.findall(r"[a-z']+", t)
    if not toks:
        return score
    from collections import Counter
    c = Counter(toks)
    if any(cnt >= 3 for cnt in c.values()):
        score += 1.0
    # scream punctuation
    if "!!!" in t or "???" in t:
        score += 0.5
    return score

def score_stereotypes(text: str) -> float:
    t = _norm_ws(text)
    matches = 0
    for p in STEREO_PATTERNS:
        matches += len(re.findall(p, t))
    # 2.5 per match
    return 2.5 * matches

def score_factuality(text: str) -> float:
    t = _norm_ws(text)
    score = 0.0
    # claimy = +2.0 each
    for p in CLAIMY_PHRASES:
        if p in t:
            score += 2.0
    # hedges = +0.7 each
    for h in HEDGE_PHRASES:
        if h in t:
            score += 0.7
    return score

def train_or_load_mlsignal(df: pd.DataFrame) -> Tuple[TfidfVectorizer, LogisticRegression]:
    """
    Tiny fallback TF-IDF + LogReg trained on the provided CSV:
    We treat rows with tag containing 'toxicity' or 'stereotype' or 'mlsignal'
    as positive (biased-ish), others negative. This is just for stub evals.
    """
    X_text = df["text"].astype(str).tolist()
    y = df["tag"].astype(str).str.contains(
        r"(toxicity|stereotype|mlsignal)", case=False, regex=True
    ).astype(int).to_numpy()

    vect = TfidfVectorizer(ngram_range=(1,2), min_df=1)
    X = vect.fit_transform(X_text)
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X, y)
    return vect, clf

def ml_probability(vect: TfidfVectorizer, clf: LogisticRegression, texts: List[str]) -> np.ndarray:
    X = vect.transform(texts)
    p = clf.predict_proba(X)[:, 1]
    # gamma blend toward 0.5
    return GAMMA * p + (1 - GAMMA) * 0.5

def normalize_for_overall(tox: float, st: float, fact: float, ml_prob: float) -> Tuple[float,float,float,float]:
    # crude capping/normalization to 0..1 so weights make sense
    tox_n  = min(tox / 3.0, 1.0)          # ~3.0 feels "high" toxicity
    st_n   = min(st  / 5.0, 1.0)          # 2 stereotype matches -> 1.0
    fact_n = min(fact/ 3.0, 1.0)          # ~3.0 feels "high" claimy+hedge
    ml_n   = float(np.clip(ml_prob, 0, 1))
    return tox_n, st_n, fact_n, ml_n

def compute_row_metrics(text: str) -> Tuple[float,float,float]:
    tox  = score_toxicity(text)
    st   = score_stereotypes(text)
    fact = score_factuality(text)
    return tox, st, fact

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in",  dest="inp", required=True, help="Input CSV path (id,text,tag)")
    ap.add_argument("--out", dest="outp", required=True, help="Output CSV path")
    args = ap.parse_args()

    inp = Path(args.inp)
    outp = Path(args.outp)
    if not inp.exists():
        print(f"[ERROR] input file not found: {inp}", file=sys.stderr)
        sys.exit(2)

    df = pd.read_csv(inp)
    if not {"id","text","tag"}.issubset(set(df.columns)):
        print("[ERROR] CSV must have columns: id,text,tag", file=sys.stderr)
        sys.exit(2)

    # compute rule-based detectors
    tox_list, st_list, fact_list = [], [], []
    for txt in df["text"].astype(str).tolist():
        tox, st, fact = compute_row_metrics(txt)
        tox_list.append(tox); st_list.append(st); fact_list.append(fact)

    # mlsignal (TF-IDF + LogReg on stub)
    vect, clf = train_or_load_mlsignal(df)
    ml_probs = ml_probability(vect, clf, df["text"].astype(str).tolist())

    # overall
    overalls = []
    tox_n_list, st_n_list, fact_n_list = [], [], []
    for tox, st, fact, mp in zip(tox_list, st_list, fact_list, ml_probs):
        tox_n, st_n, fact_n, ml_n = normalize_for_overall(tox, st, fact, mp)
        overall = (W_TOX * tox_n) + (W_ST * st_n) + (W_FACT * fact_n) + (W_ML * ml_n)
        overalls.append(overall)
        tox_n_list.append(tox_n); st_n_list.append(st_n); fact_n_list.append(fact_n)

    out = df.copy()
    out["toxicity"]     = tox_list
    out["stereotypes"]  = st_list
    out["factuality"]   = fact_list
    out["ml_prob"]      = ml_probs
    out["overall"]      = overalls

    outp.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(outp, index=False)

    # ---- Simple console summary ----
    print(f"Saved: {outp.resolve()}")
    print("\n== Summary ==")
    print(f"Rows: {len(out)}")
    print(f"Mean overall: {out['overall'].mean():.3f}")
    by_tag = out.groupby('tag')['overall'].mean().reset_index()
    print("Mean overall by tag:")
    for _, r in by_tag.iterrows():
        print(f"  {r['tag']}: {r['overall']:.3f}")

if __name__ == "__main__":
    main()
