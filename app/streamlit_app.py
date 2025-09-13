import streamlit as st

from src.scoring import aggregate_scores
from src.rewrite import suggest_rewrite
from src.utils.domain import guess_domain
from src.utils.text import sentences
from src.detectors.toxicity import score_toxicity
from src.detectors.stereotypes import score_stereotypes
from src.detectors.factuality import check_factuality

# Make ../src importable when running from app/
import sys, os, traceback, streamlit as st
CURRENT_DIR = os.path.dirname(__file__)
SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, '..', 'src'))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

# Optional: show Python version in sidebar for sanity
st.sidebar.write("Python:", sys.version)

st.set_page_config(page_title="Bias Detector", layout="wide")

st.title("Bias Detector for AI-Generated Content")
st.caption("MVP · Detect stereotype/tonal risks and basic factual issues. Step-2 will add ML models + evidence.")

with st.sidebar:
    st.header("Settings")
    weights = {
        "stereotype": st.slider("Weight: Stereotype", 0, 100, 40),
        "toxicity": st.slider("Weight: Toxicity", 0, 100, 30),
        "factuality": st.slider("Weight: Factuality (penalty)", 0, 100, 30),
    }
    st.caption("Overall = w1*stereotype + w2*toxicity + w3*(100 - factual_error)")
    st.divider()
    st.caption("Tip: Paste any chatbot output to analyze.")

st.subheader("Paste AI-generated text")
text = st.text_area("Input", height=220, placeholder="Paste chatbot output here...")

colA, colB = st.columns([1,1])
with colA:
    run_btn = st.button("Analyze")
with colB:
    st.write("")

if run_btn and text.strip():
    domain = guess_domain(text)
    st.write(f"**Detected domain:** `{domain}`")
    st.write("")

    # --- Run lightweight detectors (heuristic v0) ---
    tox_score, tox_spans = score_toxicity(text)
    stereo_score, stereo_notes = score_stereotypes(text)
    factual_error, facts_notes = check_factuality(text)

    overall = aggregate_scores(stereo_score, tox_score, factual_error, weights)

    # --- Scorecard ---
    st.markdown("### Scorecard")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Stereotype Risk (0-100)", stereo_score)
    m2.metric("Toxicity Risk (0-100)", tox_score)
    m3.metric("Factual Error (0-100)", factual_error)
    m4.metric("Overall Bias Score (0-100)", overall)

    # --- Explanations ---
    st.markdown("### Explanations & Highlights")
    with st.expander("Stereotype rationale"):
        if stereo_notes:
            for n in stereo_notes:
                st.write("• " + n)
        else:
            st.write("No obvious stereotype triggers found by the heuristic.")

    with st.expander("Toxicity rationale"):
        if tox_spans:
            st.write("Flagged terms:")
            st.code(", ".join(sorted(set([s for s, _ in tox_spans]))))
        else:
            st.write("No flagged terms found by the heuristic.")

    with st.expander("Factuality rationale"):
        if facts_notes:
            for n in facts_notes:
                st.write("• " + n)
        else:
            st.write("Heuristic didn’t find clear factual red-flags. Step-2 will add retrieval + NLI.")

    # --- Neutral rewrite suggestion ---
    st.markdown("### Suggested Neutral Rewrite")
    st.write(suggest_rewrite(text, stereo_score, tox_score, factual_error))

    # --- Per-sentence view (helps interviews) ---
    st.markdown("### Per-sentence View")
    for i, s in enumerate(sentences(text), start=1):
        st.write(f"**{i}.** {s}")

    st.caption("This is an MVP. Next, we’ll replace heuristics with trained models and add evidence links.")
else:
    st.info("Paste text and click **Analyze** to generate the scorecard.")
