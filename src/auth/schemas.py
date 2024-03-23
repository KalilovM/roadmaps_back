from pydantic import BaseModel


class Token(BaseModel):
    refresh_token: str
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    username: str
    password: str
