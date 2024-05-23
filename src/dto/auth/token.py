from datetime import datetime
from typing import Optional, Final

from pydantic import BaseModel

class Token(BaseModel):
    aud: str
    sub: int
    iat: datetime
    jti: str
    exp: Optional[datetime] = None


class AccessToken(Token):
    token_type: Final[str] = 'access'


class RefreshToken(Token):
    token_type: Final[str] = 'refresh'
