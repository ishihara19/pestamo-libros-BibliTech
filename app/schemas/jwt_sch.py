from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    id: str | None = None
    email: str | None = None       

class TokenRefreshRequest(BaseModel):
    refresh_token: str 

class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str       
    