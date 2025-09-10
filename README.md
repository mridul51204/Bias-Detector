# Bias-Detector
Bias Detector for AI-Generated Content (MVP project).

# Bias Detector for AI-Generated Content (MVP)

Detects **stereotype risk**, **toxicity risk**, and **factual issues** in chatbot outputs.  
This is a 3-day MVP focused on a clear **scorecard**, **explanations**, and a **neutral rewrite** suggestion.

## Quickstart
```bash
# 1) Create and activate a virtual env (recommended)
python -m venv .venv
# Windows:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

# 2) Install deps
pip install -r requirements.txt
python -m spacy download en_core_web_sm  # future use

# 3) Run
streamlit run app/streamlit_app.py
