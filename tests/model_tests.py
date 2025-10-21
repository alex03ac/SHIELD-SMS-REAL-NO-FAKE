from backend.ModeloML.rules_model import classify_text

def test_classify_smishing_keyword():
    text = "URGENTE: Verifica tu cuenta"
    label, score = classify_text(text)
    assert label == "smishing"
    assert score >= 0.3

def test_classify_smishing_url():
    text = "Visita http://fake.com para ganar"
    label, score = classify_text(text)
    assert label == "smishing"
    assert score >= 0.6

def test_classify_legit():
    text = "Reunión con el equipo mañana"
    label, score = classify_text(text)
    assert label == "legit"
    assert score < 0.5
