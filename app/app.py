import sys
from pathlib import Path

# --- make `src/` importable without pyproject for now ---
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import streamlit as st
import pandas as pd
import numpy as np

# our package-style imports (from src/)
from detectors import analyze_text, detectors_health
from utils import scoring, rewwrite

st.set_page_config(page_title="Bias Detector", page_icon="🧪", layout="wide")
st.title("Bias Detector — Clean Baseline")

with st.expander("Environment / Health check"):
    st.write({
        "python_ok": True,
        "numpy_version": np.__version__,
        "pandas_version": pd.__version__,
        "detectors_ok": detectors_health(),
    })
    st.caption("If any import fails here, fix requirements locally before deploying.")

tabs = st.tabs(["Single Text", "CSV Batch", "Rewrite Suggestion"])

with tabs[0]:
    text = st.text_area("Paste text", height=180, placeholder="Paste a paragraph...")
    if st.button("Analyze", type="primary"):
        result = analyze_text(text or "")
        st.subheader("Result")
        st.json(result)
        st.metric("Overall bias score", result["overall"]["score"])
        st.caption("Scores are heuristic and capped for stability.")

with tabs[1]:
    up = st.file_uploader("Upload CSV with a 'text' column", type=["csv"])
    if up:
        df = pd.read_csv(up)
        if "text" not in df.columns:
            st.error("CSV must contain a 'text' column.")
        else:
            out = []
            for t in df["text"].fillna(""):
                r = analyze_text(t)
                out.append(r["overall"]["score"])
            df["bias_score"] = out
            st.dataframe(df.head(50))
            st.success("Processed. (Showing first 50 rows)")

with tabs[2]:
    sample = st.text_area("Text to rewrite (soften bias/toxicity)", height=160)
    if st.button("Rewrite", key="rw"):
        st.write(rewwrite.rewrite_text(sample or ""))

st.caption("Baseline version; add ML later once this runs clean locally.")
