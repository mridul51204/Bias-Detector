def guess_domain(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["election", "policy", "minister", "senate", "parliament", "party", "manifesto"]):
        return "politics"
    if any(k in t for k in ["stock", "loan", "revenue", "profit", "interest rate", "market", "finance", "roi", "npa"]):
        return "finance"
    if any(k in t for k in ["health", "vaccine", "symptom", "diagnosis", "treatment", "medicine", "disease", "therapy"]):
        return "healthcare"
    return "general"
