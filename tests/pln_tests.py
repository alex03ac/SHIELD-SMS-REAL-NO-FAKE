from backend.PLN.preprocessing import normalize

def test_normalize_lowercase():
    text = "HOLA MUNDO"
    assert normalize(text) == "hola mundo"

def test_normalize_accents():
    text = "Verificación Clavé Única"
    assert normalize(text) == "verificacion clave unica"

def test_normalize_empty():
    assert normalize("") == ""
