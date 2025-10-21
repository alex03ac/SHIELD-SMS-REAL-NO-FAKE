KEYWORDS = {"urgente", "bloqueo", "banco", "clave", "verificar", "premio"}

def classify_text(text: str):
    score = 0.0
    if "http" in text or "www" in text:
        score += 0.6
    if any(k in text for k in KEYWORDS):
        score += 0.3
    label = "smishing" if score >= 0.5 else "legit"
    return label, round(min(score, 1.0), 2)
