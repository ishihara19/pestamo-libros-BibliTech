from app.utils.generar_token import generar_token

def test_generar_token_default_length():
    token = generar_token()
    assert isinstance(token, str)
    assert len(token) == 12

def test_generar_token_custom_length():
    token = generar_token(20)
    assert len(token) == 20
