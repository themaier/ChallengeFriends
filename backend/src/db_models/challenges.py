from enum import Enum
from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

from src.db_models.hashtag_challenge import HashtagChallengeTable


class ChallengeStatus(Enum):
    DONE = "done"
    PENDING = "pending"
    DECLINED = "declined"
    ACCEPTED = "accepted"
    ASLINK = "aslink"


class ChallengeTable(SQLModel, table=True):
    __tablename__ = "challenges"

    id: Optional[int] = Field(default=None, primary_key=True)
    sender_user_id: int
    receiver_user_id: Optional[int] = None
    title: str
    description: str
    reward: Optional[str]
    challenge_resources: str
    prove_resource: str
    done_date: Optional[datetime] = Field()
    status: ChallengeStatus

    hashtags: Optional[List["HashtagTable"]] = Relationship(
        back_populates="challenges", link_model=HashtagChallengeTable
    )
