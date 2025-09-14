import streamlit as st
import pandas as pd
import numpy as np

from bias_detector.pipeline import detect_bias, explain_bias

st.set_page_config(page_title="Bias Detector", page_icon="🧪", layout="wide")

st.title("Bias Detector (Baseline)")
st.write("Minimal, testable build that works with pandas/numpy locally and on Cloud.")

with st.expander("System check"):
    st.write({
        "python": str(np.__get_config__).__class__.__module__.split('.')[0],  # quick import sanity
        "numpy_version": np.__version__,
        "pandas_version": pd.__version__,
    })
    st.success("Imports OK. If this section fails, fix requirements before adding features.")

tab_text, tab_csv = st.tabs(["Single text", "CSV batch"])

with tab_text:
    text = st.text_area("Paste text to analyze", height=160, placeholder="Paste any paragraph...")
    if st.button("Analyze text", type="primary", use_container_width=True):
        result = detect_bias(text or "")
        st.json(result)
        st.caption(explain_bias(result))

with tab_csv:
    file = st.file_uploader("Upload CSV (column: text)", type=["csv"])
    if file:
        df = pd.read_csv(file)
        if "text" not in df.columns:
            st.error("CSV must have a 'text' column.")
        else:
            df["bias_result"] = df["text"].fillna("").apply(lambda t: detect_bias(t)["score"])
            st.dataframe(df.head(50))
            st.success("Processed! (Shows first 50 rows)")

st.info("This is the baseline build. We’ll add NLP/ML in stages after confirming env stability.")
