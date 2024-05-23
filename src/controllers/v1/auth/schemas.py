from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    role: str


class UserSignInOut(BaseModel):
    access: str
    refresh: str
