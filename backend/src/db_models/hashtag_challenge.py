from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class HashtagChallengeTable(SQLModel, table=True):
    __tablename__ = "hashtag_challenge"

    hashtag_id: Optional[int] = Field(default=None,foreign_key="hashtags.id", primary_key=True)
    challenge_id: Optional[int] = Field(default=None, foreign_key="challenges.id", primary_key=True)
