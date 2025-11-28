from app.schemas.jwt_sch import Token, TokenData, TokenRefreshRequest, RefreshTokenResponse

def test_token_fields():
    token = Token(access_token="abc", refresh_token="def", token_type="bearer")
    assert token.access_token == "abc"
    assert token.token_type == "bearer"

def test_token_data_optional():
    data = TokenData(id="1", email="test@example.com")
    assert data.id == "1"
    assert data.email == "test@example.com"

def test_token_refresh_request():
    req = TokenRefreshRequest(refresh_token="def")
    assert req.refresh_token == "def"

def test_refresh_token_response():
    resp = RefreshTokenResponse(access_token="abc", token_type="bearer")
    assert resp.access_token == "abc"
