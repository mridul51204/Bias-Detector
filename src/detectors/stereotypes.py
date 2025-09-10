from typing import List, Tuple

# Minimal stereotype triggers (occupation + gendered clichés, culture generalizations).
# We’ll replace this with CrowS-Pairs/BOLD-guided model checks in Step-3.
TRIGGERS = {
    "gender": [
        ("women are bad at math", 40),
        ("men are bad at caregiving", 40),
        ("girls are emotional", 25),
        ("boys are aggressive", 25),
        ("housewife should", 25),
        ("man of the house", 20),
    ],
    "culture": [
        ("all asians", 35),
        ("all indians", 30),
        ("westerners are", 25),
        ("muslims are", 35),
        ("christians are", 35),
        ("hindus are", 35),
        ("immigrants are", 30),
        ("they all are lazy", 30),
    ],
    "profession": [
        ("nurses are women", 30),
        ("engineers are men", 30),
        ("teachers are women", 25),
        ("ceos are men", 25),
    ],
}

def score_stereotypes(text: str) -> Tuple[int, List[str]]:
    """
    Simple phrase-match risk.
    Returns: (score 0-100, notes list)
    """
    tl = text.lower()
    score = 0
    notes: List[str] = []
    for bucket, pairs in TRIGGERS.items():
        for phrase, weight in pairs:
            if phrase in tl:
                score += weight
                notes.append(f"Matched '{phrase}' ({bucket}, +{weight})")
    score = min(100, score)
    return score, notes
