"""
Domain-specific bias dictionaries or helpers.
Extend this with lists of terms relevant to your use case.
"""

POLITICAL_TERMS = [
    "leftist", "right-wing", "liberal", "conservative", "radical", "extremist"
]

ECONOMIC_TERMS = [
    "capitalist", "socialist", "communist", "free-market", "pro-business", "anti-business"
]

def get_domain_terms() -> dict:
    return {
        "political": POLITICAL_TERMS,
        "economic": ECONOMIC_TERMS,
    }
