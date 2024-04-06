from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class FriendsTable(SQLModel, table=True):
    __tablename__ = "friends"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    friend_user_id: str
    # status: bool