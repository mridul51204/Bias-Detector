import re
from typing import List

def sentences(text: str) -> List[str]:
    """
    Tiny sentence splitter good enough for MVP (no punkt download needed).
    """
    rough = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in rough if s]
