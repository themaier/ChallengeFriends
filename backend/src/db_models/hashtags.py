from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from src.db_models.hashtag_challenge import HashtagChallengeTable


class HashtagTable(SQLModel, table=True):
    __tablename__ = "hashtags"

    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field(index=True)
    challenges: Optional[List["ChallengeTable"]] = Relationship(back_populates="hashtags", link_model=HashtagChallengeTable)