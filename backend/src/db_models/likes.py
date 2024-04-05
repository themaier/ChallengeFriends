from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from src.db_models.hashtag_challenge import HashtagChallengeTable


class LikesTable(SQLModel, table=True):
    __tablename__ = "likes"

    user_id: int = Field(default=None, primary_key=True)
    challenge_id: int = Field(default=None, primary_key=True)
    state: bool

