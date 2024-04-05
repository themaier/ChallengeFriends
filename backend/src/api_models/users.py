from typing import Optional
from pydantic import BaseModel


class UserVerify(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    challengeId: Optional[int] = None
