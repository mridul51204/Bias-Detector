import os
from pathlib import Path

def get_cache_dir() -> Path:
    """
    Returns a writable cache directory.
    On Streamlit Cloud this will be ephemeral but works during session.
    """
    base = Path(os.environ.get("BIAS_DETECTOR_CACHE_DIR", ".cache"))
    base.mkdir(exist_ok=True)
    return base
