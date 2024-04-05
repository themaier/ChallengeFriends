from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class FriendsTable(SQLModel, table=True):
    __tablename__ = "friends"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    friend_user_id: int
    # status: bool