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
from utils import scoring, rewrite

# ---------------- UI CONFIG ----------------
st.set_page_config(page_title="Bias Detector", page_icon="🧪", layout="wide")
st.title("Bias Detector — Clean Baseline")

# session state for CSV download
if "last_csv_results" not in st.session_state:
    st.session_state["last_csv_results"] = None

with st.expander("Environment / Health check"):
    st.write({
        "python_ok": True,
        "numpy_version": np.__version__,
        "pandas_version": pd.__version__,
        "detectors_ok": detectors_health(),
    })
    st.caption("If any import fails here, fix requirements locally before deploying.")

tabs = st.tabs(["Single Text", "CSV Batch", "Rewrite Suggestion"])

# ---------------- SINGLE TEXT ----------------
with tabs[0]:
    text = st.text_area("Paste text", height=180, placeholder="Paste a paragraph...")
    if st.button("Analyze", type="primary"):
        result = analyze_text(text or "")
        st.subheader("Result")
        st.json(result)
        # Show component scores + ML prob clearly
        cols = st.columns(4)
        cols[0].metric("Toxicity (0–10)", round(result["toxicity"]["score"], 2))
        cols[1].metric("Stereotypes (0–10)", round(result["stereotypes"]["score"], 2))
        cols[2].metric("Factuality (0–10)", round(result["factuality"]["score"], 2))
        cols[3].metric("ML prob (0–1)", f"{result['mlsignal']['proba']:.2f}")
        st.metric("Overall bias score", round(result["overall"]["score"], 2))
        ov = result["overall"]["score"]
        # new thresholds (case-1 = MODERATE, case-2 = LOW)
        if   ov >= 6.5: sev = "HIGH"
        elif ov >= 2.5: sev = "MODERATE"
        else:           sev = "LOW"
        st.write(f"**Overall severity:** {sev}")
        st.caption("Scores are heuristic and capped for stability.")

# ---------------- CSV BATCH ----------------
with tabs[1]:
    st.markdown("Upload a CSV with a **text** column. Optional columns: **id**, **tag**.")
    up = st.file_uploader("Upload CSV", type=["csv"])

    if up:
        try:
            df_in = pd.read_csv(up)
        except Exception as e:
            st.error(f"Failed to read CSV: {e}")
            df_in = None

        if df_in is not None:
            if "text" not in df_in.columns:
                st.error("CSV must contain a 'text' column.")
            else:
                # Normalize optional columns
                has_id = "id" in df_in.columns
                has_tag = "tag" in df_in.columns
                if not has_id:
                    df_in["id"] = range(1, len(df_in) + 1)
                if not has_tag:
                    df_in["tag"] = ""

                # Run detectors row-wise
                rows = []
                for _id, text, tag in df_in[["id", "text", "tag"]].fillna("").itertuples(index=False):
                    r = analyze_text(text)
                    rows.append({
                        "id": _id,
                        "text": text,
                        "tag": tag,
                        "toxicity":     r["toxicity"]["score"],
                        "stereotypes":  r["stereotypes"]["score"],
                        "factuality":   r["factuality"]["score"],
                        "ml_prob":      r["mlsignal"]["proba"],
                        "overall":      r["overall"]["score"],
                    })

                results_df = pd.DataFrame(rows)
                # Keep consistent column order
                results_df = results_df[["id","text","tag","toxicity","stereotypes","factuality","ml_prob","overall"]]

                # Save in session and display
                st.session_state["last_csv_results"] = results_df

                st.success(f"Processed {len(results_df)} rows. (Showing first 50)")
                st.dataframe(results_df.head(50), use_container_width=True)

                # Download button
                csv_bytes = results_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download results CSV",
                    data=csv_bytes,
                    file_name="bias_eval_results.csv",
                    mime="text/csv",
                    type="primary",
                )
    else:
        # If nothing uploaded, show a hint + optional last results
        st.info("No CSV uploaded yet. You can test with `tests\\tests_snippets.csv`.")
        if st.session_state["last_csv_results"] is not None:
            st.write("Last results in memory:")
            st.dataframe(st.session_state["last_csv_results"].head(20), use_container_width=True)

# ---------------- REWRITE ----------------
with tabs[2]:
    sample = st.text_area("Text to rewrite (soften bias/toxicity)", height=160)
    if st.button("Rewrite", key="rw"):
        st.write(rewrite.rewrite_text(sample or ""))

st.caption("Baseline version; add ML later once this runs clean locally.")
