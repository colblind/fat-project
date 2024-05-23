from pydantic import BaseModel


class UserSignInCredentials(BaseModel):
    email: str
    password: str


class TokenPairStr(BaseModel):
    access: str
    refresh: str


class RefreshAccessTokenIn(BaseModel):
    refresh: str
