# 🧪 Bias Detector — Prototype

An interactive **Streamlit app** to detect and analyze **bias in text**.  
Designed as a prototype to showcase **rule-based heuristics, lightweight ML models, and reproducible evaluation pipelines**.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bias-detector-n5emmpymm8toqsp9wf92uh.streamlit.app/)

---

## ✨ Features

- **Four bias detectors**
  - **Toxicity** → detects insults, repeats, excessive punctuation.  
  - **Stereotypes** → regex-based stereotype pattern matches.  
  - **Factuality** → claimy phrases and hedge words.  
  - **ML Signal** → TF-IDF + Logistic Regression, blended with γ=0.75.  

- **Weighted scoring system**  
  - Toxicity (0.40), Stereotypes (0.30), Factuality (0.10), ML Signal (0.20).  
  - Severity bands: **LOW / MODERATE / HIGH**.  

- **Streamlit UI**  
  - **Single Text**: paste text, get scores + severity.  
  - **CSV Batch**: upload CSV, process multiple rows, export results.  
  - **Rewrite**: prototype softening of biased/toxic text (heuristic).  

- **Evaluation pipeline**  
  - `tools/make_eval.py` → run detectors + ML on datasets, save results.  
  - `tests/test_snippets.csv` → stub dataset for quick validation.  

- **Cross-platform ready**  
  - Tested on Python **3.13**, runs on both Windows and Streamlit Cloud (Linux).  
  - Pinned requirements for reproducibility.  

---

## 🚀 Getting Started

### 1. Clone & set up environment
```bash
git clone https://github.com/<your-username>/bias-detector.git
cd bias-detector
python -m venv .venv
.venv\Scripts\activate   # Windows
# OR
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

Example Outputs

Single Text Mode:
Text: "Shut up, shut up, shut up — you're so stupid!!!"
→ Toxicity: 3.0, Stereotypes: 0.0, Factuality: 0.0, ML Prob: 0.81
→ Overall Score: 6.2 → Severity: MODERATE

Rewrite Mode:
Input:  "idiot idiot idiot!!! Shut up!!"
Output: "Person person! please be quiet!"



