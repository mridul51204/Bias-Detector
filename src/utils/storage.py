"""
Placeholder for Step-5 (SQLite logging + Plotly dashboard).
We keep a simple interface so app imports don’t fail.
"""

from typing import Dict, Any, Optional, List

def init_db(_path: str = "data/bias.db") -> None:
    return None

def log_analysis(_record: Dict[str, Any]) -> None:
    """
    Expected keys (later):
      text, domain, stereotype_score, toxicity_score, factual_error, overall, timestamp
    """
    return None

def fetch_summary(_limit: int = 100) -> List[Dict[str, Any]]:
    return []
